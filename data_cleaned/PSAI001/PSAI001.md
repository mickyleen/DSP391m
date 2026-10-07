# Open Grant Proposal: Lotus Farcaster

# Project Description

lotus-farcaster V3 brings additionnal functionnalities to lotus farcaster (see tables below).

Lotus farcaster is used by 400+ miners, was downloaded more than 200 times and get 30+ new users during the last 2 weeks. We want to keep farcaster has one of the main analytics companion of miners by continuously adding features supporting their new challenges. This new release follow Filecoin roadmap and bring storage markets features, bring support to the new lotus split mode architecture and made it reusable for other project by providing all the functions are a python module. This tool is build for the community and we really want to keep it opensource

Lotus farcaster is a Visualization and Analytics tool for Lotus Filecoin node It leverages Prometheus, Grafana and Python.

We want it to be accessible and designed for any types of miners. It's designed to manage all type of architecture: single miner, single miner with workers monolitic and split store architecture (markets node) multiple miners farm.

We want to move from console based monitoring to a proactive professional monitoring grade. Compared to the existing console tools, users will benefits: consolidated information data history push notification Visual monitoring Scalable solution User management Security Mobile device accessibility

## How it works

#### Architecture

```text
-------------------------- ------------ ----- ---------------- ------------ | Lotus Miner | | | | Grafana | | Web Client | | lotus-exporter-farcaster | <------- | Prometheus | <------- | farcaster-dashboard | <------- | | -------------------------- ------------ ----- ---------------- ------------ | | -------------------------
|-> | Lotus Daemon | | ------------------------- | | ------------------------- |-> | Lotus Markets | -------------------------
```

#### lotus farcaster comes with 2 Components :

A Grafana dashboard lotus-exporter-farcaster a standalone python script executed every minute by the crontab. It generates metrics that are exposed by node-exporter to prometheus.

#### Security

The design and choice of these components, was made to keep a high level of security:
- metrics are pulled from the miner to avoid compromising network or management servers
- lotus-exporterfarcaster doesn't bind any ports to avoid exposing the miner to external threat
- lotus-exporter-farcaster run under unprivileged user (ideally lotus user) to avoid system being compromised
- The global solution doesn't rely on any cloud or remote component. To avoid data leak.

lotus-exporter-farcaster is running locally on the miner without any specific privilege nor access to other servers.

#### It will follow prometheus guidelines :

ressources inexpensive standard prometheus metrics naming compatible with 3rd parties dashboards and exporters

### Benefits

Support any type of lotus architecture Easy to deploy Small footprint Collect lotus node and miner data Only rely on API Data are pulled from the Prometheus server (increase security) Deployed on the miner node only Run under Unprivileged user

## Dashboard Features

|Feature | Status Comments |
|--------------- | -------------------------------------- |
|Sectors | V1 |
|Mpool | V1 |
|Storage Info | V1 |
|Workers | Info V1 |
|Sealing | V1 Job + Scheduler |
|Power | V1 |
|Wallets | V1 |
|Chain | V1 Head + Sync Status |
|Deadlines | V1 |
|Deals | V2 |
| | View of current sealing deals |
|Gas Fee | V2 Realtime gasfee and History |
| | (requested by Community) |
|Sectors State | V2 |
| | Identify faulty sectors in deadlines |
| | (requested by Community). Helping |
| | miners to quickly indentify which |

|sectors | to restore |  |  |
|------------------- | -------------------------- | ------------------ | ----------------- |
|Fil+ Datacap V2 |  |  |  |
|Fil+ | Realtime | and Historical | view |
|of Datacap | allocated |  | to the miner |
|Max Quality |  |  |  |
|A new | indicator, | showing | the |
|maximum | power | that | can be |
|expected | from | a miner | (it’s a |
|forecast | of the | power | after the next |
|deadline | if the | full capacity | is |
|Sectors w/ |  |  |  |
|Breakdown | of | sectors | in 3 |
|categories | : | CC / inc. | deals / inc. |
|Verified. | Current | and | historical |
|view, | helping | the miner | to |
|understand | how | he gets | is power |
|over | time |  |  |
|Address lookup V2 |  |  |  |
|Allow | miners | to provide | a custom |
|lookup | file (Adress=Name/Label) |  | to |
|improve | dashboard | readability.. | The |
|lookup | apply | to any | panels |
|containing | adresses |  | (Wallet / Deals |
|/ Fil+ | / etc…). |  |  |
|Farcaster | reports | any | problems |
|when | scraping | data. | Ensuring |
|dashboard | is | accurate. |  |
|toolset V3 |  |  |  |
|Provide | a deployement |  | script |
|supporting | and | autodetecting | any |
|type | of lotus | architecture | + Docker |
|Full Python |  |  |  |
|Provides | all | functionnalities | as a |
|Python | library. |  |  |
|V3 Provides | on-going | downloads, |  |
|pending | publishing | deals, | etc… |
|Dashboards |  | helping | miners to |
|identify | expired | sectors | correlated |
|with | errors to | help fast |  |

### Roadmap

The planning could be shorted if Protocol Labs for any reasons decide to force miners to switch to splitstore.

- 01 sep 2021: V3 scoping
- 07 sep 2021: V3 Development of Design / Specifications / Mockup
- 30 sep 2021: First release open to beta tester
- 15 oct 2021: Public release of the new farcaster (without the python lib)
- 15 nov 2021: Public release of the python lib

|Milestone Hours Cost |  |
|------------------------------------------------------ | --- |
|Collect needs from the community, design, planning 8 |  |
|Studing the new Lotus API and reverse iengineering 8 |  |
|Exporter development (lotus V3.0) 40 |  |
|€ | 2 |
|Dashboard development (lotus V3.0) 40 |  |
|€ | 2 |
|Collect feedbacks from beta user / bug fix and UI 10 |  |
|Automatic Deployment process + Docker 20 |  |
|€ | 1 |
|Python library 50 |  |
|€ | 3 |
|Launch support (community support / comm / bug |  |
|€ | 1 |
|New Video Tutorial + Documentations (Docstring + |  |
|Dashboard request) |  |
|€ | 1 |

Option: Additionnal support per major update (start

after included support consummed)

10

€ 720

No VAT charged

#### Maintenance and Upgrade Plans

Tools will be updated according to lotus release. Will be glad to work closer with PL team to specify API needs.

# Team

## Team Members

Julien NOEL - julien.noel@twinquasar.io

## Team Website

https://twinquasar.io

# Relevant Experience

Julien is a:
- Filecoin miner, actively helping the filecoin community on slack.
- Filecoin Notary
- Part of MinerX program IPFS and Web3 enthousiast, starting being active around filecoin right before Space Race, Julien is a computer science engineer, spending 15 years working for Top100 companies providing strategic advice to C-level around new technologies.