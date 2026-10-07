# POLKADOT CONFORMANCE TESTS POC

## PROJECT OVERVIEW :PAGE_FACING_UP:

This grant application falls under this RFP and it aims to develop a comprehensive test suite dedicated to assessing the compliance of Host implementations against the official Polkadot Protocol Specification.

#### OVERVIEW

The reliability and security of the Polkadot network are fundamentally contingent upon the flawless implementation of Hosts/Nodes. At present, Substrate and Smoldot (implemented in Rust) are actively used in production, while Gossamer (in Go) and Kagome (in C++) are undergoing advanced stages of development. Our primary objective is to develop a comprehensive test suite dedicated to assessing the compliance of Host implementations against the official Polkadot Protocol Specification.

#### PROJECT DETAILS

Our objective will consist of developing a proof of concept for a test suite that can be run across various host implementations and executors.

In this initial phase, we will concentrate on a few different points:

Host API: cryptography primitives Trie proof verification Scale encoding and decoding

The objective is to ensure conformance with the existing specifications and highlight possible deviations. Moreover, we will organize the PoC in such a way that conformance reports can be generated after each run.

#### Technology and Languages

We aim to develop this in Python or Typescript. We will investigate but at the moment, we see a much wider ecosystem in Python.

Althoug previous work on this area has been developed in Julia, Python holds several advantages over Julia due to its extensive ecosystem, wide community support, and versatility.

Python is also known for its cross-platform compatibility, facilitating the development of cross-platform applications. Its ease of integration with other languages like C/C++ and Java enables the creation of applications with mixed-language components.

There is some previous work that has been done here in Julia we plan to re-use some part of this work, rewrite it, updated it and confront it against current specification since his code has not been updated since February 2023.

#### ECOSYSTEM FIT

Zondax is a growing and distributed team with experience and projects for more than 50 blockchains. Zondax has been contributing to the Substrate ecosystem since 2018-2019. The team has received and completed a large number of W3F grants and currently maintains most Ledger apps for the ecosystem. We have recently completed a grant on the research of an alternative host implementation.

## TEAM :BUSTS_IN_SILHOUETTE:

## TEAM MEMBERS

2 x Engineers 1 x Project Manager

## CONTACT

Contact Name: Juan Leni and Ainhoa Aldave Contact Email: juan.leni@zondax.ch / ainhoa.aldave@zondax.ch Website: zondax.ch

## LEGAL STRUCTURE

Over the last few years, Zondax has been involved in a large number of projects for most of the key players in the blockchain industry. Our team includes experts in most blockchain aspects, from cryptography to data and protocol engineering.

### TEAM CODE REPOS

Most of our contributions to the blockchain ecosystem can be found in our GitHub organization zondax

## DEVELOPMENT STATUS :OPEN_BOOK:

Not initiated.

## DEVELOPMENT ROADMAP :NUT_AND_BOLT:

## TECHNICAL SCOPE:

The scope of our work will consist on:

Review of specifications and conformance tests: The Polkadot specification and the corresponding conformance tests will be used as a reference of expected valid behavior: Polkadot Spec Polkadot tests Analysis of previous work: previous work will be analysed to determine improvements, advantages and disadvantages. In this respect, we can already pinpoint the following repositories: Polkadot Tests PVF Conformance Testing Suite Zombienet SCALE Codec Encoding State Trie Hashing Test the test-suite against all implementations Go: gossamer by ChainSafe C++: kagome by Soramitsu Rust: polkadot by Parity Rust: smoldot by Parity

#### OVERVIEW

Total estimated workload: 4 weeks Delivery time:: 6 to 8 weeks Full-Time Equivalent (FTE): 2.5 FTE Total Costs: 28'800 DAI

## MILESTONE 1 - POC IMPLEMENTATION

Estimated workload: 4 working weeks Delivery time:: 6 to 8 weeks FTE: 2,5 Costs: 28'800 DAI

|Number | Deliverable | Specification |
|-------- | --------------------------- | ------------------------------------------------------- |
|0a. | License | Apache 2.0 / GPLv3 / MIT |
|0b. | Documentation |  |
| |  | We will provide a inline documentation of the code |
| |  | and inline documentation of the code and a basic |
|0c. | Testing and Testing Guide |  |
| |  | Core functions will be fully covered by comprehensive |
| |  | unit tests to ensure functionality and robustness. In |
| |  | the guide, we will describe how to run these tests. |
|0d. | Docker |  |
| |  | We will provide a Dockerfile(s) that can be used to |
| |  | test all the functionality delivered with this |
|0e. | Article |  |
| |  | We will publish an article explaining the research, |
| |  | design decisions and proof of concept |
|1. | PoC code | General structure |
|2a. | Code | PoC Tests: Host API: cryptography primitives |
|2b. | Code | PoC Tests: Trie proof verification |
|2c. | Code | PoC Tests: Scale encoding and decoding |

Zondax has been contributing to the Polkadot ecosystem for several years, and has succesfully completed several grants. We have recently completed a grant on the research of an alternative host implementation. https://github.com/w3f/Grants-Program/pull/1324