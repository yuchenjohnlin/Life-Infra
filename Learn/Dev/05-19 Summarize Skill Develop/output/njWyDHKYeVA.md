---
id: njWyDHKYeVA
url: https://www.youtube.com/watch?v=njWyDHKYeVA
title: "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"
aliases:
  - "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"
channel: Google Cloud Tech
channel_url: https://www.youtube.com/channel/UCJS9pqu9BzkAMNTmzNMNhvg
duration: 2882
upload_date: 20260418
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/njWyDHKYeVA/maxresdefault.jpg
view_count: 10629
transcript_file: "[[Learn/Dev/05-19 Summarize Skill Develop/input/njWyDHKYeVA|njWyDHKYeVA]]"
type: youtube-digest
state: active
---

# Self host Gemma 4: Deploy LLMs on Cloud Run GPUs

> [!quote]- Source description (cleaned)
> In this episode, we deploy Google's Gemma 4 model to Cloud Run two completely different ways, each with real trade-offs you need to understand before choosing one for production.
>
> - **Ollama** — model baked into the container. Instant cold starts. Rebuild to update.
> - **vLLM** — model mounted from Cloud Storage via FUSE. Slower first boot, but swap models without redeploying.
>
> Both use Cloud Run GPUs, scale to zero, and ship through automated CI/CD with Cloud Build.
>
> Topics: CI/CD with Cloud Build; GPU-accelerated serverless inference; baked-in vs. decoupled model architecture; scale to zero; cold-start speed vs. production agility.
>
> Speakers: Ayo Adedeji, Annie Wang. Products: Agent Development Kit, Gemini API, Cloud Run.
>
> Lab: https://goo.gle/guardians
> Cloud Run GPU docs: https://goo.gle/4sEbTvG · Ollama: https://goo.gle/3Qdi64w · vLLM: https://goo.gle/4cvvxE9 · Cloud Storage FUSE: https://goo.gle/4cQAb0V

> [!info] Orientation
> Episode of *Hands-on AI* from Google Cloud Tech, a step-by-step lab series walking through a single agent-system task end-to-end. This episode is part of an "Agentverse" lab arc (the "Guardian" lab) that builds toward an A2A boss-fight demo in a later episode; here the focus is just the model-serving layer. Hosts Annie Wang and Ayo Adedeji alternate between clicking through the Google Cloud console and explaining the architectural why behind each step. The level is practical-introductory: aimed at developers who already know what Docker and a REST endpoint are but may not have deployed a self-hosted LLM on GPU before. The chosen model is Gemma (referred to throughout as "Gemma 4") at the 2B size, small enough to fit comfortably on a single NVIDIA L4.

## TL;DR

The same open model — Gemma 4 (2B) on a single Cloud Run instance with an L4 GPU — can be served two very different ways, and the choice changes what is cheap and what is hard.

- **Why self-host an open model at all.** Closed models like Gemini are state-of-the-art and managed, but cost grows linearly per API call and you cannot ship them into environments (healthcare, finance, on-prem) that won't let data leave the network. Open models invert both: cost is dominated by infra rather than per-call, and you can fine-tune for domain-specific data. The model also matters because, via Google ADK's LiteLLM wrapper, *any* model can be the brain behind an agent — model choice sets the agent's capability ceiling.
- **Ollama path — bake the model into the image.** Fastest cold start (weights are already on disk when the container boots), trivial to set up, ideal for development and POCs. Cost: every model swap means rebuilding and redeploying a multi-GB image, a 15-20 minute Cloud Build run each time.
- **vLLM path — decouple weights from code.** Pull weights from Hugging Face into a Cloud Storage bucket, mount the bucket into the Cloud Run container with Cloud Storage FUSE (bidirectional sync, GCS objects look like local files), and ship only the tiny vLLM container. Now swapping models means replacing files in a bucket — no rebuild. Pays a real first-call cold start because weights stream in at boot, but only for the first user on a fresh instance; concurrent and subsequent users hit a warm machine. vLLM also brings PagedAttention and dynamic batching, which is why it's the production choice.
- **Supporting machinery, all serverless.** Cloud Build as the CI engine (one `cloudbuild.yaml` per pipeline: build → push to Artifact Registry → deploy to Cloud Run); Secret Manager for the Hugging Face token rather than env vars; Private Google Access so Cloud Run pulls weights from GCS without traversing the public internet; default service-account IAM grants tying it all together.
- **The throughline.** Baked-in vs. mounted is not just an implementation detail — it's the axis between "fast to start, slow to change" and "slow to start, fast to change," and serverless GPU on Cloud Run is what makes either viable at scale-to-zero cost.

