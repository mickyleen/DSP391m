# OPEN GRANT PROPOSAL: PROJECT METATRON

# PROJECT DESCRIPTION

Metatron is a generic blockchain-agnostic P2P metadata versioning system. The system provides a way to establish universal ownership of 128-bit random numbers called xid (for eXtensible IDentifier).

Metatron solves the problem of proving prior art by using an xid to track (on a blockchain) the history of multiple content releases represented by IPFS cid hashes.

Content creators can use Metatron to maintain control of their rights of ownership and future revision publishing privileges. Content owners have the unique key that is used to authoritatively publish the original and any future content edition(s). Authorship rights can be transferred or shared using the functionality of the author(s) preferred P2P ledger.

Content consumers can use Metatron to certify authenticity and confirm they are accessing or purchasing the latest authorized version of a piece of digital content. Knowledge of the xid provides a full history of the digital content as published by the original author(s).

#### VALUE

One of our first use-case is in support of a supply chain traceability project called the EDEN Protocol. Metatron provides the "cursor" system that aggregates data signatures as a product travels across the supply-chain through its life-cycle towards an end-customer.

Metatron uses IPFS to store data and capture a hash of the current version. With greater control over their rights of authorship, content creators will want ways to publish and disseminate their content to broader audiences.

Filecoin is a de-facto ideal economic token to facilitate and incentivize content publishing, broadcasting, exchange, etc.

### DELIVERABLES

A grant would provide the resources needed to support the launch of the protocol. Additionally, funding would allow us to design and add an economic layer (ie: filecoin) to the protocol.

Working reference implementation: https://github.com/macterra/metatron. Docker container for easy setup: https://github.com/macterra/metatron-node Try it out yourself: http://btc.metagamer.org:5000/

The project has a community of users who are familiar with the technology and demanding the functionality provided by Metatron. The Ethical Data Alliance has defined its needs in the form of the EDEN Protocol. Metatron provides the foundation system needed to implement the EDEN Protocol.

## DEVELOPMENT ROADMAP

#### SUMMARY:

Weeks 1-8: Release and support v.1.

Weeks 8-12: Support EDA Use Cases and define incentive layer opportunity.

We are requesting funding to put together a small team of 3 individuals at a blended rate of \$50/hr for a period of 3 months. This would allow us to transfer key knowledge from macterra, who can't commit to the project at this time, but has agreed to be available as a technical advisor.

The Metatron protocol will require ongoing support and funding beyond this 3 months roadmap. We would welcome the opportunity to become a closer part of the Filecoin/IPFS ecosystem. These discussions and/or the identification of a sustainable home for the project would occur in parallel to the roadmap below.

#### DETAILS:

Week 1: Finalize v.1 protocol requirements and specifications:
- flaxscrip (40hrs): requirements
- python1 (40hrs): specifications
- python2 (40hrs): design updates

Week 2-3: Finalize v.1 protocol python reference implementation:
- flaxscrip (40hrs): documentation
- python1 (40hrs): development & code review
- python2 (40hrs): development & code review

Week 4: Finalize UI and initial data types:
- flaxscrip (40hrs): documentation
- python1 (40hrs): configure data types python2 (40hrs): configure user interfaces

Week 5: Define and run test suite:
- flaxscrip (40hrs): test cases and test data
- python1 (40hrs): test scripts and development
- python2 (40hrs): test scripts and development

Week 7: Containers and release support:
- flaxscrip (40hrs): release support
- python1 (40hrs): package git & docker release python2 (40hrs): release support

Week 8-12: Implement initial (EDEN/EDA) use cases:
- Use-case1: Data notarization (IPFS cid)
- Use-case2: Data catalog (Metatron xid)
- Use-case3: Data versioning and transfer on blockchain using Metatron

The same team would be engaged in weeks 8-12 in support of the first community of users for the protocol.

The EDA community is already discussing needs for monetization of the protocol. Although at the moment, the protocol only requires IPFS, Filecoin would be a welcome addition to help with numerous incentivization and monetisation needs being discussed by the EDA community.

#### TOTAL BUDGET REQUESTED

Total budget for roadmap: \$72,000

This budget is allocated to a small technical core team:
- flaxscrip (full-time): requirements, documentation, QA, and user support
- 2 python developers (full-time): protocol development, bug-fixes, support.
- macterra (voluntary): technical advisor

### MAINTENANCE AND UPGRADE PLANS

We are looking for a long-term home for the project. We also need to attract / engage with a visionary management and marketing team to promote the use of the protocol.

Initially Metatron will launch to a community of users already aware and needing the functionality provided by the protocol. The Ethical Data Alliance has defined its needs in the form of the EDEN Protocol. Metatron provides the foundation system needed to implement the EDEN Protocol.

Note that the EDA is currently also in a fund-raising campaign.

# TEAM

### TEAM MEMBERS

flaxscrip as full-time lead macterra as voluntary technical advisor 2x python developers to launch and support the protocol

## TEAM MEMBER LINKEDIN PROFILES

Christian Saucier David McFadzean TBD TBD

### TEAM WEBSITE

Metatron on github Metatron Test Node

### RELEVANT EXPERIENCE

Flaxscrip and macterra have been working together for many years. We maintain an active list of our joint projects here: https://cryptotechguru.github.io/Cryptonomicon/

Particular relevant projects include:
- Tesseract (also see the Tesseract Blockchain Explorer). Metatron already supports Tesseract and Bitcoin. Tesseract is ultimately a fork of Bitcoin that has been modified to support SHA3.
- Lexinomicon. We used a community governance methodology called Nomicon to help manage the Ulex open source legal system community.
- Please see other projects and references on the Cryptotech.guru website.

## TEAM CODE REPOSITORIES

Metatron: https://github.com/macterra/metatron Tesseract: https://github.com/cryptotechguru/tesseract-core Micro-Nomicon: https://github.com/cryptotechguru/Cryptonomicon/blob/master/Nomicon/microNomicon.md Lexinomicon: https://ulex-opensource.github.io/Lexinomicon/ EDENomicon: https://nomicon.edenprotocol.io/ Cryptonomicon: https://github.com/cryptotechguru/Cryptonomicon

Christian Saucier, Walhalla SC David McFadzean, Toronto Canada