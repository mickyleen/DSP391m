# **DART-SCALE-CODEC**

This document is referenced in the terms and conditions and therefore needs to contain all the required [information.](https://github.com/w3f/Open-Grants-Program/blob/master/README_2.md) Don't remove any of the mandatory parts presented in bold letters or as headlines! See the Open Grants Program Process on how to submit a proposal.

**Proposer:** [NBLTrust](https://github.com/nbltrust) **Payment Address:** 1LcdMwwiG1Vt8UmMqUk1RLAd2MUpbeoyba

## **PROJECT OVERVIEW :PAGE\_FACING\_UP:**

A Dart implementation of the SCALE (Simple Concatenated Aggregate Little-Endian) Codec. We are building a wallet app called **[Jadewallet](https://github.com/w3f/General-Grants-Program/pull/338)** which will support DOT/KSM, this project is a component of it.

**Jadewallet** is making a new paradigm of self-custody, which uses **multi-party computation (MPC)** and **threshold signature scheme (TSS)** technology. **MPC based Threshold Signatures** gives clients total autonomy over whose digital assets and multisignature ability with keyless cryptographic security.

We are building **Jadewallet** with Flutter, although there are Rust, C++ implementations of the SCALE Codec, we think the Dart implementation is the first choice. And we hope the project will also help the Polkadot developer community.

# **TEAM :BUSTS\_IN\_SILHOUETTE:**

#### **TEAM MEMBERS**

Alex Xu Hilbert Zhou

#### **TEAM WEBSITE**

https://www.nbltrust.com/#/en/team

#### **LEGAL STRUCTURE**

Tuolian (Shanghai) Co., Ltd.

#### **TEAM'S EXPERIENCE**

Alex Xu: Co-Founder and CTO in NBLTrust for 4 years, core developer in our three custody products. IT Consultant in IBM for 9 years. **Polkadot Ambassador China**. Worked as TA in two training courses hold by Parity in China. Hilbert Zhou: 2 years ops experience on AIX, websphere and Power. 7+ years backend service development experience including HFT, CTA and blockchain.

Founded in 2017 and headquartered in Shanghai, China, Tuolian(Shanghai) Co., Ltd. is a high-tech company specializing in the field of digital asset custody.

Tuolian has secure custody softwares based on self-developed high-strength classical cryptographic algorithm, hot & cold wallet and hardware wallet products that meet the bank's security level requirements, to provide overall solutions and related technical services for digital asset custody.

Tuolian provides a full range of custody services for well-known companies or organizations such as Math Wallet and HashQuark.

#### **TEAM CODE REPOS**

https://github.com/nbltrust https://github.com/alexxuyang

# **DEVELOPMENT ROADMAP :NUT\_AND\_BOLT:**

**Total Estimated Duration:** 1 month **Full-time equivalent (FTE):** 1.5 **Total Costs:** 0.85 BTC.

#### **MILESTONE 1 — DART IMPLEMENTATION**

**Estimated Duration:** 1 month **FTE:** 1.5 **Costs:** 0.85 BTC

|     | Number |               | Deliverable | Specification                         |
|-----|--------|---------------|-------------|---------------------------------------|
| 0a. |        | License       |             | Apache 2.0                            |
| 0b. |        | Documentation |             |                                       |
|     |        |               |             | Delivering document in dart supported |
|     |        |               |             | format, and publish the package to    |

| 0c. Testing Guide           |             |             |                    |              |
|-----------------------------|-------------|-------------|--------------------|--------------|
| Delivering                  | Unit        | tests.      |                    |              |
| Delivering                  | an          | example     | of fetching        | and          |
| analyzing                   | binary      | metadata    |                    | from chain’s |
| Delivering                  | an          | example     | of sending         |              |
| extrinsics                  | to          | substrate   | based              | chain.       |
| 1. Implementing the Library |             |             |                    |              |
| Delivering                  | a           | library     | that               | support      |
| converting                  | between     |             | object/json/binary | of           |
| following                   | types:      | MetadataV11 |                    | & 12, u8,    |
| u16, u32,                   | u64,        | u256,       | bool,              | fixed length |
| array,                      | dynamic     | length      | array,             | bytes,       |
| address,                    | String,     | Compact,    |                    | Hash256,     |
| Balance,                    | Extrinsic,  |             | Generalized        |              |
| structure,                  | Generalized |             | Enum               |              |

### **FUTURE PLANS**

We are planning to make our dart-substrate-sdk open source.

## **ADDITIONAL INFORMATION :HEAVY\_PLUS\_SIGN:**

**ARE THERE ARE ANY TEAMS WHO HAVE ALREADY CONTRIBUTED (FINANCIALLY) TO THE PROJECT?**

No.

#### **HAVE YOU APPLIED FOR OTHER GRANTS SO FAR?**

**[Jadewallet](https://github.com/w3f/General-Grants-Program/pull/338)**