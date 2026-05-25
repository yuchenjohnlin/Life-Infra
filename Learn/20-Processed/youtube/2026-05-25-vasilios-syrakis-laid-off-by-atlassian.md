---
id: 55pTFVoclvE
url: https://www.youtube.com/watch?v=55pTFVoclvE
title: I was laid off by Atlassian
aliases:
  - I was laid off by Atlassian
channel: Vasilios Syrakis
channel_url: https://www.youtube.com/channel/UCRs5BtvLv1NkOWxLupTIVYw
duration: 2406
upload_date: 20260510
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/55pTFVoclvE/maxresdefault.jpg
view_count: 1768711
transcript_file: "[[Learn/10-Raw/youtube/55pTFVoclvE|55pTFVoclvE]]"
type: youtube-digest
state: active
---

# I was laid off by Atlassian

> [!quote]- Source description (cleaned)
> Chapter list for the video — no other promotional content was included in the original description.
> - 00:00 Intro
> - 00:58 Interview process
> - 04:16 Starting at Atlassian
> - 04:35 Building an Open Service Broker
> - 07:43 Diagram of OSB architecture
> - 09:56 Picking a proxy technology — Envoy
> - 11:36 Envoy XDS Control Plane
> - 14:33 AWS Infrastructure
> - 17:45 Creating the machine image (AMI)
> - 20:22 24 month recap
> - 21:09 What did I do after building
> - 22:45 Extending the load balancing platform
> - 24:37 Envoy extensions
> - 25:54 Edge Compute and centralized logic
> - 27:12 Handling concerns for dev teams
> - 31:35 Diplomacy and conflict resolution
> - 32:14 Maintaining software over long-term
> - 35:42 Personality Conflicts
> - 37:11 Mentoring

> [!info] Orientation
> A solo reflective video from Vasilios Syrakis, a platform engineer who spent eight years at Atlassian before being let go in a recent layoff round. It's not a polished conference talk — it's an informal screen-share, narrated while he sketches architecture diagrams live on a whiteboard tool, and it walks through the actual systems he built (a self-service load-balancing platform on Envoy) plus the non-technical lessons he took away. Useful as a candid case study of how a single engineer's mandate at a large company evolves over almost a decade — from "build the app you promised in your interview" to "centralize concerns for thousands of services" — and as a personal retrospective on maintenance, conflict, and mentoring at the same time. Audience: backend / platform / infra engineers, especially anyone curious about real-world Envoy control planes or what long-tenure platform work actually looks like day to day.

## TL;DR

An eight-year platform-engineering retrospective, told as one continuous arc that starts at the whiteboard and ends with the human side of the job.

- **The interview made him a promise he had to keep.** Asked what success at 12 months would look like, his interviewers described a self-service load-balancer platform — and his first task on day one was to build exactly that. The Open Service Broker (OSB) he stood up in Python became the seed of everything that followed.
- **From OSB to a full Envoy edge.** The broker (FastAPI + SQS worker + DynamoDB) handled async provisioning. To replace expensive enterprise load balancers, the team picked Envoy and Vasilios wrote *Sovereign*, an XDS control plane that turns dynamic context from the broker into rendered Envoy config. Underneath: CloudFormation across ~13 regions managing ~2,000 EC2 proxies, with AMIs baked by Packer + SaltStack.
- **The platform's real leverage was centralizing concerns.** Once Jira, Confluence, Bitbucket and the long tail of microservices were forced through this edge, the team could solve auth, authz, rate-limiting, DDoS, access logs, and tracing *once* — in Envoy filters or in sidecars (his auth sidecar was in Rust) — instead of in "a bazillion bazillion" backend services.
- **Building is easy; maintaining is hard.** Over eight years he watched code churn cluster predictably in specific areas — a smell that something needs restructuring. He's curious-but-cautious about how vibe-coded / AI-assisted codebases will hold up when maintenance burdens start to bite.
- **The non-technical lessons surprised him most.** Diplomacy and conflict resolution grew more than any technical skill. Personality clashes hurt his performance enough that he took the lesson seriously. And mentoring — distinct from teaching, which he's good at — remains the thing he's least sure he's figured out, partly because he was never mentored himself.

## Chapters

