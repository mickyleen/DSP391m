# **Classical Mechanics: Implement Wrapping Geometry and Pathways for Musculoskeletal Modeling**

![](images/_page_0_Picture_1.jpeg)


## **Table of Contents**

- 1. Me the person 1.1. Personal Details 1.2. My Introduction
- 2. Me the programmer 2.1. Math and CS background 2.2. Why I chose to go for Sympy 2.3. My Contributions to Sympy
- 3. Me and my project 3.1. Overview 3.2. Project Phases 3.3. Project Timeline 3.4. My commitment to this project
- 4. References

## **Me the person**

### **Personal Details**

- Full name: Rushabh Mehta
- Primary Email: [mehtarushabh2005@gmail.com](mailto:mehtarushabh2005@gmail.com)
- College Email: [rbmehta\\_b23@ce.vjti.ac.in](mailto:rbmehta_b23@ce.vjti.ac.in)
- Github: [RushabhMehta2005](https://github.com/RushabhMehta2005)
- LinkedIn: [mehtarushabh2005](https://www.linkedin.com/in/mehtarushabh2005/)
- University: Veermata Jijabai Technological Institute (VJTI), Mumbai
- Degree: Computer Engineering
- Minor: Signal and Image Processing
- Country: India
- Location: Mumbai
- Timezone: Indian Standard Time (IST) (UTC + 5:30)
- Language of Communication: English

### **My Introduction**

Hello, myself Rushabh Mehta, a second year computer engineering student at Veermata Jijabai Technological Institute (VJTI), Mumbai. Regarded as one of the finest engineering institutions in the country, to get enrolled in its programs, you must qualify entrance exams like JEE and MHT-CET, in which millions of students appear and are tested heavily on math, physics and chemistry.

In my spare time I enjoy reading non-fiction stories, solving puzzles of any kind and keeping up to speed with the latest advancements in STEM.

During my 2 years in university, I have participated in various coding competitions and organised various events, mentored juniors in their journey and helped my peers grow along with me. I have good communication and written communication skills. I speak English fluently.

## **Me the Programmer**

### **Math and CS background**

Mathematics has always been my forte, and it forms the basis for the study of core computer science subjects like computational theory, algorithms and much more.

My first programming language was C. I appreciated the low level control over the CPU that the language gave but I preferred faster development and dynamic typing more, thus I learnt Python and have been programming in it for 2.5+ years in it at the moment of writing.

I use Visual Studio Code as my IDE. It has all the features I need built into it making my experience seamless, and Windows 11 as my operating system which serves my needs. I have experience with Git and Github as I use both frequently for my contributions to Sympy and for my personal projects.

A small project that I wish to share here is my (in-progress) attempt at creating a python package for the subject of [Theory of Computation.](https://en.wikipedia.org/wiki/Theory_of_computation) What attracted me towards the idea was the simplistic nature of the models of computation and the algorithmic aspects of the course. It felt intuitive and fun to implement automata in an object oriented fashion. [Link here.](https://github.com/RushabhMehta2005/theory-of-computation/)

Coming back to why I am suited for this project, I have a strong background in physics due to my JEE preparation. Newton's Laws of Motion, Forces, Rotation and Torques were parts of the core curriculum and I am proficient in these concepts. I am also well versed in geometry, paths and curves from my engineering math courses, the concepts of which will be useful to us.

The relevant college courses I have taken are:

- **Engineering Mathematics 1 and 2**
- **Engineering Mechanics**
- Discrete Mathematics
- Data Structures
- Design and Analysis of Algorithms
- Computer Programming and Problem Solving
- **Python Programming Lab**

Now let's talk about Sympy, a tool which I liked after mere minutes of discovering it! Sympy combines my love for math and computer science and turns it into a Python package. My favourite feature by far is the "integrate()" function. The integration operation is the most daunting topic in math. Whether you're good at it or not is a matter of practicing problems and developing an intuition for its methods. But Sympy distills that down into a single function using powerful and carefully implemented algorithms.

**Example problem from JEE exam math section:**

Figure 1: (Try doing this by hand)

#### **But in Sympy,**

Figure 2: The integrate API

It is merely a matter of writing out your integrand function now. This shows the power of symbolic computation and the advantage of using a library like Sympy.

### **Why I chose to go for Sympy**

As expressed already, I am fascinated by Sympy and wish to contribute to it, and improve it for its users. It is a well maintained and respected open source project. It will give me real world software development and engineering experience. The community was extremely welcoming for a new contributor like me, which drew me more towards it. Sympy is widely used by researchers, students and educators all around the globe.

#### **My Contributions to Sympy**

I have been contributing to Sympy for about 4-5 months now. I have learnt the open source workflow for Sympy and have gained a general understanding of the codebase.

- (**Merged**) [#27228](https://github.com/sympy/sympy/pull/27228) Solved the issue where the wigner\_3j function in sympy.physics was violating behavioral subtyping with numpy floats.
- (**Merged**) [#27288](https://github.com/sympy/sympy/pull/27288) Solved a similar issue which arose in both the wigner\_6j and wigner\_9j functions.
- (**Merged**) [#27347](https://github.com/sympy/sympy/pull/27347) Implemented the expectation method of the PoissonDistribution class to quickly return the correct expected value of the distribution, thus solving the issue.
- (**Merged**) [#27414](https://github.com/sympy/sympy/pull/27414) Added tests for the Quaternion.integrate() method, removed the TODO.
- (**Merged**) [#27789](https://github.com/sympy/sympy/pull/27789) Fixed an incorrect type annotation in sympy.mechanics docs.
- (**Closed**) [#27286](https://github.com/sympy/sympy/pull/27286) Implemented is\_kth\_power\_free and kth\_power\_free\_range functions which utilized factorint function to check and obtain k-th power free numbers easily.
- (**Closed**) [#27574](https://github.com/sympy/sympy/pull/27574) Tried to extend the double factorial function for complex arguments.
- (**Open**) [#27384](https://github.com/sympy/sympy/pull/27384) Added support for symbolic multiplication of scalar multiplication of waves.
- (**Open**) [#27831](https://github.com/sympy/sympy/pull/27831) Added a neccessary check in geodesic\_end\_vectors method in sympy.mechanics.
- Raised issue [#27610](https://github.com/sympy/sympy/issues/27610) regarding the ask function returning unexpected output on the input I\*oo. It was then resolved.

## **Me and my project**

Now I will describe the project. **This is intended to be a 175 hour project.**

#### **Overview**

A wrapping geometry specifies the path along which a force acts. For example, if the wrapping geometry is a sphere, it can model the behavior of a force that follows a spherical path between two points. This is particularly useful in biomechanics, where muscles and tendons often wrap around bones or joints. The geometric representation of these paths directly influences the magnitude and direction of the force, making accurate modeling essential for realistic simulations of musculoskeletal interactions.

According to the principle of least action, when a force travels between two points on a surface, it always follows the **shortest possible path**. These shortest paths are known as **geodesics**. For simple geometries such as spheres or cylinders, closed-form solutions for geodesics exist. However, for more complex surfaces like ellipsoids, cones, and toroids, closed form solutions are either challenging or not available at all. This represents the major problem I will try to solve with this project.

One of the most popular tools currently in use for biomechanical modeling is Open-Sim, which is a C++ library. It relies on numerical methods such as discretizing complex geometries and computing force pathways by means of numerical integration. We, on the other hand, in Sympy will aim to solve these problems symbolically as much as possible. An approximate but symbolic solution can offer analytical insights as well; this can be immensely useful for biomechanics researchers. This project will add new wrapping geometry objects to Sympy, enabling users to model more involved musculoskeletal interactions for biomechanics research and educational/teaching purposes. I have reviewed contact geometry objects available in OpenSim and what Sympy currently lacks.

I will implement 3 new wrapping geometries in Sympy, namely the **Spheroid**, **Cone** and **Torus**.

## **Project Phases**

### **Phase 1 – Conical Wrapping Geometry (WrappingCone)**

#### **Mathematical Foundations**

A right circular cone is a **developable surface** – it can be flattened onto a plane without distorting distances. This property allows us to derive closed–form expressions for geodesics on the cone by "unfolding" it into a circular sector. Specifically, a point on the cone is described by two coordinates:

- the *slant distance r* from the apex, and
- the angular coordinate *u* (measuring rotation about the cone's axis).

When unfolded, the cone maps isometrically onto a circular sector with:

Radius = *r,* Central angle *γ* = 2*π* sin *θ,*

where *θ* is the cone's half-angle. In the unfolded (plane) setting, we introduce polar coordinates (*r, ϕ*) with the relation:

*ϕ* = *u* sin *θ.*

Given two points *P*<sup>1</sup> and *P*<sup>2</sup> on the cone with coordinates (*r*1*, u*1) and (*r*2*, u*2), their unfolded coordinates become (*r*1*, ϕ*1) and (*r*2*, ϕ*2), where *ϕ<sup>i</sup>* = *u<sup>i</sup>* sin *θ*. In the plane the geodesic is the straight line (chord) connecting these points. By the law of cosines, the geodesic length *L* is

*L* = r *r* 2 <sup>1</sup> + *r* 2 <sup>2</sup> <sup>−</sup> <sup>2</sup> *<sup>r</sup>*<sup>1</sup> *<sup>r</sup>*<sup>2</sup> cos ∆*ϕ ,*

with

∆*ϕ* = *ϕ*<sup>2</sup> − *ϕ*1*.*

For the geodesic end vectors, the procedure is as follows:

- 1. **Unfolded Unit Tangent Calculation:** In the plane, compute the difference vector

∆**v** = *r*<sup>2</sup> − *r*1*, ϕ*<sup>2</sup> − *ϕ*<sup>1</sup>

and normalize it to obtain the unit tangent vector **t**plane = (*tr, tϕ*).

#### 2. **Refolding via the Differential:** The unfolding map

*F* : (*r, u*) 7→ (*r, u* sin *θ*)

has differential

*dF* = 1 0 0 sin *θ* ! *.*

Its inverse,

*dF* <sup>−</sup><sup>1</sup> = 1 0 0 sin *θ* ! *,*

converts the angular component back so that the tangent components in the cone's coordinates become

*tr, t<sup>u</sup>* with *t<sup>u</sup>* = *tϕ* sin *θ .*

- 3. **Push–Forward onto the Embedded Cone:** The cone is embedded in R <sup>3</sup> by the mapping

*<sup>f</sup>*(*r, u*) = *r* sin *θ* cos *u, r* sin *θ* sin *u, r* cos *θ .*

Its partial derivatives are

*∂f ∂r* <sup>=</sup> sin *θ* cos *u,* sin *θ* sin *u,* cos *θ*

and

*∂f ∂u* <sup>=</sup> −*r* sin *θ* sin *u, r* sin *θ* cos *u,* 0 *.*

At each endpoint, the tangent vector is assembled as

**T** = *t<sup>r</sup> ∂f ∂r* <sup>+</sup> *<sup>t</sup><sup>u</sup> ∂f ∂u,*

and then normalized.

#### **Implementation Strategy**

- **Geodesic Length:** Compute the geodesic length between two points *p*1 = (*r*1*, u*1) and *p*2 = (*r*2*, u*2) on the cone by:
  - 1. Converting the angular coordinates with *ϕ<sup>i</sup>* = *u<sup>i</sup>* sin *θ*.
  - 2. Calculating the angular difference ∆*ϕ* = *ϕ*<sup>2</sup> − *ϕ*1.
  - 3. Evaluating the length via

*L* = r *r* 2 <sup>1</sup> + *r* 2 <sup>2</sup> <sup>−</sup> <sup>2</sup> *<sup>r</sup>*<sup>1</sup> *<sup>r</sup>*<sup>2</sup> cos ∆*ϕ .*

- **Tangent Vector Computation:** Determine the geodesic's end tangent vectors as follows:
  - 1. Unfold the points *p*1 and *p*2 to the plane and compute the unit tangent vector along the chord, **t**plane = (*tr, tϕ*).
  - 2. Map the tangent component back to the cone's (*r, u*) coordinates using

*t<sup>u</sup>* = *tϕ* sin *θ .*

- 3. Embed the tangent vector on the cone by computing the partial derivatives from

*<sup>f</sup>*(*r, u*) = *r* sin *θ* cos *u, r* sin *θ* sin *u, r* cos *θ ,*

then forming

**T** = *t<sup>r</sup> ∂f ∂r* <sup>+</sup> *<sup>t</sup><sup>u</sup> ∂f ∂u,*

and normalizing **T** to obtain the unit tangent.

### **Phase 2 – Spheroidal Wrapping Geometry (WrappingEllipsoid)**

#### **Mathematical Foundations**

An ellipsoid of revolution (or spheroid) is given by

*x* <sup>2</sup> + *y* 2 *a* 2 + *z* 2 *b* 2 = 1*,*

where *a* is the equatorial radius and *b* is the polar radius. Two key derived parameters are the *flattening*

*f* = *a* − *b a ,*

and the *eccentricity*

*e* = vuut1 − *b a* !2 *.*

Since there is no simple closed-form for the geodesics on a spheroid, a common strategy is to map the geodetic coordinates to the *auxiliary sphere*. This is done as follows:

- 1. For each point with geodetic latitude *ϕ*, compute the **reduced latitude**

*<sup>β</sup>* = arctan (1 − *f*) tan *ϕ .*

- 2. For two points with reduced latitudes *β*<sup>1</sup> and *β*<sup>2</sup> and longitudes *λ*<sup>1</sup> and *λ*2, the spherical law of cosines on the auxiliary sphere gives the spherical arc length *σ*:

cos *σ* = sin *β*<sup>1</sup> sin *β*<sup>2</sup> + cos *β*<sup>1</sup> cos *β*<sup>2</sup> cos(∆*λ*)*,*

where ∆*λ* = *λ*<sup>2</sup> − *λ*1.

- 3. The geodesic distance *s* on the spheroid is then expressed as a series in the flattening *f*:

*s* ≈ *a A σ* <sup>−</sup> *<sup>B</sup>* sin(2*σ*) + *<sup>C</sup>* sin(4*σ*) − · · · *,*

with coefficients *A*, *B*, *C*, *. . .* easily determined via a series expansion in *f*.

For the tangent (or endpoint) vectors, the local directions at each point are computed from the ellipsoidal coordinate transformation. Specifically, the local north and east unit vectors, **N** and **E**, are derived by differentiating the coordinate mapping. Once the azimuth *α* (the angle between the geodesic and the north direction) is determined, the endpoint tangent vector is given by

**T** = cos *α* **N** + sin *α* **E***.*

#### **Implementation Strategy**

- **Class Structure:** Develop a class WrappingEllipsoid as a subclass of WrappingGeometryBase that stores the ellipsoidal parameters *a* and *b* (or equivalently *a* and *f*).
- **Series Expansion for Geodesic Length:** Implement helper functions using Sympy's symbolic tools to:

- 1. Compute the reduced latitude *β* for any given geodetic latitude *ϕ*.
- 2. Calculate the spherical arc length *σ* on the auxiliary sphere via the spherical law of cosines.
- 3. Expand the geodesic distance *s* as a series in *f*, i.e.,

*s* ≈ *a* [*A σ* − *B* sin(2*σ*) + *C* sin(4*σ*) − · · · ] *,*

where the coefficients *A*, *B*, *C*, *. . .* are determined symbolically.

- **Computation of Tangent Vectors:** Derive the local north (**N**) and east (**E**) vectors by differentiating the ellipsoidal coordinate transformation. Then:
  - 1. Compute the azimuth *α* from the geodetic data.
  - 2. Form the endpoint tangent vector using the relation

**T** = cos *α* **N** + sin *α* **E***.*

## **Phase 3 – Toroidal Wrapping Geometry (WrappingToroid)**

#### **Mathematical Foundations**

A torus is parametrized by

*<sup>x</sup>*(*u, v*) = *R* + *r* cos *v* cos *u, <sup>y</sup>*(*u, v*) = *R* + *r* cos *v* sin *u, z*(*u, v*) = *r* sin *v,*

with *u* ∈ [0*,* 2*π*) and *v* ∈ [0*,* 2*π*). Here, *R* is the major radius (the distance from the center of the tube to the torus center), and *r* is the minor radius (the tube radius).

The first fundamental form, which encodes the metric on the torus, is given by

*ds*<sup>2</sup> = *R* + *r* cos *v* 2 *du*<sup>2</sup> + *r* 2 *dv*<sup>2</sup> *.*

Although a torus is not developable over its entire surface, for a sufficiently small patch (e.g., where the muscle wraps) it is acceptable to locally "unfold" the torus into a planar domain. In this local domain, the geodesic is approximated by a straight line and its length is computed by the Euclidean distance. This computed length is then appropriately scaled to account for the toroidal curvature when mapped back to the surface.

For the tangent (or endpoint) vectors, we derive a local basis from the partial derivatives of the torus parametrization. Analogous to the north–east basis in the ellipsoidal case, these local tangent directions allow us to combine with the computed azimuth to yield the final endpoint unit vectors:

**T** = cos *α* **N** + sin *α* **E***,*

where *α* is the azimuth of the geodesic at the endpoint.

#### **Implementation Strategy**

- **Class Structure:** Develop a class WrappingToroid that extends WrappingGeometryBase and stores the torus parameters *R* and *r*.
- **Point Verification:** Implement a method point\_on\_surface that checks if a given point (*x, y, z*) satisfies the torus equation. For example, by verifying that

 √ *x* <sup>2</sup> + *y* <sup>2</sup> − *R r* !2 + *z r* 2 ≈ 1*.*

- **Geodesic Length Calculation:** Develop geodesic\_length as follows:
  - 1. *Local Unfolding:* Map the two points from their toroidal coordinates (*u, v*) to a planar domain using the standard mapping. For instance, the *u*-coordinate is scaled by the local factor *R* + *r* cos *v* while the *v*-coordinate is retained.
  - 2. *Chord Computation:* Compute the Euclidean chord length in the plane:

*L*planar = q ∆*u* 2 (*R* + *r* cos *v*) <sup>2</sup> + ∆*v* 2 (*r*) 2 *,*

where ∆*u* and ∆*v* are the differences in the toroidal coordinates (with an appropriate handling of periodicity).

- 3. *Scaling Adjustment:* Adjust *L*planar using scaling factors derived from the first fundamental form to obtain the geodesic length *s* on the torus.
- **Endpoint Tangent Vectors:** For geodesic\_end\_vectors:
  - 1. Compute the partial derivatives of the torus parametrization:

*∂f ∂u* <sup>=</sup> − *R* + *r* cos *v* sin *u, R* + *r* cos *v* cos *u,* 0 *, ∂f ∂v* <sup>=</sup> −*r* sin *v* cos *u,* −*r* sin *v* sin *u, r* cos *v .*

- 2. Define the local basis vectors analogous to "north" and "east" using these derivatives.
- 3. Determine the geodesic's azimuth *α* from the unfolded planar mapping.
- 4. Form the endpoint tangent vector as

**T** = cos *α* **N** + sin *α* **E***,*

and normalize **T** to obtain a unit tangent.

## **Project Timeline**

## **Community Bonding Period (May 8 to June 1)**

- Set up my GitHub blog to share my progress publicly.
- Get to know my mentors, establish communication channels, and finalize a regular meeting schedule with them.
- Network with fellow GSoC contributors and review their proposals to better understand diverse projects this year.
- Familiarize myself with the codebase and the overall GSoC ecosystem.
- Engage in preliminary discussions regarding the project scope and initial ideas with my mentors.

## **Weeks 1, 2, and 3 (June 2 to June 23)**

- Focus on Phase 1: WrappingCone (Conical Wrapping Geometry).
- Implement closed-form expressions for the geodesic length and endpoint tangent directions for the cone.
- Implement the WrappingCone class with methods point\_on\_surface, geodesic\_length, and geodesic\_end\_vectors.
- Develop unit tests and detailed documentation for WrappingCone to validate against known cases.

## **Weeks 4, 5, and 6 (June 24 to July 14)**

- If there is any remaining work from Phase 1, finish it in week 4.
- Transition to Phase 2: WrappingEllipsoid (Spheroidal Wrapping Geometry).
- Implement the mathematical derivations for the reduced latitude, spherical arc length *σ*, and series expansion for the geodesic length *s* as a function of *f*.
- Develop local helper functions and integrate them into the WrappingEllipsoid class.
- Begin writing initial tests and comprehensive documentation for WrappingEllipsoid, ensuring consistency with the overall WrappingPathway interface.

## **Weeks 7, 8, and 9 (July 15 to August 4)**

- Finalize tests and documentation for Phase 2.
- Begin Phase 3: WrappingToroid (Toroidal Wrapping Geometry).
- Develop methods to compute local basis vectors from the torus parametrization and derive the endpoint tangent vectors.
- Initiate preliminary testing and draft documentation for WrappingToroid.

## **Weeks 10, 11, 12, and 13 (August 5 to September 1)**

- Finalize testing and documentation for WrappingToroid.
- Integrate and refine all modules, clean up the code, and merge any open pull requests.
- Polish overall documentation to ensure clarity and consistency across all new classes, in compliance with the WrappingPathway interface.
- Submit final evaluations and project deliverables.

## **My Commitment to this project**

- I have end semester examinations till 15th May, after which I will begin my work discussed in the community bonding phase.
- My 5th semester starts near July 14th, but there is a significantly lesser amount of work in the first couple of months of the semester, thus this will not create any hindrance.
- I have no other work or internships during this summer; therefore, I will dedicate my entire time during the day to GSoC.
- I will communicate regularly with my mentors, updating them about my progress.
- I will strive to work as independently as possible, adhering to the proposed timeline. If any unforeseen blockers arise, I will communicate them transparently to my mentors.
- If there are any blockers or unforeseen situations arising, I will communicate them to my mentors with full transparency.
- I am committed to owning the work completed during GSoC, addressing any bugs or issues that arise post-project, and continuing to improve the implementation based on user feedback and emerging needs.

## **References**

- [OpenSim Documentation.](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/overview)
- Vincenty, T. (1975). *Direct and inverse solutions of geodesics on the ellipsoid with application of nested equations.* Survey Review.
- Karney, C. F. F. (2013). *Algorithms for geodesics.* Journal of Geodesy.
- Danielsen, J. (1989). *The area under the geodesic.* Survey Review.
- Standard texts on differential geometry and geodesy, including works by Bessel and Helmert.
- [Sympy Wiki and Documentation.](https://github.com/sympy/sympy/wiki/)
- GSoC 2024 proposals.
- [GSoC 2025 Timeline.](https://developers.google.com/open-source/gsoc/timeline)