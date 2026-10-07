# VUE.JS + TYPESCRIPT SUBSTRATE FRONT-END TEMPLATE

### PROJECT OVERVIEW :PAGE_FACING_UP:

#### OVERVIEW

When building our app (The Wunderbar Network team is part of the Substrate Builders Program), we have used a very useful existing community template - the Substrate Front End Template from the Substrate Developer Hub. This template is built using React.js and JavaScript. We are proposing to create an alternative version of this template, which would achieve three major outcomes:

- 1. Create an extendable template app, where developers can quickly connect and interface with the Substrate blockchain, using simple, clear and strongly typed examples, with a great baseline UX (which could provide a starting point for an entire new project).

This will build on top of what the current community template provides.

- 2. It would use Vue.js instead of React.js

According to StackOverflow's 2022 Developer Survey, React.js is still undeniably in the lead when it comes to web framework popularity (according to the survey, 42.62% of projects would be using React), however at 18.86% Vue.js is still in the top 6 and is on the rise.

- 3. It would be written using TypeScript as opposed to JavaScript.

Even though most developers who code in TypeScript can work well with JavaScript and vice versa, the "conversion" is not always straight-forward, and despite JavaScript being around for a very long time (and seemingly not going anywhere), TypeScript is gaining rapidly in popularity and most greenfield projects would prefer TypeScript over JavaScript.

According to same survey mentioned above, JavaScript is the most commonly used technology (for the tenth year in a row!), however TypeScript is steadily closing in. Looking at the loved vs. dreaded category though, the picture is very different - TypeScript is loved by 73.46% of developers (and is near the very top of the list), whereas JavaScript achieved a score of 61.46% to be placed in the middle of the table.

Overall, we believe that the combination of TypeScript's strong, static typing, and Vue's simplicity will together serve the purpose of providing an alternative source of very clear examples of how to interface with a Substrate Node from a modern front-end application, which should be of great value to the community.

#### PROJECT DETAILS

The core technology stack is Vue 3 + Typescript, integrated with the Polkadot.js set of packages. The app will deliver Vue3 native components and "composables" (reusable functions), that other developers will easily be able to integrate/build on top of.

The app will also provide a Dockerfile and container.

We have created a mockup design (in both dark and light mode), screenshots below (we also have a high-fidelity Figma file that can be provided upon request).

Note that Wunderbar Network team is already using the same technology stack to consume Substrate blockchain features into the app we are building as part of the Substrate Builders Program, therefore we already have experience in both the core technology stack, and the Polkadot.js API packages.

This grant will not include future ongoing maintenance of the deliverables, unless agreed prior (i.e. smaller grants to periodically refresh/keep up to date), or additional feature requests after the agreed milestone deliveries. We will however address reported bugs and major security vulnerabilities.

#### ECOSYSTEM FIT

Where and how does your project fit into the ecosystem?

This app provides a more robust and extendable example/template app compared to the current Substrate Front End Template app, which should be of great value to builders within the ecosystem, that are utilising the same or similar tech stack as ours.

Primarily UI developers, although any builders interfacing with Substrate would find value. New users, hackathon teams, etc would also be strong contenders to use this app as a template/baseline for what they are building.

The combination of TypeScript's strong, static typing, and Vue's simplicity will together serve the purpose of providing an alternative source of very clear examples of how to interface with a Substrate Node from a modern front-end application, which should be of great value to the community.

The Substrate Front End Template from the Substrate Developer Hub. Our project aims to provide a more robust example app, providing all the benefits and advantages mentioned above.

### TEAM :BUSTS_IN_SILHOUETTE:

#### TEAM MEMBERS

Dan Henton Mila Dymnikova Miloš Ranđelović

#### CONTACT

Contact Name: Dan Henton Contact Email: dan@wunderbar.network Website: Wunderbar Network

#### LEGAL STRUCTURE

Registered Address: Level 1, 320 Ti Rakau Drive, Burswood 2013, Auckland, New Zealand Registered Legal Entity: Greengate Global Ltd

#### TEAM'S EXPERIENCE

Wunderbar Network is a currently active participant of the Substrate Builders Program. We have extensive experience building Typescript + Vue.js apps, and interfacing with Substrate Nodes via API.

#### TEAM CODE REPOS

https://github.com/WunderbarNetwork

Please also provide the GitHub accounts of all team members. If they contain no activity, references to projects hosted elsewhere or live are also fine.

https://github.com/DanHenton https://github.com/Milarr https://github.com/MilosRandelovic

### TEAM LINKEDIN PROFILES (IF AVAILABLE)

https://www.linkedin.com/company/wunderbar-network/

# DEVELOPMENT STATUS :OPEN_BOOK:

Not started yet, mockup designs/wireframes provided above.