| #            | Chapter                                                                          | Time    | Uploader's chapters                                                                                                                              |
| ------------ | -------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Part I**   | Joining Atlassian                                                                |         |                                                                                                                                                  |
| 1            | [[#1. Intro and the interview process (00:00)]]                                  | 00:00   | Intro; Interview process                                                                                                                         |
| 2            | [[#2. The mandate: a self-service load balancer (04:16)]]                        | 04:16   | Starting at Atlassian; Building an Open Service Broker                                                                                           |
| **Part II**  | Building the load-balancing platform                                             |         |                                                                                                                                                  |
| 3            | [[#3. OSB architecture: async provisioning via worker and queue (07:43)]]        | 07:43   | Diagram of OSB architecture                                                                                                                      |
| 4            | [[#4. Envoy as the proxy, Sovereign as its control plane (09:56)]]               | 09:56   | Picking a proxy technology - Envoy; Envoy XDS Control Plane                                                                                      |
| 5            | [[#5. AWS infrastructure and the AMI build pipeline (14:33)]]                    | 14:33   | AWS Infrastructure; Creating the machine image (AMI)                                                                                             |
| 6            | [[#6. The 24-month foundation, in one sentence (20:22)]]                         | 20:22   | 24 month recap                                                                                                                                   |
| **Part III** | Scaling the platform                                                             |         |                                                                                                                                                  |
| 7            | [[#7. Migrating Jira, Confluence, and the long tail (21:09)]]                    | 21:09   | What did I do after building                                                                                                                     |
| 8            | [[#8. Extending Envoy: centralizing concerns at the edge (22:45)]]               | 22:45   | Extending the load balancing platform; Envoy extensions; Edge Compute and centralized logic; Handling concerns for dev teams                     |
| **Part IV**  | The non-technical retrospective                                                  |         |                                                                                                                                                  |
| 9            | [[#9. Maintenance as the real long game (31:35)]]                                | 31:35   | Diplomacy and conflict resolution; Maintaining software over long-term                                                                           |
| 10           | [[#10. Personality conflicts and the growth of diplomacy (35:42)]]               | 35:42   | Personality Conflicts                                                                                                                            |
| 11           | [[#11. Mentoring vs. teaching (37:11)]]                                          | 37:11   | Mentoring                                                                                                                                        |

---

## 1. Intro and the interview process (00:00)

The video opens as a reflection: Vasilios was just laid off by Atlassian after eight years, and wants to talk through the things he built that he's personally proud of — partly to document them, partly in the hope that someone in a similar situation might draw inspiration (or avoid his mistakes). Most of it will be technical, but the non-technical bits get their own section at the end.

The interview process, eight years ago, was already different from today's. A HackerRank coding quiz he aced with full marks. A first technical interview where two interviewers handed him a Cloudflare white paper on custom domains, left the room for ten minutes, came back, and asked him to articulate what was in it — then a few questions on microservices and containers. A second technical interview was a troubleshooting exercise: prompt the interviewer for information to debug a real Atlassian incident, an application-level problem that escalated into a denial of service. He was also asked how latency-based DNS works; he reasoned from first principles (guessing Route 53 triangulated on actual client latency) and was inaccurate but apparently acceptable — the real answer is probably a geolocation database driving the DNS responses.

Then a values interview. Most of it he doesn't remember, except for the question he asked the interviewers: looking back from 12 months in the future, what would need to be true for hiring me to have been a good decision? Their answer was concrete — they wanted an internal application that would let Atlassian's developers self-serve load balancers, the internal equivalent of AWS ALBs. He said he could build it. He had confidence with Python web apps. They believed him, and hired him.

That conversation is the seed of everything else in the video: the rest of the eight years grew out of the answer to that one question.

---

## 2. The mandate: a self-service load balancer (04:16)

Joining Atlassian comes with the in-house cliché of "drinking from the fire hose" in the first few months. The very first task Vasilios gave himself was to build the application he'd been told they wanted: an **Open Service Broker** (OSB).

He pulls up the open spec on GitHub to show what an OSB actually is. It's a web app with a defined API that brokers the provisioning of resources for a platform — designed in a Kubernetes-shaped world where workloads come and go and need to bind resources (databases, load balancers, whatever) on demand. The spec defines endpoints like the *catalog* (lists available services and plans), and PUT / PATCH / DELETE flows for provisioning and updating. At Atlassian, the user experience wasn't a console with clickable buttons — internal developers expressed their intent via config files committed to version control, which a build server uploaded when deploying a service.

The first implementation used a Python library called Connexion, which generates API handlers directly from an OpenAPI document. That eventually migrated to plain Flask, and then to FastAPI — which is reportedly still what it runs on today. The shape of the thing matters more than the framework: an HTTP API that accepts provisioning requests for load balancing, validates them, and hands them off for the slow work to happen elsewhere.

That "elsewhere" is the next chapter.

---

## 3. OSB architecture: async provisioning via worker and queue (07:43)

The first whiteboard sketch makes the shape concrete. The OSB is a FastAPI app fronted by a client; behind it sits a **worker process**, a **DynamoDB** table, and **SQS** in between. The web app does not perform provisioning inline — it would block for too long. Instead, it accepts the request, drops the task details onto SQS, and the worker picks them up and does the actual work asynchronously.

A provisioning task in this world is concrete cloud work: creating DNS records, creating a CloudFront distribution, making whatever API calls are needed against AWS. While the worker grinds through this, the client polls: *is it ready yet?* When the worker finishes, it writes status to DynamoDB; the FastAPI app reads that on the next poll and responds with success or failure.

That's it — that's the broker. Vasilios is explicit that this part isn't conceptually complicated; the interesting complexity lives downstream, in what gets provisioned. And what's being provisioned, from a customer's point of view, is *load balancing somewhere in Atlassian's edge infrastructure so that traffic can reach their service*. That demand is the bridge into the next, more interesting piece: the proxy fleet itself.

---

## 4. Envoy as the proxy, Sovereign as its control plane (09:56)

One of the architects had been pushing an idea independently of the broker: replace Atlassian's enterprise load balancers — which carried real licensing costs — with an open-source, cloud-native, commodity proxy. The choice was **Envoy** (similar in role to nginx, but more modern; the headline property that matters here is its first-class dynamic-configuration API). Crucially, Envoy can reload configuration at runtime, which means you can deploy a large fleet of proxies once and reconfigure them on the fly. Combined with the broker, that gave devs a real self-service experience: push a configuration change through provisioning, and it flows out to the proxies — no ticket to the platform team required.

The piece that makes that flow work is the Envoy **management server** — what the team called the **control plane**. Vasilios open-sourced his implementation as **Sovereign** (still on Bitbucket, at least for now). Architecturally, it's another FastAPI app, but with a different job: it ingests *templates* and *context*, and serves rendered Envoy configuration to proxies that ask for it.

The Envoy resource types it serves are the usual ones — clusters, routes, listeners. Sovereign keeps a set of templates for each, and on every request it pulls the current context, merges it through the templates, and returns the result. Where does the context come from? Two main sources in his diagram: the **broker's DynamoDB** (the dynamic state of what's currently provisioned) and **other places** like an S3 bucket that holds slower-changing data. The data sources are deliberately pluggable because the context is fundamentally dynamic — services come and go, configurations change, and the rendered output must reflect that.

Put together, the full request flow becomes legible: a developer's client sends a provisioning request to the broker; the worker performs the work and writes new state to the database; Sovereign polls the broker (and the other sources), regenerates configuration, and the proxies pick it up the next time they request it. The proxy's behavior then changes — new routes, new clusters, new listeners — without anyone restarting anything.

---

## 5. AWS infrastructure and the AMI build pipeline (14:33)

Two questions remain about the proxies themselves: *where do they live*, and *how do they come into existence*?

The first answer is **CloudFormation**. Each proxy fleet is provisioned by a CloudFormation template — AWS's infrastructure-as-code mechanism. The template describes the standard cast: a VPC, subnets, an internet gateway, security groups, a key pair, an IAM role, and crucially an Auto Scaling Group that creates the actual EC2 instances. The ASG references an AMI (more on that in a moment), an NLB sits in front as a layer-4 proxy, ACM handles certs, and a few Route 53 records pin everything together. At steady state this produced roughly **2,000 proxies across ~13 regions** — basic AWS building blocks, but a lot of them.

The AMI isn't built by CloudFormation — it's *referenced* by it. AMI production is its own pipeline, built with **HashiCorp Packer** and a **SaltStack** configuration repo. Packer uses an EC2 provisioner: it spins up a live EC2 instance in a dev account, uploads the Salt configuration, runs the Salt provisioning step (SaltStack being in the same family as Puppet, Ansible, and Chef — a declarative way to install packages, drop files, and run services in a specific order), then snapshots the instance into a reusable image.

The Salt states layered onto that image cover everything a production proxy needs: install and configure Envoy, an **observability agent** (covering logs, traces, and metrics), security hardening, network tuning, container support, and tracing. CloudFormation then takes that AMI and rolls out EC2s; at boot, runtime parameters inject secrets and keys, and the proxies come up ready to accept traffic.

That, end-to-end, is the foundation: broker, control plane, proxy fleet, image pipeline.

---

## 6. The 24-month foundation, in one sentence (20:22)

The recap puts the whole stack in one breath. When a developer says *"I want my service to be publicly accessible with all the fancy routing and bells and whistles,"* the platform's response is now mechanical: the broker accepts the request and queues a provisioning task; the worker writes the new state; Sovereign re-queries that state (plus everything else), renders new Envoy configuration through the templates, and serves it to the proxies the next time they ask. The proxies were pre-provisioned long ago by CloudFormation, running on AMIs baked by Packer + SaltStack. Centralized load balancing, dynamically reactive to deployments, owned by his team.

That's roughly the first two years of the job in a single paragraph. Everything that follows is *what you do with that foundation*.

---

## 7. Migrating Jira, Confluence, and the long tail (21:09)

With the platform in place, the next stretch was migration: get the big products *and* every microservice onto the new edge. The microservice case was relatively easy — it could be enforced from the platform side. Previously the platform itself had given every service a very basic load balancer; the team changed that contract so you could no longer expose your service publicly through the default path. To go public you had to go through their centralized load balancing infrastructure, which doubled as an explicit *signal of intent* that your service was meant to be reachable. Before, public exposure could happen almost by accident, often without proper protection. After, public meant deliberate.

The big products — Jira, Confluence, Bitbucket, Statuspage, and many others — had to be moved onto the edge through real effort. They had special cases that a generic multi-tenanted platform had to learn to support; the migration took years and a long tail of feature work. By the end, the centralized edge actually fronted Atlassian's flagship products, not just the long tail.

---

## 8. Extending Envoy: centralizing concerns at the edge (22:45)

Once everything was behind the edge, the platform's real leverage became visible: Envoy is enormously configurable, and the team had built the abstraction layer that exposed *the right amount* of that configurability to developers.

Envoy's routing alone is a small world: virtual hosts decide which domains a listener accepts, route actions decide where requests go, you can match, redirect, direct-respond, add and remove headers — and importantly, *any* route can in principle send to *any* cluster on the proxy. That last property is dangerous in a multi-tenant setting. With a thousand devs and a thousand clusters, you can't let an arbitrary route point at an arbitrary cluster. So a lot of the team's engineering work concentrated in the **validation layer**: ensuring the simple parameters developers passed in could not, after being rendered through the templates, produce a configuration that misroutes traffic between tenants. Vasilios half-jokes about the "curse of knowledge" — it feels routine to him now, but there is genuinely a lot of it.

Beyond routing, Envoy's extensions matter just as much: network filters (the **HTTP Connection Manager** being the big one, handling routing, proxying behavior, websockets, etc.), plus things like *external processing* and *external authorization* hooks. These are the bridges into the second part of the story.

**Centralizing logic at the edge.** The whole point of putting all of Atlassian's services behind a programmable proxy is that you can solve concerns *once*, before requests reach the backends. Imagine — Vasilios gestures at the whiteboard repeatedly — "a bazillion bazillion" backend services. If every one of those teams had to independently implement authentication, authorization, DDoS protection, rate limiting, and access logging on their own service, the company would burn enormous money, slow every feature down, and ship less for its customers. Centralizing these concerns at the edge is what unlocks platform leverage.

How each concern actually landed:

- **DDoS protection** was delegated to CloudFront, sitting in front of the NLB. (This piece was led by a colleague Vasilios describes as very smart and conscientious.)
- **Access logs** were handled inside Envoy natively, via network filters configured by the HCM. Because all of this configuration is dynamic and template-driven, a developer's small JSON input fans out into the full access-logging setup automatically.
- **Authentication, authorization, and rate limiting** were more complex and used a **sidecar model**: Envoy talks out the side to a local container running its own service. Auth was written by Vasilios in Rust ("the Lord's language"). Authorization and rate limiting were contributed by other teams. The sidecars themselves were installed and configured onto the AMI by the same Packer + SaltStack image-build pipeline described earlier — so the proxy fleet shipped with them already in place.

The result: a programmable edge with sidecars that themselves receive dynamic configuration over the wire, solving cross-cutting concerns in very little time, well before requests ever reach the backends.

After that came compliance work — taking everything that already existed and re-shaping it to meet new compliance requirements. He's blunt that this stretch was tedious and boring for him: checklist work, no new building.

---

## 9. Maintenance as the real long game (31:35)

The remainder of the video shifts to the non-technical lessons. The first one is **maintenance**, and Vasilios treats it as the harder half of software engineering — the part that doesn't show up at the start.

At the beginning of any system there's a predictable batch of work: onboarding people, writing documentation, training colleagues so they know what particular log messages mean, which metrics to check when things go wrong, what those metrics indicate, and how to resolve the expected failure modes (an AWS outage taking out the database; SQS going down and blocking provisioning; a proxy receiving valid-but-traffic-destroying configuration). That work is real but it's predictable.

The harder problem is what happens *over time*. People come and go. New hires need onboarding from a now-larger collective who all need to know the system. New people bring new opinions; they look at the existing codebase, want to change things, and do. He frames this as **churn** — and the key observation is that churn is *not uniform*. Some areas of a codebase churn predictably, and once you notice an area is churning, that's a *smell*: it's an indicator that this part of the system is going to keep growing in size or complexity unless something is done. Identifying those areas early is half the battle.

He folds his concern about LLM-assisted code in here: it will be interesting to see how vibe-coded apps handle the maintenance phase, because the people running them may not be deeply familiar with what was created. Building is easy; *changing* something while keeping it changeable is hard, because changes slowly couple things together and eventually a change in one area breaks another. He's cautiously hopeful that LLMs could help with the detangling once these areas are identified, but doesn't want to be too optimistic just in case.

---

## 10. Personality conflicts and the growth of diplomacy (35:42)

The second non-technical lesson is about people, and it's the one he says he grew most in. Over eight years he was exposed to many different managers and colleagues, with many different personalities and working styles. With enough variety, conflict is statistically inevitable — and he had conflicts with people he still respects, simply because personalities sometimes don't mix.

His framing of how to handle it is generous and practical: you need self-awareness, awareness of the other person, and enough understanding of psychology to take responsibility for the difference itself — to anticipate where conflict is going to come from and act to make the relationship work. Maybe it's sometimes impossible. But personality conflict was a real source of stress and at times it visibly affected his performance — which is the part that made him take it seriously. Because his performance was affected, he learned and changed, and he expects to handle similar situations meaningfully better the next time they arise.

---

## 11. Mentoring vs. teaching (37:11)

The final reflection is about **mentoring** — and importantly, Vasilios draws a careful distinction between mentoring and what he's actually good at.

What he's good at: helping colleagues, pointing out areas where they need understanding, delivering that understanding, breaking down complex things into simple terms so they can build a working mental model. That kind of teaching and pairing was his "bread and butter" for the second half of his Atlassian tenure — jumping on calls, working through problems with colleagues, getting consistent feedback that he was always available to help and could distill hard topics into something understandable. He's proud of that.

Mentoring, he insists, is distinct from that — and harder for him. He had an intern in his last year who got the highest possible rating, which essentially guarantees an offer. The project they shipped was impressive, and they got there partly by working with several subject-matter experts on Vasilios's team in areas where he himself is weaker. The intern did the majority of the actual legwork: building, testing, design decisions. The result was excellent.

But he still feels uncertain about his own contribution to mentoring specifically. The hard part for him was *calibration*: how much time to give the mentee, what that time should consist of, how to avoid handing over answers while also not letting them get so stuck they got frustrated. He doesn't have a good way of evaluating whether he hit that balance, and acknowledges that part of the difficulty is that he was never mentored himself — so he doesn't have a model of what mentoring should feel like to receive.

He closes with the offer that, if there's interest, he could do follow-up videos rebuilding some of these systems from scratch on stream — both as a teaching exercise and to sharpen his own skills. Then he signs off.
