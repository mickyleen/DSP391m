# Sport Video Analysis for Billiard Matches

Final Project Proposal

#### Group members: Vishesh Goyal and Himashi Bogahawaththa

### 1. Introduction

This proposal follows the final project brief for sport video analysis of Eight Ball billiard matches. The goal is to design a computer vision system that processes billiard video clips frame by frame and produces high-level information about the match state, including ball positions, ball categories, the playing-field area, and a 2D top-view minimap.

Our solution will be implemented in C++ with OpenCV and will use classical image-processing techniques rather than deep learning. The proposed system is intended to be robust across the provided benchmark clips, which differ in camera perspective, number of visible balls, and pool-table colour.

|Project scope | Classical computer vision system for analysing Eight Ball billiard |
|--------------------------- | --------------------------------------------------------------------- |
|Implementation constraint | C++ and OpenCV only; no deep learning models or external detector |
|Main outputs | Ball localisation/classification, playing-field boundary detection, |
|Proposed extension | Pocket-aware game-state tracking that removes balls from the |
|Evaluation dataset | The 10 provided benchmark clips and the annotated first/last frames |

# 2. Required System Outputs

|Task | Required output Planned implementation |
|----------------------------------- | ----------------------------------------------- |
|Ball recognition and localisation | Detect all balls and assign category IDs: cue |
|Playing-field boundary detection | Detect the main lines delimiting the billiard |
|Semantic segmentation | Generate a mask for background, cue ball, 8- |
|2D top-view minimap | Display ball positions and trajectories in a |

#### 3.1 Playing Field Detection

For each clip, the table area will be detected from the first frame and reused for the remaining frames, following the project simplification that the camera pose does not change within a single video. The cloth region will be isolated through HSV thresholding and contour filtering. The upper rail edges will then be estimated using Canny edge detection and the Probabilistic Hough Transform. Intersections of the four selected boundary lines will define the table corners.

#### 3.2 Homography and Minimap Coordinates

The four detected table corners will be mapped to a fixed top-view rectangle using cv::getPerspectiveTransform. This homography will convert ball centres and pocket centres from image space into minimap coordinates. It will also make trajectory drawing independent of the camera perspective.

#### 3.3 Ball Detection and Classification

Ball candidates will be detected with cv::HoughCircles restricted to the playing-field mask. The classification step will examine HSV pixels inside each circle: low saturation and high value for the cue ball, low value for the black 8-ball, a dominant saturated hue for solid balls, and a combination of near-white and saturated regions for striped balls.

#### 3.4 Semantic Segmentation

The segmentation mask will be generated using deterministic drawing operations. Pixels outside the detected table will be labelled as background, pixels inside the table will be labelled as playing field, and each detected ball circle will overwrite the mask with its ball-category label. This directly matches the label IDs described in the project brief.

#### 3.5 Tracking and Pocket-Aware Extension

Consecutive detections will be associated using nearest-neighbour matching. Recent positions will be stored to draw trajectories for moving balls. As an additional contribution, the six pocket regions will be inferred from the table geometry. If a ball disappears near a pocket region, it will be marked as pocketed and removed from the active minimap state. If it disappears away from a pocket, it will be treated as an occlusion and kept temporarily at its last known position.

# 4. Assumptions and Robustness Plan

- The camera pose is assumed to remain fixed during each video clip, as allowed in the brief.
- The table boundary will use the visible upper rail/cloth attachment lines, consistent with the example provided by the professor.
- Different table colours will be handled by using configurable HSV ranges and validating the largest plausible table contour.
- Players, cue sticks, and spectators will be rejected where possible through table masking, geometric constraints, and temporal consistency.
- Additional internet or self-recorded videos will only be used for development if their source and annotation format are clearly documented in the final report.

### 5. Performance Measurement

The evaluation will follow the metrics specified in the project brief. The provided ground truth will be used only for evaluation, not as input to the algorithm.

|Output | Metric How it will be reported |
|----------------------------- | ----------------------------------------------- |
|Ball localisation | mAP at IoU threshold 0.5 |
|Segmentation | mIoU averaged over background, cue ball, 8- |
|2D minimap and trajectories | Qualitative comparison with the visible final |

The total estimated effort is approximately 100 person-hours. The final report will clearly identify each member's contribution in ideas, implementation, testing, and performance measurement, as requested in the project brief.

# 7. Development Milestones

|Milestone | Focus | Expected output |
|----------- | ------------------------------------------- | ------------------------------------------------- |
|1 | Table boundary and homography | Stable playing-field corners and top-view |
|2 | Ball detection, classification, and masks | Bounding boxes, class labels, and |
|3 | Tracking and minimap overlay | Ball trajectories, pocket-aware active state, |
|4 | Evaluation and reporting | mAP, mIoU, qualitative figures, error analysis, |

## 8. Planned Delivery

- C++ source code using OpenCV only, with one main author identified in each source file header.
- CMake configuration files and build instructions tested in the Virtual Lab environment.
- A final report with the proposed method, implementation details, quantitative metrics, qualitative output images, and error analysis.
- Output images for every benchmark frame pair, including bounding boxes and segmentation masks.
- Output videos for all benchmark clips with the 2D top-view minimap superimposed on the input video.
- A clear statement that the delivered code was written by the group members and does not include code generated by ChatGPT or similar tools.