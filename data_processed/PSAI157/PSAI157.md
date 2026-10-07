# Google Summer of Code project proposal 2025 - OSIPI

## Contact details

Full name: Ibrahim Abdelazim

Country: Germany

Time zone: GMT+1

Email: ibrahim.abdelazim@fau.de

GitHub ID: 1brahimmohamed

Personal blog: www.ibrahim-abdelazim.de

LinkedIn: https://linkedin.com/in/1brahimmohamed

## GSOC information

### Have you participated in the Google Summer of Code previously?

No, this will be my first time participating in GSoC. However, I have experience contributing to open-source projects, particularly in medical imaging, such as working with OHIF during my internship at Neureveal Inc.

Are you applying to any other organizations this year?

No, my primary focus is on OSIPI because its work aligns closely with my medical imaging and software engineering background.

How many hours will you devote to your GSoC project each week? Do you have any other commitments during the summer?

I plan to dedicate around 20 hours per week to my GSoC project as I have a part-time working student job that requires 15 hours/week.

Did you contribute to OSIPI during the application period?

No, but I have been reviewing OSIPI's repositories, documentation, and past GSoC Contributions

What skills or knowledge do you think you are missing before you are able to participate in OSIPI and how will you deal with this (it is ok to not know everything up front!)?

I have a solid foundation in Python, JavaScript, software engineering, web development, and medical imaging including DICOM, NIfTI, and BIDS. even I know and studied MRI Physics and MRI pulse sequences. However, I am new to the acquisition parameters of ASL MRI. To bridge this gap, I will:

- 1. Read relevant literature on ASL MRI to understand it more
- 2. Discuss with the mentors and community to understand best practices for extracting and reporting MRI parameters.

I have started this already. I am a fast learner and have successfully picked up new technologies in past projects, so I am confident in my ability to adapt. This is not a big deviation from my current experience as I develop cardiac MRI solutions at Siemens Healthineers.

How do you plan to interact with your mentors?

I plan to maintain regular communication with my mentors via their preferred way of communication but for me, I prefer slack, discord, and meetings so I am planning to do:

- 1. Weekly or bi-weekly check-ins to discuss progress, roadblocks, and next steps.
- 2. Document my work clearly so mentors can review and provide feedback efficiently.

## Project Idea

Title of the idea that you are interested in

Methods section generator for ASL

Brief description of the idea.

The goal of this project is to develop a Python-based tool that extracts acquisition parameters from ASL MRI images (BIDS/NIfTI and DICOM formats) and automatically generates a standardized methods section for scientific publications. This will enhance transparency and reproducibility in MRI research by ensuring accurate and consistent reporting of acquisition details. The tool will handle missing parameters interactively, improve DICOM metadata extraction, and enhance modularity for future extensions.

Have you worked on a similar project in the past? If yes, please provide a brief description (with links if possible)

Yes, I have worked on projects related to medical imaging and structured data extraction:

- 1. Cloud-Based Medical Imaging Platform: For my BSc. graduation project, I developed a web-based medical imaging platform for AIbased brain tumor segmentation and MRI motion artifact correction, supporting DICOM and NIfTI formats. The backend followed a microservices architecture, utilizing DICOMweb for communication and BIDS standards for structured data representation. We designed a custom NIfTI storage service, similar to a PACS but specifically for NIfTI files, built on BIDS using FastAPI. The system also included an API gateway using Django for load balancing, caching, and reverse proxy. The frontend was developed with React and TypeScript. We used to extract metadata in the backend for inference and for the frontend using Cornerstone3D for medical image visualization.
- 2. OHIF Viewer Contribution: During my internship at Neurveal, I contributed to OHIF (Open Health Imaging Foundation), a medical imaging viewer that supports DICOM and research-oriented image visualization for their internal usage

Have you examples of previous GitHub or Python contributions?

<https://github.com/1brahimmohamed/Brain-Tumor-Segmentation-GP> (Gateway, Nifti Storage Services)

<https://github.com/1brahimmohamed/Function-Plotter>

<https://github.com/1brahimmohamed/Digital-Filters-Design-Suite>

