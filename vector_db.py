from pathlib import Path
import json
import numpy as np
import chromadb
from chromadb.config import Settings
from tqdm import tqdm


# ============================================================
# PSAI VECTOR DB PIPELINE v1
#
# Input:
#   D:\fall26\DSP_PROJECT\data_embedded\<doc_id>\<doc_id>.npy
#   D:\fall26\DSP_PROJECT\data_embedded\<doc_id>\<doc_id>.meta.json
#
# Output:
#   D:\fall26\DSP_PROJECT\chroma_db\
#
# Collection:
#   name     = "psai_chunks"
#   distance = "cosine"
# ============================================================


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(r"D:\fall26\DSP_PROJECT")

EMBED_DIR = BASE_DIR / "data_embedded"
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "psai_chunks"
BATCH_ADD = 128

RESET_COLLECTION = True


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

def load_embeddings():
    meta_files = sorted(EMBED_DIR.rglob("*.meta.json"))
    if not meta_files:
        return

    for meta_file in meta_files:
        doc_id = meta_file.parent.name
        npy_file = meta_file.parent / f"{doc_id}.npy"

        if not npy_file.exists():
            print(f"[SKIP] {doc_id}: missing .npy")
            continue

        vectors = np.load(npy_file)
        meta = json.loads(meta_file.read_text(encoding="utf-8"))

        if len(vectors) != len(meta):
            print(f"[SKIP] {doc_id}: vectors/meta mismatch")
            continue

        yield doc_id, vectors, meta


# ============================================================
# BUILD COLLECTION
# ============================================================

def build_collection():
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    if RESET_COLLECTION:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"Deleted existing collection '{COLLECTION_NAME}'.")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    total_added = 0

    for doc_id, vectors, meta in tqdm(load_embeddings(), desc="Documents"):
        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for vec, m in zip(vectors, meta):
            ids.append(m["chunk_id"])
            embeddings.append(vec.tolist())
            metadatas.append({
                "doc_id": m.get("doc_id", doc_id),
                "chunk_index": int(m.get("chunk_index", 0)),
                "section": m.get("section", ""),
                "heading_path": " > ".join(m.get("heading_path", [])),
                "block_type": m.get("block_type", "section"),
                "token_count": int(m.get("token_count", 0)),
                "hash": m.get("hash", ""),
            })
            documents.append(m["text"])

        # add in batches
        for i in range(0, len(ids), BATCH_ADD):
            collection.add(
                ids=ids[i:i + BATCH_ADD],
                embeddings=embeddings[i:i + BATCH_ADD],
                metadatas=metadatas[i:i + BATCH_ADD],
                documents=documents[i:i + BATCH_ADD],
            )
            total_added += len(ids[i:i + BATCH_ADD])

        print(f"[{doc_id}] added {len(ids)} chunks")

    print()
    print(f"Total chunks in DB: {collection.count()}")

    return collection


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 75)
    print("PSAI VECTOR DB PIPELINE v1")
    print("=" * 75)
    print(f"EMBED_DIR : {EMBED_DIR}")
    print(f"CHROMA_DIR: {CHROMA_DIR}")
    print(f"COLLECTION: {COLLECTION_NAME}")
    print()

    if not EMBED_DIR.exists():
        print("ERROR: embedding folder does not exist.")
        return

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    collection = build_collection()

    print()
    print("=" * 75)
    print("VECTOR DB FINISHED")
    print("=" * 75)
    print(f"Collection : {COLLECTION_NAME}")
    print(f"Chunks     : {collection.count()}")
    print(f"Path       : {CHROMA_DIR}")


if __name__ == "__main__":
    main()