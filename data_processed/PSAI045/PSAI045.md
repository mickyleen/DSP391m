## Trang 1

Computer Vision Final Project Proposal | Vishesh Goyal and Himashi Bogahawaththa
COMPUTER VISION
Sport Video Analysis for Billiard Matches
Final Project Proposal
Group members: Vishesh Goyal and Himashi Bogahawaththa
1. Introduction
This proposal follows the final project brief for sport video analysis of Eight Ball billiard matches. The goal is to design a computer 
vision system that processes billiard video clips frame by frame and produces high-level information about the match state, 
including ball positions, ball categories, the playing-field area, and a 2D top-view minimap.
Our solution will be implemented in C++ with OpenCV and will use classical image-processing techniques rather than deep 
learning. The proposed system is intended to be robust across the provided benchmark clips, which differ in camera 
perspective, number of visible balls, and pool-table colour.
Project scope Classical computer vision system for analysing Eight Ball billiard 
videos frame by frame.
Implementation constraint C++ and OpenCV only; no deep learning models or external detector 
code.
Main outputs Ball localisation/classification, playing-field boundary detection, 
semantic segmentation, and 2D top-view minimap.
Proposed extension Pocket-aware game-state tracking that removes balls from the 
minimap when they are detected as pocketed.
Evaluation dataset The 10 provided benchmark clips and the annotated first/last frames 
supplied with the project brief.
2. Required System Outputs
Task Required output Planned implementation
Ball recognition and localisation Detect all balls and assign category IDs: cue 
ball, 8-ball, solid, or striped.
Hough circle detection inside the table mask, 
followed by HSV colour analysis.
Playing-field boundary detection Detect the main lines delimiting the billiard 
playing field.
HSV cloth isolation, contour filtering, Canny 
edges, Hough lines, and line intersections.
Semantic segmentation Generate a mask for background, cue ball, 8-
ball, solid, striped, and playing field.
Layered OpenCV masks: background first, 
playing field second, ball classes last.
2D top-view minimap Display ball positions and trajectories in a 
top-view representation for each frame.
Homography projection from image 
coordinates to a canonical table map with 
trajectory polylines.

---

## Trang 2

Computer Vision Final Project Proposal | Vishesh Goyal and Himashi Bogahawaththa
3. Proposed Methodology
3.1 Playing Field Detection
For each clip, the table area will be detected from the first frame and reused for the remaining frames, following the project 
simplification that the camera pose does not change within a single video. The cloth region will be isolated through HSV 
thresholding and contour filtering. The upper rail edges will then be estimated using Canny edge detection and the Probabilistic 
Hough Transform. Intersections of the four selected boundary lines will define the table corners.
3.2 Homography and Minimap Coordinates
The four detected table corners will be mapped to a fixed top-view rectangle using cv::getPerspectiveTransform. This 
homography will convert ball centres and pocket centres from image space into minimap coordinates. It will also make 
trajectory drawing independent of the camera perspective.
3.3 Ball Detection and Classification
Ball candidates will be detected with cv::HoughCircles restricted to the playing-field mask. The classification step will examine 
HSV pixels inside each circle: low saturation and high value for the cue ball, low value for the black 8-ball, a dominant saturated 
hue for solid balls, and a combination of near-white and saturated regions for striped balls.
3.4 Semantic Segmentation
The segmentation mask will be generated using deterministic drawing operations. Pixels outside the detected table will be 
labelled as background, pixels inside the table will be labelled as playing field, and each detected ball circle will overwrite the 
mask with its ball-category label. This directly matches the label IDs described in the project brief.
3.5 Tracking and Pocket-Aware Extension
Consecutive detections will be associated using nearest-neighbour matching. Recent positions will be stored to draw 
trajectories for moving balls. As an additional contribution, the six pocket regions will be inferred from the table geometry. If a 
ball disappears near a pocket region, it will be marked as pocketed and removed from the active minimap state. If it disappears 
away from a pocket, it will be treated as an occlusion and kept temporarily at its last known position.
4. Assumptions and Robustness Plan
• The camera pose is assumed to remain fixed during each video clip, as allowed in the brief.
• The table boundary will use the visible upper rail/cloth attachment lines, consistent with the example provided by the 
professor.
• Different table colours will be handled by using configurable HSV ranges and validating the largest plausible table contour.
• Players, cue sticks, and spectators will be rejected where possible through table masking, geometric constraints, and 
temporal consistency.
• Additional internet or self-recorded videos will only be used for development if their source and annotation format are 
clearly documented in the final report.
5. Performance Measurement
The evaluation will follow the metrics specified in the project brief. The provided ground truth will be used only for evaluation, not 
as input to the algorithm.
Output Metric How it will be reported
Ball localisation mAP at IoU threshold 0.5
Per-video results for frame_first.png and 
frame_last.png, with bounding-box 
visualisations.
Segmentation mIoU averaged over background, cue ball, 8-
ball, solid, striped, and playing field
Per-class IoU and average mIoU, with 
predicted masks shown beside the input 
frames.
2D minimap and trajectories Qualitative comparison with the visible final 
game state
Final minimap for each clip, including ball 
positions, movement trajectories, and 
pocketed-ball state where applicable.

---

## Trang 3

Computer Vision Final Project Proposal | Vishesh Goyal and Himashi Bogahawaththa
6. Work Division and Estimated Hours
Member Main contribution Estimated hours
Vishesh Goyal
Playing-field detection, boundary-line 
selection, homography, pocket geometry, 
and minimap rendering.
35 h
Himashi Bogahawaththa
Ball detection, HSV classification rules, 
semantic segmentation, tracking logic, and 
pocket-aware state update.
35 h
Both members
Integration, CMake configuration, benchmark 
runs, result tables, report writing, and final 
video generation.
15 h each
The total estimated effort is approximately 100 person-hours. The final report will clearly identify each member's contribution in 
ideas, implementation, testing, and performance measurement, as requested in the project brief.
7. Development Milestones
Milestone Focus Expected output
1 Table boundary and homography Stable playing-field corners and top-view 
mapping for each clip.
2 Ball detection, classification, and masks Bounding boxes, class labels, and 
segmentation masks for benchmark frames.
3 Tracking and minimap overlay Ball trajectories, pocket-aware active state, 
and output videos with minimap.
4 Evaluation and reporting mAP, mIoU, qualitative figures, error analysis, 
and final report content.
8. Planned Delivery
• C++ source code using OpenCV only, with one main author identified in each source file header.
• CMake configuration files and build instructions tested in the Virtual Lab environment.
• A final report with the proposed method, implementation details, quantitative metrics, qualitative output images, and error 
analysis.
• Output images for every benchmark frame pair, including bounding boxes and segmentation masks.
• Output videos for all benchmark clips with the 2D top-view minimap superimposed on the input video.
• A clear statement that the delivered code was written by the group members and does not include code generated by 
ChatGPT or similar tools.