[https://github.com/1brahimmohamed/Images-Phase-Magnitude-](https://github.com/1brahimmohamed/Images-Phase-Magnitude-Mixer)[Mixer](https://github.com/1brahimmohamed/Images-Phase-Magnitude-Mixer)

#### How are your previous experiences useful in your contribution to OSIPI?

My previous experiences have equipped me with the necessary skills to contribute effectively to OSIPI. My work with DICOM, NIfTI, and BIDS will help in extracting and structuring acquisition parameters for ASL MRI data, I have built backend and frontend tools for handling medical imaging metadata, which is directly relevant to developing and improving the OSIPI tool. My contributions to OHIF and other projects have prepared me to work in a structured, community-driven development environment like OSIPI. Additionally, my role as a

Working Student at Siemens Healthineers has further strengthened my expertise, as I develop Cardiac MR solutions using Python and TypeScript, enhancing my understanding of MRI data processing, and medical imaging standards.

#### How will your project benefit OSIPI

- 1. The tool will help researchers automatically generate accurate, standardized acquisition reports, reducing errors and manual effort.
- 2. Expanding the DICOM module will make the tool more versatile and useful across different ASL MRI datasets.
- 3. Adding an interactive system for missing parameters will improve usability and adoption in the research community.
- 4. Making the tool more modular will allow future extensions to DSC/DCE/IVIM sequences, broadening its impact beyond ASL.
- 5. I aim to strengthen the OSIPI open-source medical imaging ecosystem and support the broader MRI research community.

### Project plan (max 750 words)

Approach:

Project timeline:

| # | Phase                                 | Duration (Weeks) | Week  |
|---|---------------------------------------|------------------|-------|
| 1 | Investigation & Requirements Analysis | 2                | 1 - 2 |
| 2 | Design and Prototyping                | 1                | 3     |
| 3 | Core Development                      | 3                | 4 - 6 |
| 4 | Integration & System Testing          | 1                | 7     |
| 5 | Documentation & Reporting             | 1                | 8     |
| 6 | Final Testing                         | 1                | 9     |

#### Milestones:

| Phase |           |    |                                                                                         |
|-------|-----------|----|-----------------------------------------------------------------------------------------|
| 1     | Tasks     | 1. | Explore the current OSIPI codebase, documentation (OSIPI                                |
|       |           | 2. | Identify gaps in existing DICOM and BIDS handling,                                      |
|       |           | 3. | Schedule an initial meeting with mentors to clarify project resources.                  |
|       | Milestone | ●  | Deliver a comprehensive requirements document and an                                    |
|       |           |    | initial architectural diagram outlining the planned improvements.                       |
| 2     | Tasks     | 1. | Develop a detailed design for a modular architecture that                               |
|       |           | 2. | Create wireframes and user flow diagrams to visualize the                               |
|       |           | 3. | Prototype a critical module for DICOM metadata extraction, private tags.                |
|       | Milestone | ●  | Finalize the design document and produce functional                                     |
| 3     | Tasks     | 1. | Implement an interactive interface that prompts users to input                          |
|       |           | 2. | Expand and refine the DICOM metadata extraction module to consistency.                  |
|       |           | 3. | Develop and integrate a comprehensive testing suite that verified reference reports.    |
|       | Milestone | ●  | Achieve a working version of the tool that incorporates the                             |
| 4     | Tasks     | 1. | Integrate all new modules and features into a cohesive system.                          |
|       |           | 2. | Conduct extensive unit tests and integration tests to verify                            |
|       |           | 3. | Optimize system performance and resolve any integration issues.                         |
|       |           | 4. | Share the prototype tool with TF4.1 members for beta testing tool before final release. |

|   | Milestone | ●  | Deliver a fully integrated tool that passes preliminary system |
|---|-----------|----|----------------------------------------------------------------|
| 5 | Tasks     | 1. | Prepare detailed user documentation, technical guides for      |
|   |           | 2. | Refine and polish the codebase based on testing feedback,      |
|   |           | 3. | Draft a final report that details the project’s methodology,   |
|   | Milestone | ●  | Deliver a beta-tested version of the tool with improvements    |
|   |           | ●  | Complete comprehensive documentation and finalize a            |
| 6 | Tasks     | 1. | Conduct final rounds of testing to address any remaining       |
|   |           | 2. | Prepare demonstration materials, such as a walkthrough         |
|   |           | 3. | Perform final performance optimizations and verify the overall |
|   | Milestone | ●  | Finalize the tool and demonstration package, ensuring the      |