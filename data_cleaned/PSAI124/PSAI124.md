# RFP PROPOSAL: SOLIDITY LIBRARIES AND PRE-COMPILES FOR FEVM SMART CONTRACTS

to RFP: https://github.com/filecoin-project/devgrants/pull/898

RFP Category: devtools-libraries

## PROJECT DESCRIPTION

In the context of the FVM Early Builder program (Solidity edition), we propose to build a set of tools and libraries to enable Ethereum developers to re-use their existing know-how to develop Filecoin-specific use cases.

The first goal, which we have defined as Milestone 1 would consist of a feasibility analysis to evaluate if it is worth it to serialize and deserialize data in solidity.

If the evaluation is successful we would like to continue working on this project, otherwise, a different approach should be investigated.

## DEVELOPMENT ROADMAP

MILESTONE 1 - RESEARCH AND FEASIBILITY ANALYSIS OF CBOR IN SOLIDITY IN TERMS OF FVM GAS USAGE

Assumptions/ Pre-requirements

Access to tutorials and existing documentation for the integration is provided. Access to async agile communication in the FVM Slack Channel.

Technical Scope and Timeline

#### Week 1: Ramp-up into FEVM

During the first week we will go through the existing tutorials and documentation, we will identify the gaps that exist to improve this documentation for other developers.

Set up a FEVM running environment Investigate how to deploy a Solidity Smart Contract in the FVM environment.

#### Weeks 2-3 The deep dive into Solidity

Implementation of a smart-contract in solidity that serialises and deserializes data in CBOR including complex types like structs and lists. Benchmarking of gas efficiency. Short documentation and preparation of the results for the demo

## DELIVERABLES

Smart Contract of the PoC capable of serialising and deserializing data in CBOR. Short Documentation (Readme file). Results of the Benchmark.

### TEAM MEMBERS

1.5 FTE

Technical Leader Engineer 1 Support Engineer Management POC

### ESTIMATED MILESTONE DELIVERY

|Milestone | No. |  | Milestone Summary & Staffing |  | Funding |  | Estimated Timeframe |
|----------- | ----- | --------- | --------------------------------- | ----- | -------------- | ---------- | ------------------------- |
| |  | Results | of feasibility analysis for the | use |  |  |  |
| |  | of CBOR | in Solidity in terms of FVM gas |  |  |  |  |
| |  |  |  |  | 28.400,00 \$ | Delivery | Mid-Late September 2022 |

#### MAINTENANCE AND UPGRADE PLANS

If the research analysis from Milestone 1 provides good results in terms of feasibility for this approach, we would like to continue this project, with Milestone 2, focusing around the Implementation CBOR serde for the common Filecoin data types (Address, Actor ID, Sector Number, etc. – a lot of this is inside fvm_shared) and later a Milestone 3 consisting in the implementation of the actual library. Otherwise, the work around this approach will stop and other approaches should be investigated.

## TEAM

#### CONTACT INFO

This has been shared per Email.

#### TEAM MEMBERS

Team Member 1:
- Emmanue Murano Team Member 2
- Lola Rigaut-Luczak Team Member 3
- Ainhoa Aldave

#### TEAM WEBSITE

https://zondax.ch/

#### RELEVANT EXPERIENCE

We have taken par of the FVM Early Builders program and recently delivered an SDK for FVM in Assmblyscript. https://github.com/Zondax/fvm-as-sdk

We have been collaborating with PL for several years and have/or are currently contributing to the following projects: Signing Tools (WASM/Typescript and FFI support, Secp256k1 and BLS support) Filecoin Indexing, Filecoin GPU Scheduler, Exchanges & Custodian technical support among others.

#### TEAM CODE REPOSITORIES

https://github.com/Zondax/