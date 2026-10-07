"""Layout-aware, local-only PDF OCR using Surya and pypdfium2."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


# Avoid exhausting or losing unsupported Vulkan devices; users can override
# these defaults through the corresponding Surya environment variables.
os.environ.setdefault("LLAMA_CPP_NGL", "0")
os.environ.setdefault("SURYA_INFERENCE_PARALLEL", "1")


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = BASE_DIR / "data_unprocessing"
DEFAULT_OUTPUT_DIR = BASE_DIR / "data_processed"
FIGURE_LABELS = {"figure", "diagram", "image", "picture"}
PIPELINE_VERSION = "surya-local-v1"


def _already_processed(pdf_path: Path, output_dir: Path) -> bool:
    document_dir = output_dir / pdf_path.stem
    markdown_path = document_dir / f"{pdf_path.stem}.md"
    metadata_path = document_dir / f"{pdf_path.stem}_metadata.json"
    if not markdown_path.is_file() or not metadata_path.is_file():
        return False
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        metadata.get("pipeline") == PIPELINE_VERSION
        and metadata.get("source") == pdf_path.name
        and isinstance(metadata.get("pages_processed"), list)
    )


def _parse_page_range(value: str | None, page_count: int) -> list[int]:
    if not value:
        return list(range(page_count))

    pages: set[int] = set()
    try:
        for part in value.split(","):
            part = part.strip()
            if not part:
                raise ValueError("có phần tử trang rỗng")
            if "-" in part:
                start_text, end_text = part.split("-", maxsplit=1)
                start, end = int(start_text), int(end_text)
                if start > end:
                    raise ValueError(f"khoảng trang không hợp lệ: {part}")
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
    except ValueError as exc:
        raise ValueError(
            f"Khoảng trang không hợp lệ {value!r}; dùng dạng 0-2,5."
        ) from exc

    selected = sorted(pages)
    if any(page < 0 or page >= page_count for page in selected):
        raise ValueError(
            f"Khoảng trang nằm ngoài PDF có {page_count} trang: {value!r}."
        )
    return selected


def _html_to_markdown(html: str) -> str:
    from bs4 import BeautifulSoup, NavigableString

    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        rows = []
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"], recursive=False)
            if cells:
                rows.append(
                    [
                        cell.get_text(" ", strip=True).replace("|", r"\|")
                        for cell in cells
                    ]
                )
        if not rows:
            table.decompose()
            continue

        width = max(map(len, rows))
        rows = [row + [""] * (width - len(row)) for row in rows]
        lines = [
            "| " + " | ".join(rows[0]) + " |",
            "| " + " | ".join("---" for _ in range(width)) + " |",
        ]
        lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
        table.replace_with(NavigableString("\n\n" + "\n".join(lines) + "\n\n"))

    for line_break in soup.find_all("br"):
        line_break.replace_with("\n")
    text = soup.get_text("\n", strip=True)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _crop_block(image: Any, block: Any) -> Any:
    x0, y0, x1, y1 = block.bbox
    pad = 5
    bounds = (
        max(0, int(x0) - pad),
        max(0, int(y0) - pad),
        min(image.width, int(x1) + pad),
        min(image.height, int(y1) + pad),
    )
    if bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
        raise ValueError(f"Invalid OCR block bounds: {bounds}")
    return image.crop(bounds)


def _safe_image_name(name: str) -> str:
    return re.sub(r"[^\w.-]+", "_", name).strip("._") or "figure"


class LocalPDFOCR:
    """OCR page layout and figure crops with a local Surya inference server."""

    def __init__(self, batch_size: int = 2, dpi: int = 192):
        try:
            from surya.inference import SuryaInferenceManager
            from surya.layout.schema import LayoutBox, LayoutResult
            from surya.recognition import RecognitionPredictor
        except ImportError as exc:
            raise RuntimeError(
                "Thiếu thư viện Surya trong môi trường Python hiện tại."
            ) from exc

        self.manager = SuryaInferenceManager()
        self.predictor = RecognitionPredictor(self.manager)
        self.LayoutBox = LayoutBox
        self.LayoutResult = LayoutResult
        self.batch_size = batch_size
        self.dpi = dpi

    def close(self) -> None:
        self.manager.stop()

    def process_pdf(
        self,
        pdf_path: Path,
        output_dir: Path,
        page_range: str | None = None,
    ) -> Path:
        import pypdfium2 as pdfium

        document = pdfium.PdfDocument(str(pdf_path))
        try:
            page_count = len(document)
            page_numbers = _parse_page_range(page_range, page_count)
            document_dir = output_dir / pdf_path.stem
            images_dir = document_dir / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            markdown_pages: list[str] = []
            metadata_pages: list[dict[str, Any]] = []

            for page_number in page_numbers:
                page = document[page_number]
                text_page = page.get_textpage()
                native_text = text_page.get_text_range().strip()
                native_text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", native_text)
                has_usable_text_layer = (
                    len(native_text) >= 40
                    and native_text.count("\ufffd") / max(len(native_text), 1) < 0.02
                )
                embedded_images = list(
                    page.get_objects(filter=[pdfium.raw.FPDF_PAGEOBJ_IMAGE])
                )
                page_image = None

                if has_usable_text_layer:
                    page_markdown = f"## Trang {page_number + 1}\n\n{native_text}"
                    page_metadata: dict[str, Any] = {
                        "page": page_number + 1,
                        "source": "pdf-text-layer",
                        "images": [],
                    }
                else:
                    page_image = (
                        page.render(scale=self.dpi / 72, draw_annots=False)
                        .to_pil()
                        .convert("RGB")
                    )
                    page_results = self.predictor([page_image], full_page=True)
                    if len(page_results) != 1:
                        raise RuntimeError(
                            f"OCR trả về {len(page_results)} kết quả cho "
                            f"trang {page_number + 1}."
                        )
                    page_markdown, page_metadata = self._render_page(
                        page_number,
                        page_image,
                        page_results[0],
                        images_dir,
                    )
                    page_metadata["source"] = "surya-ocr"
                    page_metadata["images"] = []

                if embedded_images:
                    if page_image is None:
                        page_image = (
                            page.render(scale=self.dpi / 72, draw_annots=False)
                            .to_pil()
                            .convert("RGB")
                        )
                    image_items = self._extract_embedded_images(
                        page,
                        page_image,
                        page_number,
                        embedded_images,
                        images_dir,
                    )
                    for _, _, _, filename in image_items:
                        page_metadata["images"].append(filename)
                    image_ocr = self._ocr_figure_crops(image_items)
                    if image_ocr:
                        page_markdown += "\n\n### Hình ảnh trên trang"
                        for _, _, _, filename, text in image_ocr:
                            page_markdown += f"\n\n![Hình ảnh](images/{filename})"
                            if text:
                                page_markdown += (
                                    "\n\n**OCR trong hình (theo thứ tự đọc):**"
                                    f"\n\n{text}"
                                )

                markdown_pages.append(page_markdown)
                metadata_pages.append(page_metadata)

            document_dir.mkdir(parents=True, exist_ok=True)
            markdown_path = document_dir / f"{pdf_path.stem}.md"
            markdown_path.write_text(
                "\n\n---\n\n".join(markdown_pages).rstrip() + "\n",
                encoding="utf-8",
            )
            (document_dir / f"{pdf_path.stem}_metadata.json").write_text(
                json.dumps(
                    {
                        "pipeline": PIPELINE_VERSION,
                        "source": pdf_path.name,
                        "page_count": page_count,
                        "pages_processed": page_numbers,
                        "pages": metadata_pages,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            return markdown_path
        finally:
            document.close()

    def _render_page(
        self,
        page_number: int,
        page_image: Any,
        page_result: Any,
        images_dir: Path,
    ) -> tuple[str, dict[str, Any]]:
        ordered_blocks = sorted(page_result.blocks, key=lambda block: block.reading_order)
        figure_items = []
        for block_index, block in enumerate(ordered_blocks, start=1):
            if block.label.casefold() not in FIGURE_LABELS:
                continue
            crop = _crop_block(page_image, block)
            if crop.width < 32 or crop.height < 24:
                continue
            filename = _safe_image_name(
                f"page_{page_number + 1:04d}_{block.label}_{block_index:03d}.jpg"
            )
            crop.save(images_dir / filename, format="JPEG", quality=95)
            figure_items.append((block_index, block, crop, filename))

        figure_ocr = self._ocr_figure_crops(figure_items)
        figure_by_index = {
            block_index: (block, filename, text)
            for block_index, block, _, filename, text in figure_ocr
        }

        output_blocks = [f"## Trang {page_number + 1}"]
        metadata_blocks = []
        for block_index, block in enumerate(ordered_blocks, start=1):
            label = block.label
            text = _html_to_markdown(block.html) if block.html else ""
            figure = figure_by_index.get(block_index)
            if figure:
                _, filename, figure_text = figure
                text = (
                    f"![{label} - trang {page_number + 1}](images/{filename})"
                    + (
                        f"\n\n**OCR trong hình (theo thứ tự đọc):**\n\n{figure_text}"
                        if figure_text
                        else ""
                    )
                )
            if text:
                output_blocks.append(text)
            metadata_blocks.append(
                {
                    "label": label,
                    "reading_order": block.reading_order,
                    "bbox": [round(value, 1) for value in block.bbox],
                    "confidence": block.confidence,
                }
            )

        return (
            "\n\n".join(output_blocks),
            {"page": page_number + 1, "blocks": metadata_blocks},
        )

    def _extract_embedded_images(
        self,
        page: Any,
        page_image: Any,
        page_number: int,
        image_objects: list[Any],
        images_dir: Path,
    ) -> list[tuple[int, Any, Any, str]]:
        page_width, page_height = page.get_size()
        scale_x = page_image.width / page_width
        scale_y = page_image.height / page_height
        images = []
        pad = 5

        for image_number, image_object in enumerate(image_objects, start=1):
            left, bottom, right, top = image_object.get_bounds()
            bounds = (
                max(0, int(left * scale_x) - pad),
                max(0, int((page_height - top) * scale_y) - pad),
                min(page_image.width, int(right * scale_x) + pad),
                min(page_image.height, int((page_height - bottom) * scale_y) + pad),
            )
            if bounds[2] - bounds[0] < 32 or bounds[3] - bounds[1] < 24:
                continue

            crop = page_image.crop(bounds)
            filename = _safe_image_name(
                f"page_{page_number + 1:04d}_image_{image_number:03d}.jpg"
            )
            crop.save(images_dir / filename, format="JPEG", quality=95)
            images.append((image_number, image_object, crop, filename))

        return images

    def _ocr_figure_crops(
        self, figures: list[tuple[int, Any, Any, str]]
    ) -> list[tuple[int, Any, Any, str, str]]:
        results: list[tuple[int, Any, Any, str, str]] = []
        for start in range(0, len(figures), self.batch_size):
            batch = figures[start : start + self.batch_size]
            images = [item[2] for item in batch]
            layouts = [
                self.LayoutResult(
                    bboxes=[
                        self.LayoutBox(
                            polygon=[
                                [0, 0],
                                [image.width, 0],
                                [image.width, image.height],
                                [0, image.height],
                            ],
                            label="Text",
                            raw_label="Text",
                            position=0,
                            count=1200,
                        )
                    ],
                    image_bbox=[0, 0, image.width, image.height],
                )
                for image in images
            ]
            recognized = self.predictor(
                images=images,
                layout_results=layouts,
                full_page=False,
            )
            if len(recognized) != len(batch):
                raise RuntimeError(
                    "Số kết quả OCR ảnh không khớp số ảnh đầu vào "
                    f"({len(recognized)} kết quả / {len(batch)} ảnh)."
                )
            for item, page_result in zip(batch, recognized):
                block_index, block, image, filename = item
                text = "\n\n".join(
                    value
                    for result_block in sorted(
                        page_result.blocks, key=lambda value: value.reading_order
                    )
                    if (value := _html_to_markdown(result_block.html))
                )
                results.append((block_index, block, image, filename, text))
        return results


def _pdf_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            raise ValueError(f"Đầu vào không phải PDF: {input_path}")
        return [input_path]
    if not input_path.is_dir():
        raise FileNotFoundError(f"Không tìm thấy đầu vào: {input_path}")
    return sorted(
        (path for path in input_path.iterdir() if path.suffix.lower() == ".pdf"),
        key=lambda path: path.name.casefold(),
    )


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description=(
            "OCR PDF bằng Surya chạy cục bộ, không cần AI API key. "
            "Nhận diện thứ tự đọc, cột, bảng và chữ trong ảnh/diagram."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"PDF hoặc thư mục PDF (mặc định: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Thư mục kết quả (mặc định: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--page-range",
        help="Chỉ xử lý trang, đánh số từ 0, ví dụ: 0-2,5",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Bỏ qua PDF đã được hoàn tất bằng script này.",
    )
    args = parser.parse_args(argv)

    try:
        pdfs = _pdf_files(args.input)
        if not pdfs:
            print(f"Không tìm thấy PDF trong: {args.input}", file=sys.stderr)
            return 1

        pending = [
            pdf
            for pdf in pdfs
            if not args.skip_existing or not _already_processed(pdf, args.output)
        ]
        skipped = len(pdfs) - len(pending)
        print(f"Tìm thấy {len(pdfs)} PDF; bỏ qua {skipped} PDF đã có kết quả.")
        if not pending:
            return 0
        if not args.skip_existing and any(
            (args.output / pdf.stem / f"{pdf.stem}.md").exists()
            for pdf in pending
        ):
            print("Lưu ý: kết quả Markdown hiện có sẽ được ghi đè.")

        processor = LocalPDFOCR()
        succeeded = 0
        failed: list[tuple[Path, Exception]] = []
        try:
            for pdf_path in pending:
                print(f"[ĐANG OCR] {pdf_path.name}", flush=True)
                try:
                    result_path = processor.process_pdf(
                        pdf_path,
                        args.output,
                        page_range=args.page_range,
                    )
                except Exception as exc:
                    failed.append((pdf_path, exc))
                    print(f"[LỖI] {pdf_path.name}: {exc}", file=sys.stderr)
                else:
                    succeeded += 1
                    print(f"[OK] {pdf_path.name} -> {result_path}")
        finally:
            processor.close()

        print(
            f"Hoàn tất: {succeeded} thành công, {len(failed)} lỗi, "
            f"{skipped} bỏ qua. Kết quả: {args.output}"
        )
        return 1 if failed else 0
    except Exception as exc:
        print(f"Lỗi OCR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