## Chapters

| #         | Chapter                                                                                          | Time     | Uploader's chapters                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------- |
| **Part I**| Framing                                                                                          |          |                                                                                                     |
| 1         | [[#1. Why open models, and the model-as-brain framing (00:00)]]                                  | 00:00    | Intro                                                                                               |
| **Part II** | Lab plumbing                                                                                   |          |                                                                                                     |
| 2         | [[#2. Lab setup: project, APIs, IAM, and the GCS FUSE warm-up (06:08)]]                          | 06:08    | Getting started with Agentverse lab; Laying the foundations of the citadel                          |
| **Part III** | Two serving paths                                                                             |          |                                                                                                     |
| 3         | [[#3. Path A — Ollama with the model baked into the image (16:07)]]                              | 16:07    | Forging the power core: Self hosted LLMs                                                            |
| 4         | [[#4. Path B — vLLM with weights mounted from Cloud Storage (28:02)]]                            | 28:02    | Forging the citadel's central core: Deploy vLLM                                                     |
| **Part IV** | Wrap-up                                                                                        |          |                                                                                                     |
| 5         | [[#5. Trade-offs side-by-side, and what comes next (43:59)]]                                     | 43:59    | Summary                                                                                             |

---

## 1. Why open models, and the model-as-brain framing (00:00)

The lab opens by stepping back from "how do I deploy this" to "why would I deploy this." End-to-end agent-system management has several pillars — cost and capacity (how do you size GPUs for self-hosted models), model strategy (open vs. closed, and which use case), serving at scale (multi-user throughput), security and safety, and observability — and the choice of model touches almost all of them.

The closed/open contrast is drawn pragmatically rather than ideologically. Closed models like Gemini are state-of-the-art, fully managed, and easy to start with; their downside is two-fold. First, cost scales linearly with API calls — every prompt is metered. Second, they can't go where data can't go: regulated industries like healthcare and finance often cannot send data over the public internet, and on-prem or isolated deployments rule out a hosted API entirely. Open models like Gemma invert this: the cost curve flattens because you're paying for infra rather than per call, and because you control the weights, you can fine-tune for domain-specific data rather than being limited to prompting and system instructions.

The framing then escalates: the model isn't just a generator, it's the *brain behind the agent*. The agent uses the model to reason and pick which tools to call, which means the model sets the upper bound on what the agent can do. A common misconception, the hosts note, is that Google's Agent Development Kit only works with Gemini. In fact ADK ships with a LiteLLM wrapper that lets any model — closed or open — sit behind an agent, and later episodes will use Gemma as exactly that.

This sets up the rest of the lab: the goal is to deploy Gemma 4 (the 2B variant) so that an agent can call it. The hosts introduce the two serving frameworks they'll compare. **Ollama** is positioned as the development tool — trivial to install, easy to get a model running locally, decent multi-GPU support, great for experimental POCs. **vLLM** is positioned as the production tool — PagedAttention for memory efficiency, dynamic batching, and concurrent request handling. (Vertex AI's Model Garden is mentioned as a third, fully-managed option that's out of scope for this lab.) Both will be deployed to Cloud Run with an NVIDIA L4 GPU, and the architectural difference between the two paths is foreshadowed: Ollama bakes the model into the image, vLLM keeps the model in Cloud Storage and mounts it.

## 2. Lab setup: project, APIs, IAM, and the GCS FUSE warm-up (06:08)

Before either deployment, the lab walks through the plumbing — and the plumbing matters because the same scaffolding underpins both paths. Because the lab requires a GPU, no free credits are issued; viewers are pointed at their own billing accounts or a Google Cloud free trial.

Development happens in Cloud Shell — effectively a VS Code-like editor running on a managed Cloud VM, persistent across sessions, with one quirk to know: it times out roughly every 30 minutes for security, so authentication errors usually just mean "refresh the page." Two repos get cloned: `agentverse-devopssre` (containing the agent templates and the `cloudbuild.yaml` scripts used for image build/deploy) and `agentverse-dungeon` (containing assets for a later boss-fight demo). A fresh Google Cloud project — `agentverse-guardian` with a unique suffix — is created and linked to a billing account; if the automatic billing fetch fails because it's looking for a trial account, the hosts demonstrate doing the link manually under *Manage Resources*.

`gcloud config set project` points the local environment at the new project. Then a batch of APIs gets enabled — Cloud Storage (for the vLLM model weights later), AI Platform, Cloud Run (the serving target), Cloud Build (the CI engine), Artifact Registry (the image store), and Secret Manager (for the Hugging Face token). The hosts make the cost-anxiety point explicitly: enabling an API does not incur charges; you're only billed when you actually call it.

An Artifact Registry repository is created to hold the container images. Then IAM: the default service account — Annie's analogy is "a robot version of yourself" with its own permissions — is granted what it needs to interact with Cloud Storage, kick off Cloud Build jobs, read and write logs, and pull from Secret Manager. In a real production setup you'd split these across multiple service accounts per principle of least privilege, but for the lab everything goes on the default account.

Finally, a "warm-up" script preps the GCS FUSE cache. The explanation of *what* FUSE is gets deferred to the vLLM section; here it's just done so it's ready when needed.

## 3. Path A — Ollama with the model baked into the image (16:07)

The Ollama path is deliberately the simplest possible deployment. The Dockerfile is essentially one substantive line — run Ollama and pull Gemma 4 — so that the model's weights become part of the container image at build time.

The CI is expressed as a `cloudbuild.yaml`, which the hosts describe as a "blueprint" for the deployment process. It has three steps that mirror the diagram exactly: build the container image with Docker, push it to Artifact Registry, and deploy it to Cloud Run. This same three-step shape recurs for the vLLM path, which is part of the point — Cloud Build is the engine for CI/CD on Google Cloud regardless of what you're shipping.

The Cloud Run service config is where the GPU-serverless reality shows up. Each instance gets 4 CPU minimum, at least 16 GB of memory (enough to hold the 2B Gemma weights), one NVIDIA L4 GPU, and a concurrency cap of 4 parallel requests. Min and max instances are both pinned to 1 — not realistic for production, where you'd want to scale up, but a deliberate cost-control choice so the lab doesn't over-allocate GPUs. For the lab the service is set to `--allow-unauthenticated`; production would require auth.

Submitting the build takes 15-20 minutes. When it finishes, the Cloud Build history in the console shows the three-step pipeline and a Cloud Run URL is exposed. The verification step is a POST to that URL with the prompt *"As a guardian of Agentverse, what is my primary duty?"*; Gemma 4 responds with an in-character answer, confirming the model is serving.

The trade-off discussion that closes this chapter is the whole point of doing Ollama first. Because the weights are already in the image, cold starts are very fast — spinning up a new instance is just starting a container, no model download required. The cost is rigidity: changing the model version, switching from 2B to a larger variant, or swapping to a different model entirely means rebuilding and redeploying the image, which means another full 15-20 minute Cloud Build cycle. That's fine for local development and one-off experiments, and Cloud Build can automate the rebuilds, but it's an awkward fit for any workflow with rapid model iteration.

## 4. Path B — vLLM with weights mounted from Cloud Storage (28:02)

The vLLM path is the structural opposite: the container image holds only the vLLM code; the model lives in a Cloud Storage bucket; the bucket is mounted into the running container so vLLM reads weights as if they were local files. The image is therefore tiny, and swapping models becomes a matter of replacing files in a bucket rather than rebuilding the image.

The mechanism for the mount is **Cloud Storage FUSE**. The hosts emphasize that this is genuinely bidirectional — anything written to the mounted local folder is persisted back to the GCS bucket, and any read from the folder pulls from GCS. From vLLM's point of view, the model directory is just a directory. This is what makes weight-swapping cheap.

The setup unfolds in clear stages:

**Hugging Face token via Secret Manager.** Weights come from Hugging Face, which requires an access token. Rather than treat the token as an environment variable (visible) or commit it (worse), the lab puts it in Secret Manager and pulls it at runtime. The hosts frame Secret Manager as the best-practice way to store application secrets in a Google Cloud environment — it removes the data-governance burden of managing `.env` files and keeps secrets out of code. A read-only token is generated in Hugging Face, then stored via a script that prompts for the value (invisibly) and pushes it into Secret Manager; the console can be used to verify or rotate it.

**Bucket creation and the model-download pipeline.** A dedicated `agentverse-guardians` Cloud Storage bucket is created with the right permissions, then a *second* `cloudbuild.yaml` — the "download" pipeline — runs as a one-off to fetch the model weights into the bucket. Its steps: confirm the bucket exists; `pip install huggingface_hub`; authenticate with the Secret Manager-stored token; download the specified model ID; copy the resulting files into the GCS bucket (via the FUSE path that was warmed up earlier). The hosts step through the Cloud Build console to confirm completion and use `gcloud storage ls -r` to verify all weights and optimizer files landed.

**Private Google Access via a VPC subnet.** With weights now living in GCS but about to be pulled by Cloud Run, the hosts enable Private Google Access on the subnet so that traffic between Cloud Run and Cloud Storage stays on Google's private network rather than traversing the public internet. This is the standard pattern for service-to-service communication on GCP when you want both security and lower latency.

**The vLLM-tuned Dockerfile.** Because Gemma 4 was newly released, there's a vLLM image specialized for it; the Dockerfile pulls that base, pins the `transformers` library to a version known to be compatible with Gemma 4 (the hosts note you can either `pip install transformers --upgrade` for the latest, or — better — check the model's documentation for the verified version), cleans up any default models pulled by the base, and sets the entry point for the vLLM server.

**The deployment pipeline.** A third `cloudbuild.yaml` runs the same build → push → deploy shape as the Ollama path, with two important additions to the Cloud Run config: parameters for Private Google Access so the service can talk to GCS over the private network, and volume-mount parameters that expose the GCS bucket as a local path inside the container. CPU, memory, GPU, and concurrency settings are unchanged from Ollama — the model is the same size, so the resource envelope is the same. This build takes 20-30 minutes.

Verification mirrors the Ollama test: POST the same Guardian-of-Agentverse prompt to the Cloud Run URL's chat-completions endpoint. The first request shows the cold-start delay the hosts will dissect in the next chapter; the response itself is similar to Ollama's but not identical, which the hosts use to remind that these models are stochastic.

## 5. Trade-offs side-by-side, and what comes next (43:59)

The summary lines the two paths up against each other rather than declaring a winner. Ollama wins on simplicity and cold-start speed because the image carries the weights — perfect for local development, prototyping, and multi-GPU scenarios. vLLM wins on production flexibility: PagedAttention for memory efficiency, dynamic batching for parallelism, and — because weights are mounted rather than baked in — you can swap models by changing what's in the bucket and restarting, no rebuild.

The cold-start nuance vLLM pays is worth a careful framing the hosts call out: yes, decoupling weights costs you a real delay because they stream in at boot. But that delay is paid only by the *first* call to a freshly-spawned instance. Once the instance is warm, subsequent and concurrent users — the hosts use "1,000 users calling the same endpoint at a time" as the scale to imagine — hit the warm machine and pay no extra. The cold start is a one-time tax per new instance, not a per-request one.

The episode closes by pointing at where the Hands-on AI series goes next: serving and scaling these self-hosted models globally with a load balancer; protecting them against prompt injection, jailbreaking, and sensitive-data leakage using Model Armor; wiring them in as the brain behind an ADK agent via LiteLLM (the promise made back in chapter 1); and observing them — using a Prometheus sidecar attached to the Cloud Run instance to extract token-usage and GPU-utilization metrics, which is how the earlier cost discussion connects back to operational reality. The two episodes together are meant to cover the full pillars of end-to-end agentic system management introduced at the start.