## DEVELOPMENT ROADMAP :NUT_AND_BOLT:

#### OVERVIEW

Total Estimated Duration: 6 months Full-Time Equivalent (FTE): 0.5 FTE Total Costs: US\$ 30,000.00

#### MILESTONE 1 - FOUNDATIONS + HEADER + ACCOUNT PANELS

|Number Deliverable |  |  |  | Specification |  |  |  |
|---------------------------------- | ------------ | ----------- | ---------- | ------------------- | --------------- | ----------- | ---------------- |
|0a. License | Apache | 2.0 |  |  |  |  |  |
|0b. Documentation |  |  |  |  |  |  |  |
|We | will | provide | both | inline | documentation |  | of the code |
|and | a | basic | tutorial |  |  |  |  |
|0c. Testing and Testing Guide |  |  |  |  |  |  |  |
|Core |  | functions | will | be fully | covered | by | comprehensive |
|unit | tests | to | ensure |  | functionality | and | robustness. In |
|the | guide, | we | will | describe | how to | run these | tests. |
|0d. Docker |  |  |  |  |  |  |  |
|We | will | provide | a | Dockerfile(s) | that | can be | used to |
|test | all | the |  | functionality | delivered | with | this |
|1. Foundations of a Vue.js app A | standalone |  |  | Vue.js/Typescript | app | (built | using Vite) |
|2. UI/UX elements |  |  |  |  |  |  |  |
| | Common | UI/UX | elements | from | the provided |  | mockup |
| | designs | for the |  | Header, | Balance | Transfers | and Account |

| | Balances panels |
|---- | ------------------------------------------------------- |
|3. | Composables |
| | Common composables to connect and interface with a |
| | Substrate node and all supported Web3 wallets |
|4. | Header |
| | Provide common Substrate node metadata and select an |
| | “active” account from a list of seeded and injected |
|5. | Account Balance List & Transfer |
| | Provide the ability to see the balances (and perform |
| | a transfer) between both seeded and injected accounts |

### MILESTONE 2 - RUNTIME MANAGEMENT, EVENT PANEL AND PALLET INTERACTION COMPOSABLES

|Number |  | Deliverable Specification |
|---------- | --------------------- | ------------------------------------------------------- |
|0a. | License | Apache 2.0 |
|0b. | Documentation |  |
| |  | We will provide both inline documentation of the code |
| |  | and a basic tutorial |
|0c. | Testing and Testing | Guide |
| |  | Core functions will be fully covered by comprehensive |
| |  | unit tests to ensure functionality and robustness. In |
| |  | the guide, we will describe how to run these tests. |
|0d. | Docker |  |
| |  | We will provide a Dockerfile(s) that can be used to |
| |  | test all the functionality delivered with this |
|1. | Runtime management |  |
| |  | The ability (via the header) to choose a Substrate |
| |  | Node connection and upgrade the runtime |
|2. Event | panel |  |
| |  | Display a panel which live-updates from global |
| |  | Substrate Node events |
|3. | Pallet interaction | composables |
| |  | Composables that are able to call queries, |
| |  | extrinsics, RPCs and read constants |

### MILESTONE 3 - COMPLETE VUE.JS APP

|Number | Deliverable | Specification |
|-------- | --------------------------- | -------------------------------------------------------- |
|0a. | License | Apache 2.0 |
|0b. | Documentation |  |
| |  | We will provide both inline documentation of the code |
| |  | and a basic tutorial |
|0c. | Testing and Testing Guide |  |
| |  | Core functions will be fully covered by comprehensive |
| |  | unit tests to ensure functionality and robustness. In |
| |  | the guide, we will describe how to run these tests. |
|0d. | Docker |  |
| |  | We will provide a Dockerfile(s) that can be used to |
| |  | test all the functionality delivered with this |
|0e. | Article |  |
| |  | We will publish an article /workshop that explains […] |
| |  | (what was done/achieved as part of the grant). |
|1. | Pallet Interaction Panel |  |
| |  | A panel that can execute extrinsics, RPC calls or |
| |  | display constants, using mapped parameters |
| |  | dynamically generated for each call, and displaying |
| |  | live events as the transaction transitions state |
|2. | Chain State Query Panel |  |
| |  | A panel that can display the chain state, optionally |
| |  | providing parameters, and displaying live events as |
| |  | the transaction transitions state |

# FUTURE PLANS

We plan to promote this project within the development community. In case of significant Substrate/Polkadot.js API changes in the future, the app should be upgraded to reflect those (out of scope for the grant, as mentioned above).

# ADDITIONAL INFORMATION :HEAVY_PLUS_SIGN:

How did you hear about the Grants Program? Via the Substrate Builders Program, networking with people from Parity/Web3 Foundation