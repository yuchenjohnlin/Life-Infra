---
# === identity ===
id: njWyDHKYeVA
url: "https://www.youtube.com/watch?v=njWyDHKYeVA"
title: "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"
aliases:
  - "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"

# === creator ===
channel: Google Cloud Tech
channel_url: "https://www.youtube.com/channel/UCJS9pqu9BzkAMNTmzNMNhvg"
channel_follower_count: 1370000

# === time ===
duration: 2882
upload_date: 20260418
fetched_at: "2026-05-16T07:57:20+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/njWyDHKYeVA/maxresdefault.jpg"

# === content structure ===
chapters:
  - {start: 0, title: Intro}
  - {start: 368, title: Getting started with Agentverse lab}
  - {start: 477, title: Laying the foundations of the citadel}
  - {start: 967, title: "Forging the power core: Self hosted LLMs"}
  - {start: 1682, title: "Forging the citadel's central core: Deploy vLLM"}
  - {start: 2639, title: Summary}
chapters_authoritative: true
has_real_chapters: true
has_key_moments: false

# === language ===
language: en-US
original_language: en

# === subtitles ===
manual_track_languages:
  - en
auto_track_languages:
  - en
transcript_status: available
transcript_source: manual_en
transcript_target: null
is_translated: false

# === engagement ===
view_count: 10521
like_count: 390

# === status ===
availability: public
live_status: not_live

# === lifecycle ===
state: active
---

# Self host Gemma 4: Deploy LLMs on Cloud Run GPUs

## Description

GCP credit → https://goo.gle/handson-ep7-lab1
Lab → https://goo.gle/guardians

In this episode, we deploy Google's Gemma 4 model to Cloud Run two completely different ways, each with real trade-offs you need to understand before choosing one for production.

🔨 Ollama — model baked into the container. Instant cold starts. Rebuild to update.
⚡ vLLM — model mounted from Cloud Storage via FUSE. Slower first boot, but swap models without redeploying.

Both use Cloud Run GPUs, scale to zero, and ship through automated CI/CD with Cloud Build.

We build both. You decide which fits. 👇
📦 CI/CD with Cloud Build
🖥️ GPU accelerated serverless inference
🔄 Baked in vs. decoupled model architecture
🚀 Scale to zero
⚖️ Cold start speed vs. production agility

Chapters:
0:00 - Intro
6:08 - Getting started with Agentverse lab
7:57 - Laying the foundations of the citadel
16:07 - Forging the power core: Self hosted LLMs
28:02 - Forging the citadel's central core: Deploy vLLM
43:59 - Summary

More resources:
Cloud Run GPU documentation → https://goo.gle/4sEbTvG
Ollama documentation → https://goo.gle/3Qdi64w
vLLM documentation → https://goo.gle/4cvvxE9
Cloud Storage FUSE → https://goo.gle/4cQAb0V

Watch more Hands on AI → https://www.youtube.com/watch?v=qCBreTfjFHQ&list=PLIivdWyY5sqKnJOvP89yF8t9mWuzMTcbM
🔔 Subscribe to Google Cloud Tech → https://goo.gle/GoogleCloudTech

#Gemma4 #CloudRun

Speakers: Ayo Adedeji, Annie Wang
Products Mentioned: Agent Development Kit, Gemini API, Cloud Run

## Transcript

ANNIE WANG: Hi, everyone. Welcome to Hands-on AI where
we walk you through AI lab step by step. I'm Annie. AYO ADEDEJI: And I'm Ayo. ANNIE WANG: And
today, you're going to learn how to deploy Gemma
4 model with Ollama or VM to Cloud Run. And essentially, you can connect
your agentic system to Gemma 4. But before we dive into in this
architecture on the screen, let's take a step
back to understanding

this end-to-end agent
system management. So Ayo, why don't you start to
explain the cost and capacity for [INAUDIBLE]. AYO ADEDEJI: Oh, yes,
so as you mentioned, so throughout this
lab, we're going to be learning the pillars
of end-to-end agent system management. There's a lot of
different considerations that go into that. There's cost and
capacity considerations. So how do you optimize
your resources,

such as GPUs, when you're
deploying self-hosted models? Model strategy, when
do you select open versus closed models
for your use cases? Serving at scale,
how do you optimize for multi throughput and serving
multiple users at a time? Security and safety is another
one, as well as observability. So these are all
the pillars we're going to be covering as
part of this lab, and yeah. ANNIE WANG: Yeah,
so before we go

through how to
deploy Gemma 4, we need to understand the
difference between closed model and open model. Closed model like
Gemini, it's great. It's state-of-art. It's fully managed,
easy to start. An open model, like Gemma,
is easy to take control. You can even fine tune it. So why we're talking about
Gemma 4 today, right? Why would you want
to use open model IO? AYO ADEDEJI: Yeah,
you mentioned, you

just talked about a lot of
the pros of using open models. A lot of industries, such
as healthcare or finance, they're working in
industries where you may not be able to pass data
over the internet, or you may be limited with
how you can handle your data. In those use cases, if you have
to call these models on premise or in isolated scenarios,
running self-hosted models is a really good
solution for that.

As you mentioned, you
can customize the model. So a lot of use cases have
very domain-specific data, where you can improve
performance by tuning. And you can do that
with an open model, as opposed to closed models,
like Gemini, essentially, they're great out of the box,
they're state of the art, and they're really
general, but you may not be able to customize it
as much beyond tuning-- I mean, beyond prompting
and system instructions

of that nature. So those are the benefits
of using open models. ANNIE WANG: Yeah, and cost is
also another consideration. You can take a look
at this diagram that the more you use,
if you're using a closed model like Gemini,
the cost is increased per API call, versus if you're
using open model, like Gemma, the cost is not linear growth
because it's based on the infra. AYO ADEDEJI: Yeah. ANNIE WANG: So coming back
to this model strategy--

AYO ADEDEJI: Yeah, there's
many dimensions to consider. We talked about a few of
them, but those are just the ones to keep in mind. But beyond that, it's
also important to know that the reason why we're
so focused on model strategy is, at the end of
the day, these models act as the brain
behind your agents. So when you're using something
like Google's Agent Development Kit, not only could
you use Gemini

as the brain behind
these agents, you can use open models as well. So that's something that people
sometimes they don't know. They think you can
only use Gemini. But in reality, you
could pretty much use any model that you want,
because Google ADK comes with a LiteLLM wrapper that
allows you to connect models as you see fit. So later on in this
lab, we're going to learn how can you use Gemma
4 as the brain behind an agent.

ANNIE WANG: Yeah, so
essentially, agent is that you're using
the model as a brain, and then to reasoning, to
pick which two you want to pick to make a decision. And as you can see
on this diagram, this agent architecture, so the
model you're choosing really can determine the upper bound,
the capability of your agent system. That's why it's very important. And you want to be smart
to choose your model.

And when you choose
the model, you can think about the performance
of the model, the use case you want, and also the cost. You have different angle
to pick your model smartly. And so this is the
overall architecture you're going to dive into today. As you can see that on
this right-hand side, we're going to start
with this Runtime. So today, we will deploy Gemma
4 model, this service, vLLM and Ollama.

But yeah, why we have
this two different way? What is the real difference
between Ollama and vLLM? AYO ADEDEJI: Yeah, they're
both LLM serving frameworks. But you tend to see Ollama used
more in development use cases. It's really easy to install
and get up and running. So it's great for
experimental POCs. And you can also use it for
multi-GPU support use cases. vLLM is great for
production use cases.

It comes with Paged
Attention, it's great for memory
efficiency, and it allows you to do multiple
concurrency when it comes to calls and dynamic batching. So again, so Ollama is great
when it comes to development. vLLM is great for production. And there's other elements
serving frameworks, as well, like TensorRT-LLM and such. So there's a lot of options
to choose from in the world. But for this lab, we're
focusing on Ollama and vLLM.

ANNIE WANG: And
don't forget, you can also deploy a model to
Vertex AI through Model Garden. That's also another choice. It's a managed service for you. Yeah, so Ollama is
very easy to install. And it's very good
for you to try things in your local development. And let's get
started with Ollama. So as you can see from this
diagram, what we want to do is we want to first pull
the model from Ollama.

And then we want to build
this image with Docker. So once we have
this image, we're going to send it to the
Artifact Registry, which is a container on Cloud. And you can essentially
deploy the image so that you can have this
image hosted on [INAUDIBLE]. So that's essentially
how your agentic system agent is going to connect
to your deployed Gemma 4. And if you're interested, let's
start by going through this lab.

So we will have this link
on the screen about what is this lab link about. But as usual, Ayo,
usually we want to start with the equipment
check with the credit. But today, we're going
to skip the credit part. AYO ADEDEJI: Yes. Yeah, today, we're skipping the
credits because this lab does require GPU, such as when
we're deploying to Cloud Run, we will be equipping
our Cloud Run instances with L4 accelerators and such.

Because of that, we won't be
giving credits for this lab. But please feel free
to follow along. You could use your own credit
accounts if you have them, or you can sign up for free
trial credits on Google Cloud platform if you're a
first-time signer upper. But yeah, please feel
free to follow along. ANNIE WANG: As always, we
want to start our development in Cloud Shell on Google Cloud. To open that, making sure you
go to console.cloud.google.com.

And on the top right
there's a button. It's saying to
Activate Cloud Shell. Just click that,
and you will see this VS is similar to our
VS Code, but it's on Cloud. Essentially, it's
a VM hosting it. Yeah, Ayo, anything to add? AYO ADEDEJI: Yeah,
as you mentioned, so the Cloud Shell
editor is essentially like a VS Code on Cloud. It's persistent over time. So any code that you develop
or files that you create,

you can come back to
it a day, a week later. So please feel free to use it
as your development environment. That's actually what we're going
to be doing for today's lab. ANNIE WANG: Yeah, but one
thing you need to notice is you will time out
every 30 minutes or so for security reasons. So if you see any
error for IP address missing or some weird
issue, or [INAUDIBLE] asking you to re
authenticate it,

and just making sure
to refresh the page to refresh the token so that
it will keep you authenticated. And to get start, let's
just set up our environment so that we are ready to deploy
and host our Gemma 4 model. And as always, let's just
copy this [INAUDIBLE] code. Also, I'm going to zoom in. I'm going to copy this and
then paste it to my terminal. So you can see this terminal. And I paste it so that making
sure this Gmail account

is the same account you have
your billing account connected. And next, we need to
clone this to repo. We'll clone those to repo. And one is the
agentverse-dungeon and another one is the
agentverse-devopssre. Yeah, maybe, would you mind
explaining to our audience in case they haven't watched
our previous episodes? They don't know about
the agentverse concept. AYO ADEDEJI: Yeah, so we're
cloning two different repos.

The first one
agentverse-devopssre, that one has all the template
files for the agent we're going to be deploying later
on, the cloudbuild.yaml scripts that we're going to be using for
deploying our images to Artifact Registry and such. So essentially, it has a bunch
of staging and template files that kind of gets us up
and running a lot quicker. The dungeon repo has
essentially the boss dungeon and files that we're
using for the boss fight

later on in the lab. So once we build our
agent, essentially, we're going to be building
up to a boss fight, where our agent is
fighting with another agent in the cloud via A2A. So that one just has files
that we can get that up and running so by the
time we get to that point, our boss fight is ready to go. ANNIE WANG: Yeah, let's come
back to this setup page. And next, you need to initialize
a new project so that you have

a Google Cloud project ready. And you can see that you always
start with agentverse-guardian. You may have a
different number here. Essentially, the script is
creating a Google Cloud project for you. And it's trying to link the
billing to this project. So you can see now, I have
this full setup complete. But for you, if you're
running the script, you'll probably notice that when
you fetch the billing account,

it has a fetch failure. That because it's looking
for a trial account. So what you can do is if
you happen to have a billing account with your credit
card linked to it, this is where you
can do it manually in Google Cloud Console. Now, you're at
console.cloud.google.com. And then in the search bar-- so
I just click this Search icon in the search bar. I will search resources. So when I type resources,
I have something

called Manage Resources. So when I open the
Manage Resources, this is where you can
manage all your projects and its corresponding
billing account. So you can select this
Agentverse Guardian project. And here, you can just
click this button action and go to the billing. So now, this one, it's already
attached to my account. For your case, you'll
probably see a pop-up window to see manage
billing, And you can

select the billing that has
your payment information linked to it. Next is, as always, we want
to Gcloud config set project. And why we need to
configure the project? AYO ADEDEJI: Yeah. We're just making
sure that our project is set in Gcloud environment. So there's two ways
you can double check. If you're in the
Cloud Shell, you want to make sure that you
see your project ID in yellow. And beyond that, you
also want to make sure

that again, the Gcloud is
set to the right project. So what we just
did was making sure that the Gcloud is set to
the right project, which should match your Agentverse
Guardian some unique ID. Yeah. ANNIE WANG: Yeah. And next, we need to enable
some Google Cloud API. As you can see, if you
take a look at the API we want to enable, it's
including the storage. API platform-specific
storage is, essentially, you want to store
your-- later on, moving to vLLM,

we want to store our model
in Google Cloud Storage. And we want to
deploy to Cloud Run. We want to enable Cloud
Build, and we also want to have Artifact
Registry to store our image. So we want to enable this. And essentially, we want to
stay our store our API keys. So you want to enable
Secret Manager. Yeah. Anything you want
to mention, Ayo? AYO ADEDEJI: Yeah. So only thing I would
add is that just

by enabling these
APIs does not mean you're going to be charged
immediately for these APIs. Essentially, you're
just enabling them to be used in the project. A lot of people ask, if
I enable AI platform, Google APIs, for
example, will I start being charged by the second? No, you won't. You're only going to be charged
when you actually use the API. So that's just one
thing to keep in mind. ANNIE WANG: Yeah.

And it's coming back to this. Yeah. So now, we successfully
finish enabling. And next is, we need to create
this artifact repository so that later on, we can
deploy our image to it. So coming back to
this diagram that we want to build an image of-- we want to first pull the model
from Ollama and build the image and later, deploy this
to image repository. Yeah. I don't know why we want
to have this design.

Is there any other
way we can do? AYO ADEDEJI: No, this
is just best practice when it comes to CI in
context of Google Cloud, where essentially,
you're building an image, you're storing it in
Artifact Registry, you're deploying
it to Cloud Run. And it's-- essentially, this
is the build process that we're going to be enabling
with Cloud Build that allows us to programmatically specify
each of these steps,

and then we can go ahead and
just execute that Cloud Build YAML file. So you can see that later
on, once we get to that step. ANNIE WANG: Yeah. And also, you can see that
the model, essentially, we directly build it
because we do not have to store model anywhere,
because it's baked in Ollama. You will see really
soon in our lab. Yeah. So now, we have this repo,
artifact repository created. And next one is set
up the permission.

I don't know, what
is service account? Why we need to grant this
role to the service account? AYO ADEDEJI: Yeah,
great question. So every Google Cloud project
has a default service account. And that's essentially going
to be the operator behind many of your default actions. So if we're uploading
files to Cloud Storage or executing a Cloud
Build deployment, you want to make sure that
default service account has

certain permissions. So that's pretty much
all we're doing here. We're making sure that the
default service account has the ability to interact
with Cloud Storage, has the ability to
initiate Cloud Build jobs, has the ability to write
logs and read the logs, has the ability to interact
with Secret Manager, which we're going to be using
later on for storing our Hugging Face Secret Manager key. So as Annie just
mentioned, for Ollama,

we're going to be
baking in the model directly into the
container image. But when we actually
use VLM, we're going to be doing a
different approach. We're going to be storing
the model weights directly in Cloud Storage, and
pulling those model weights from Hugging Face. So there's different
approaches that are being enabled through
this IAM permissioning. ANNIE WANG: Now, one
metaphor I can think of

is, you can think of
service kind of a robot-- [LAUGHS] AYO ADEDEJI: Yeah. ANNIE WANG: --of yourself. And then you have different
robots controlling different permissions, and so
that you can manage the project permission. And here, we're using the
same account for easy demo. But in production, you can
have different robot account and different service account
for different permission configuration.

And the last step is to warm up. We need to run this warm
up, the [INAUDIBLE] script. So essentially, we want to
essentially using GCS fields for our VLM deployment. We want to run this
warm-up script here to warm up our GCS fields cache. And if you want to
know, what is GCS FUSE and why we want to
use that, stay tuned. We will talk about
it in VLM deployment. AYO ADEDEJI: Yes.

ANNIE WANG: Now, it's finished. Let's start host
our Java for Ollama. Let's get started. All right, so let's get started. So first, we want to pull
the image from Ollama. As I mentioned
earlier, you know, Ollama is great for
local development, and it's great for quickly
testing any model because Gemma 4 is baked in Ollama. And you can see, it's very easy. First, we want to create this
Dockerfile build the image.

And with only this
line of the code, you just need to run Ollama and
pull this Gemma 4 from Ollama. So now, you can just have
this model from Ollama. So it's very straightforward. And just copy this, and
coming back to my terminal, and paste it. So now, we just create
a Dockerfile folder. And what's next is
we want to create this cloudbuild.yaml file. So Ayo, maybe you can explain,
what is cloudbuild.yaml file,

before we explain what are
inside the cloudbuild.yaml file? AYO ADEDEJI: Yeah. So as mentioned
before, Cloud Build is essentially the engine
for CI/CD on Google Cloud. So essentially, it allows you to
programmatically specify steps you want to run as a process. So pretty much, all
we're doing here is we just created
the Dockerfile that defines our container image. Now, we're going to build
the container image.

In step one. We're going to push the
container image to Artifact Registry in step two. And then we're going to deploy
that container image to Cloud Run in step number three. So that's all we're specifying
here in the Cloud Build YAML file. ANNIE WANG: Yeah. So basically, it's
like a blueprint file to specify all the
steps you need to do, and exactly we're
showing on this diagram. So we just did is we have
this Dockerfile to explain

how to pull this image. So you want to build
this image and then push to Artifact Registry,
and deploy the image. It's like a blueprint file to
including all this process we want to have over here. And let's just copy this, and
coming back to our terminal, and paste it. But Ayo, why we want to
set the CPU to before, and why we want to build
a concurrency to before? For auto setting,
anything we need

to be aware of when we're trying
to deploy our image to Cloud Run? AYO ADEDEJI: Yeah. Cloud Run is a really
powerful serverless platform. It gives us a lot of
configuration capability. So as you can see here, we're
specifying 4 CPU minimum for each machine of the service. We're specifying memory to be
at least 16 gigabytes, which is really important if we're
going to be storing Ollama or Gemma 4 model on the image.

You have to have a lot
of memory capacity. So we're working with a
2D version of Gemma 4. So 16 gigabytes is
sufficient memory for that. So that's why we're
specifying that. We're specifying that we want
to use the NVIDIA L4 GPU type. We're specifying
concurrency to 4. We want to allow up
to four parallel calls against the service. And yeah. So again, Cloud Run gives
us a lot of configuration capabilities, and
we're just trying

to optimize for how we're going
to be using it in the lab. As you can see at the
bottom, we have Min instances equals 1, Max
instances equal to 1. That's not going to be
too common in production. You want to be able to
scale beyond one machine. But for cost purposes, just so
you're not allocating more GPUs than you need, we're kind
of just minimizing it to one machine per
service for this lab. ANNIE WANG: Yeah.

Also, we have this allow
unauthenticated for this lab purpose, but you can
make it authenticated for security reason, for
your actual image deployment. All right. So next one is, we want--
so now, we configure this cloudbuild.yaml file. So next step is actually
follow this blueprint in the cloudbuild.yaml file,
and then finish this process with Cloud Build. So just copy this. Basically, you put this Cloud
Build YAML file in the config

file, and then do the
setting with the region and the repo name
Project ID you have. And let's just go ahead
and go to our terminal, and go ahead to deploy
the whole process. If you want to track
the process of it, we can also go to Google Cloud
Console in the Cloud Build to see the process. So now, you can see that we just
finished the environment setup. And now, we're waiting
for the build to complete.

It's trying to pull
in the interval. So it's basically
following the process, trying to first build
the image, this Docker. AYO ADEDEJI: Yeah. And keep in mind, this
Cloud Build process will take some time. So this step may take anywhere
from 15 to 20 minutes, depending on how
long things take. So feel free to take a coffee
break and grab some coffee. But yeah, we'll be back once
our Cloud Build job completes.

ANNIE WANG: Yay! It finished! Finally. And as you can see, that we
can go to Google Cloud Console to also see the process, let
you research Cloud Build. We can see the process
we just had earlier. And yeah, this is
a building process. You're just having-- because
we have two building processes. One is for Dungeon. Another one is for
this deployment. You can also see, this image is
[INAUDIBLE] deploy to Cloud Run.

So let's just go to
Cloud Run, making sure that on the top left, it's
selecting the project. And go to the Gemma Ollama
baked service, and here we go. We have this URL that later on,
we can connect to our agent. So now, you have
this URL, right? We have this URL, and we want
to verify this is working by sending it the POST request. So here, basically, what
you want to do is this step. You know? This Ollama URL, this step
is to try to grab that URL.

You can also grab this
URL just by copy this. But here, this is a command
for you to grab this URL. And once you have
this URL, you're trying to test this URL
by sending this prompt. As a guardian of Agentverse,
what is my primary duty? Or you can send anything else. And then what you expect
is behind the scenes, you want this Gemma 4 model
answering this question. And let's see, what
is the response?

I'm just going to copy this
and paste it to the terminal.

Time to verify if
everything is working. AYO ADEDEJI: Yes. And now, all it's doing is
resetting the environmental variables because we're running
that set_env.sh file each time, just to make sure that
in case you lose context, because the building
process takes a long time. So throughout this
lab, we're setting that set_env multiple
times at the very top. So that's the reason why it
takes a little bit longer

for each step. But it's just important
to run, just in case you lose any context. And then, yeah, it's going to
print out the Cloud Run URL. And then we're going
to call the URL and see if we can get a
response from the LLM. ANNIE WANG: Yeah. So you have this URL, and then
you can send a POST request. We are expected to see a
response look like this. But maybe you're not exactly
the same response here,

because AI cannot generate the
same result every single time. But oh, let's see. This is a result. Oh, wow. OK. Here-- oh, yeah. The context. Oh. Here's the result.
This is the response. As a Guardian of the
Agentverse, the primary duty is this-- safeguard
because of the Agentverse representing reality. Yeah. Great. So that means the Gemma 4
on Cloud Run with Ollama is working. All right. So Ayo, you know that
we are using a Ollama,

and it's really
easy to get started, and it's really easy to use. And we have this model baking,
so that we have really fast code start. You do not have to start waiting
for it to load in the model, and to have the initial
code start problem. However, you have some
disadvantages, right? So Ayo, what are
some disadvantages with this Ollama use case? AYO ADEDEJI: Oh, yeah. So since we're baking in
the model into the image,

as you mentioned, it leads
to very fast code starts because the fact that the
image is already deployed, essentially, if
you want to create a new version of or new instance
of that machine for the service, it's really easy to spin up. In our particular use case,
we're only limited to 1. But if we were, it would
be really easy to spin up more instances for the service. But the downside to that
is because we're baking it

into the container image, if
you want to change the model version or the
parameters of the model, so you want to go from 2 B to a
larger version of the same model to a different model, you have
to rebuild the image and then redeploy. So it's a long process. And as you just saw, building
these images can take some time. So as mentioned before, it's
really good for development use cases. Oftentimes, when you're
running these models locally,

you may want to use Ollama. But if you're baking it
into the container image, it can be pretty inflexible
when it comes to rapid changes. But of course, when you're using
something like Cloud Build, you can automate the
changes to an extent, but that's just one
thing to keep in mind. ANNIE WANG: Yeah. Also, another thing
worth mentioning is if your production use
case serve huge traffic and you want to improve
the performance, that

is where you should really
consider using vLLM. And different from Ollama-- Ollama has a model baked in. But here, you want to grab
the model from Hugging Face, and save that to Cloud Storage. And then, this process
is a little bit similar where we have this model. The Ci pipeline is
kind of similar. You want to build the image. But this image does
not contain the model. It only contain the vLLM code.

And then once you
save that, push that to the image repository, and
then deploy them to Cloud Run. And now, you can see that
the container image is tiny because you only have vLLM code. And then the Gemma is going
to store in the Google Cloud Storage. And then we're be using
Cloud Storage FUSE to mount the bucket as a local folder. So anything you change in the
local folder will reflect it. Ayo, can you explain more
about Cloud Storage FUSE?

AYO ADEDEJI: Yeah. So Cloud Storage
FUSE is a great way of representing Cloud
Storage folders and paths as local paths for your machine
for the Cloud Run service, and that's what makes
it so efficient. So as far as any
package or service that's running on the
Cloud Run service, it's concerned-- it
can actually access GCS files the same way
that it would access local files, temp files that are
running directly on the machine.

So Cloud Storage
uses, essentially, what mediates that connection
between the Cloud Storage bucket and it being mounted as
a local folder for access directly on the
Cloud Run machine. Yeah. ANNIE WANG: So anything we
change in the local folder will also reflect it here. AYO ADEDEJI: Exactly, yeah. So and what makes
it really powerful is that not only could you read
from that local folder that's been mounted the same way
that you would read from a GCS

bucket, any files that you
write to that local folder is almost as if you're writing
to that GCS bucket as well, for persistence down the line. ANNIE WANG: So it's
bidirectional sync. AYO ADEDEJI: Yeah,
bidirectional. Yeah. ANNIE WANG: Yeah. Pretty cool. And let's take into how we're
going to save the model to Cloud Storage, and how to go
through all the Ci pipeline, and set up that
Cloud Storage FUSE.

Let's get to step five. All right. Let's get started by
first, download this model from Hugging Face, and then
save that to Cloud Storage. So let's get started. And what you need
to do is first, you need to go to step five. And when you're scrolling
down, and you can see that we have instructions here. If you don't have a
Hugging Face account, you can just create
an account over here, or you can Create
Account over here.

If you already have it,
you can just click Login. And now, you're in
this page to log in. And what's next is you
need to click on this link to generate a token. So now, I'm at this page. I'm going to click,
Generate a New Token. So you can use
Agentverse workshop token as a name, or any name you want. So just copy here for the
Agentverse workshop name. When it comes to the permission,
you can just use the Read rule.

So we can choose Read for this
use case, and create a token. And now, you have
this token ready. I just copy this to save it. So yeah, next
thing we want to do is we want to run this
command so that it will save the token to Secret Manager. And first, we just
copy this command. And then going back to our
terminal, I will paste it. So first, we want to
enable this script, and then we want
to run the script.

Essentially, behind
the scenes is we want to save the
token to Secret Manager. And Ayo, do you know
what Secret Manager? Might you explain to everyone
what is Secret Manager? AYO ADEDEJI: Great question. So Secret Manager,
essentially, it's eponymous. It speaks for its name. It's our best practice way
for managing secret API keys in Google Cloud context. So if you're working in a
Google Cloud environment,

rather than you storing your API
keys as environmental variables or sometimes, really
not good practices to embed it directly
into the file, what you can do with something
like Secret Manager is you can call the Google Cloud
a Secret Manager API, or there's Python SDK. And then you can
actually pull the secret during your actual runtime
into your application. So it's a way of preventing
you from having to actually

make visible your secrets
directly in the code, or having to store it
in environmental file. That adds more data governance
issues because now, you have to start managing
the environmental files, and make sure that they don't
get pushed to your code version in repo, and stuff like that. So overall, Secret Manager
is the best practice way for storing and managing
your application secrets. ANNIE WANG: All right.

So now, if you're
coming back, it's asked you to paste your
Hugging Face token. So what we want to
do is we just want to copy the token here
and paste it over here. You don't see anything. So if you happen
to paste it wrong, you can go to Secret Manager
here and delete the token and redo it, or you
can update the token. And once it's finished, you
will see the token saved in Secret Manager in Google
Cloud Console, over here.

All right. It says, success. And we can double
check by refresh it. And yeah, we have
this token created, and we have this one version. And if you want
to see the value, you can also see
view value, just verify this value is
the correct token. You just copy. So once it's
verified-- all right. So we just download the
model from Hugging Face, and we have this token
saved to Secret Manager. What's next is you want to save
this model to Cloud Storage.

So how to do that? First, you need to create
this Gcloud Storage bucket using this command
to create a Cloud Storage. And next is, you're making
sure the permission is ready. So I'm just copy this
command to prepare my Cloud Storage so that later on, I can
save my model to Cloud Storage. Yeah. Now, I finished,
so we can verify it by go to Google Cloud Storage. Store, Cloud Storage. You can Search Cloud storage
here, and making sure

we select Agentverse. And here in the
bucket, as you can see, we have two Cloud Storage ready. So this is the latest one,
because we have the previous one for our Dungeon deployment. And yeah, we have this
Guardians storage ready, and then we can
push our model here. Ayo, you can see we have
Cloud Build YAML file again. What does this file do? AYO ADEDEJI: Yeah,
great question. So what we're doing
here is essentially,

we're not going to go
through the Cloud Build process of actually
specifying the model that we want to download,
checking if the bucket exists. So that's step number one. We want to make sure that we've
actually created the bucket, and that's set as part of
its environmental variable. That's all going to be true. Two, we actually now want
to download, actually, from Hugging Face. So we're specifying
the model that we want

to download based off the ID. We're pip installing the
Hugging Face hub library. We're authenticating
with the token that we downloaded and saved
as part of Secret Manager. And then we're
downloading the model, and we're specifying
that it should save to our local directory. Again, we're using
GCS FUSE here. Remember earlier
on in the setup, we did the warm up for
the GCS FUSE cache. We're specifying the
model ID, and then

ultimately, just copying
that model to the GCS bucket. Yeah. ANNIE WANG: Great. So let's go ahead and create
this Cloud Build download YAML file so that we can continue. Let's continue. And first, it will create
this Cloud Build download YAML file for us to follow. AYO ADEDEJI: This will take
about anywhere from two to three minutes. It's a pretty
quick process here. ANNIE WANG: Yeah. So here, we're just creating
this Cloud Build download

file with our command. And next is, let's using Gcloud
Build command to run this Cloud Build download YAML file
so that it will actually do all the processes we
wrote in the blueprint. So let's go ahead and copy this. Yeah. So while we're waiting, we can
just mapping each little step to our diagram over here. As I mentioned earlier, that
first step is making sure our model bucket exists. So this is like a pre-check.

And once we have, we want
to log in to Hugging Face, and using the token-- so
basically, this is a step. We want to make sure we
get access to Hugging Face. And then we copy the
model, download the model to GCS bucket. So this is the next
step, is we want to-- once we have the token,
we download the model, and then from the GCS bucket. And once we have
this, we want to make sure the secret available
for this build environments.

Yeah, it finished! So what we've done so far
is, we have this token so that we can install this
model, and copy the model, and save everything to
the Google Cloud Storage. So this will be done, so far,
with this Cloud Build download YAML file. So this is basically, the
downloading processing, and we can verify
everything in the bucket. I'm going to refresh the page. You can see. Yay! We have Gemma 4.

Everything downloaded
in our Cloud storage. Great. What's next is--
oh, you can also verify Cloud GCS bucket
with a command over here. You can just copy this with
a Gcloud storage OS command to recursively verify
things in the Gcloud bucket. There's another verify. AYO ADEDEJI: All the
weight's downloaded, the optimizers, all of that. So yeah, it's just
listing out the files. ANNIE WANG: Yeah. So now, we verified it.

So the next thing is, we
need to finish this pipeline. So Ayo, do you know what is-- when we talk about network
subnet, what is the subnet, and why we need to compute
this networks subnet here? AYO ADEDEJI: Yeah,
great question. So Private Google Access is a
great kind of tool and feature that you can use when you have
different services communicating with each other. In our use case, what we
have is our model weights

being stored in Cloud
Storage, and then we're going to have it deployed
model on Cloud Run. We want to be able to pull these
weights without the data having to traverse over
the public internet. To accomplish that, we're going
to enable Private Google Access. So this will allow
our Cloud Run service to communicate
with our GCS files without actually
having to pull the data over the public internet.

So it's going to traverse
through our private subnet. So it's a really smart
way of keeping data secure when you have,
again, connections between different
services on Google Cloud. In our use case,
we have Cloud Run communicating with Cloud Storage
to pull the model weights. So that's the benefit of that. ANNIE WANG: Yeah. So you can see, we have
this line over here-- Cloud Run, pull
from Cloud Storage.

All right. So let's just copy
this and continue. All right. So we should continue. Once we download this
model and we set our VPC, and next, we want to
configure our CM pipeline. So Ayo, why we want to create
this Dockerfile for this vLLM and everything? What are the-- why we need
to do all those process here with Dockerfile? AYO ADEDEJI: Yeah,
great question. So what we're doing at the very
first step, since Gemma 4 just

was released just
last week, there's actually a version
of VLM image that's kind of specialized for Gemma 4. Essentially, what we're pulling
is the Gemma 4 version of VLM, just so it's optimized for
inference with Gemma 4. And then what we now
want to do is make sure that we're using a
transformers library that's compatible with the
newest version of Gemma 4. So all we're doing
is making sure that we are setting
the right version

of the transformers
library to a version that's compatible with Gemma 4. And then all we're
doing afterwards is cleaning up any default
models that were pulled, and setting the environment as
part of development process. And then we're setting the
entry point for the VLM server when it's being deployed on
Cloud Run, and that's it. So pretty much, all
we're doing, again, is we're specifying the
VLM default container

image that we want to use, one
that's specialized for Gemma 4. We're making sure that
our transformers library is compatible from a
version standpoint. And then we're just doing
some cleanup afterwards, and then specifying the entry
point for the Cloud Run service. ANNIE WANG: Yeah. How do we know the
right transformer for the version for
this Gemma 4 vLLM, or how do we change it
for a different model?

AYO ADEDEJI: Yeah,
great question. So there's multiple
ways you can do this. Sometimes, if you just
want to be a little bit more general, you can just say,
pip install transformers dash, dot upgrade, and
that'll make sure that you're installing
the very latest version. Other times, you can
look at the documentation and see what version
of the library was used for a particular model. So you take a look at the
Gemma 4 documentation vLLM,

you'll notice that
it's using 5.50. So it's just a good way
of being consistent. But yeah. ANNIE WANG: Got it. Thank you. So let's configure it by
quoting this on our Dockerfile. So now, we want to create
this Cloud Build pipeline. So to create this
pipeline, basically, is we want to
define the blueprint for this whole process. And the first is,
as always, we want to build the image with Docker. So we want to build this image.

So we have this image with vLLM. And then next is, you want to
push this to Artifact Registry, like this. And then this next
step is you want to deploy everything,
the service, a vLLM FUSE service
to Cloud Run. So while I'm deploying,
I'm going to copy this. I'm going to create this
cloudbuild.yaml file. Ayo, do we have different
setting here for vLLM, compared to Ollama settings previously? AYO ADEDEJI: Great question.

It's pretty similar. There are some
slight differences, especially because we're taking
a mounted approach with vLLM. So especially before, we have
the model weights in GCS, and we're mounting it on
the Cloud Run machine. So there's a few extra
parameters for that mounting. But beyond that,
when you actually look at the machine sizing, the
memory, the CPU, it's the same. And reason why is because
we're pretty much using

the same exact model with the
same exact amount of parameters, so the same memory
constraints are the same across Ollama and vLLM. But as I mentioned before, we
have a few other parameters to one, address the
Private Google Access that we enabled, so to make
sure that we can communicate with Cloud Storage
over private network, and then two, to actually
mount the Cloud Storage bucket as a local path.

So you can see, there's
some volume mounds that have been added as parameters. But beyond that,
it's very similar. ANNIE WANG: Hmm. Great. So once we have
this Cloud Build-- so this is the
Cloud Storage FUSE that we mentioned earlier that
can mount Google Cloud Storage bucket with local file. So this is like
earlier, we mentioned. And so, yeah, we have this Cloud
Storage FUSE explanation before. And you can check these
flags over here by configure

the volume for enable
Cloud Storage views. Next, we have this Cloud
Build YAML file configured. And next is, let's run this
Gcloud Builds Submit file, as always, to follow
this whole instruction, so that you will actually
follow this Ci pipeline. AYO ADEDEJI: Yeah. Build, push, and then
deploy to Cloud Run. Yeah. ANNIE WANG: Yeah. And it probably take 20
minutes or so, right? AYO ADEDEJI: Yeah. 20 to 30 minutes.

ANNIE WANG: All right. Looks like it's finished. AYO ADEDEJI: Yay. ANNIE WANG: Yay. So what's next is, let's take a
look at this Google Cloud Build history. So if you click this
link, it will take a look at this whole building
summary, the building process. And also, you can see the
Cloud Run service page by go to Cloud Run
Service, and making sure you pick this project. And you can see
that we have Ollama

that deployed from the previous
one, and vLLM is this one. Again, you can see that
we have this URL here. This is the link you can
connect to Gemma 4 model. And now, we want to verify
everything is working. So again, we want to send the
POST request with this URL link. And this is the endpoint
with a check completion. And we want to ask
the same question, like, as our Guardian
of Agentverse, what is my primary duty?

And we want to verify if this
whole deployed version of Gemma 4 hosted on Cloud Run,
is that working or not? So let's give it a try. I copy this. So I'm going to come
into the terminal, and I'm going to paste it here. So let's take a look
at what is the result. Yeah. As you can see, because the
first time initial load, we have some cold start. AYO ADEDEJI: Yeah. So let's look. So we see the response.

As a Guardian of Agentverse,
your primary duty is multifaceted, and so on. If you recall the
response from Ollama before, as Annie mentioned,
these models are stochastic. So you can call the same
model multiple times, and get a different response. But overall, very similar
response to the same question as before. And overall, everything
looks like it's working. Yeah. ANNIE WANG: Great. All right.

So just have a quick
overview of what we've done so far with vLLM. So first, we
download this image. We download the model
from Hugging Face to Google Cloud
Storage, and then we have this pipeline that we build
the image of the vLLM code, and then deploy the
whole thing to Cloud Run. And then we set up
the GCS views so that it will sync-- we
will mount the Cloud Storage with a local file. And let's talk about the
advantages or disadvantages

of this approach because
compared to Ollama, Ollama is very easy to
start and try anything, do the local development. VLLM is a great option
for production use case, and it's very flexible to
update the model and swap. You can just simply swap the
file in the bucket and restart. However, it has some
initial code start because it doesn't have the
model baked in, as Ollama does. Anything to add, Ayo, for
the trade-off with vLLM?

AYO ADEDEJI: No. That's a great summary
where essentially, with VLM, with the process
that we took, essentially, you can use something
like GS FUSE to dynamically update the
model weights if you need to. [INAUDIBLE], essentially,
there's a longer cold start. But one caveat with
that is that it's really meant for the initial
invocation or initial user. If you have multiple
concurrent users, 1,000 users calling the
same endpoint at a time,

that warm instance
actually won't, obviously, have that cold start
for future users. So it's really meant--
that cold start you tend to experience, really
meant for the first call to that newly created machine. But, yeah. ANNIE WANG: So here
is an overview of-- so far, we have Ollama and vLLM. So those are the advantages of
Ollama, for local development and prototyping, and also
has multiple GPU support.

However, if you use the
production use case, like vLLM has the page
attention for product efficiency and parallelism for
maximize GPU usage. So yeah, it's really good
for production use case. So coming back for this
high-level architecture we have-- and for today's
episode, we learn, how do you host Gemma 4 model
with Ollama, vLLM to Cloud Run? So this is the piece
we covered for today. We cover how do you
pull model from Ollama

and host on Cloud
Run, and we also know how to download the
model from Hugging Face and then host it with vLLM. And what's next, Ayo? What are we going to cover next? AYO ADEDEJI: Oh
yeah, great question. We're going to learn
lots of things. So we're going to learn,
how can you serve and scale these models at a global
scale using something like a load balancer? How can you secure
these models and protect

against things like model
prompt injection, jailbreaking? How can you determine if
your model is actually leaking sensitive data? The answer for that is also
something like Model Armor. How can you use these
models as the brain behind a deployed agent? We talked a little bit about
Light LM earlier today. We're actually going
to put this in practice tomorrow and use
Lightroom to connect with our self-deployed
models, so we

can use them as the brain
behind these agents. And lastly, we're going
to learn, how can you actually observe the metrics
being generated by these models? So we talked about cost earlier,
and how can you actually monitor that from how many tokens are
being generated by these models? You can use something like a
Prometheus Sidecar associated with the Cloud Run instance to
actually be extracting metrics

such as, how many tokens
are being generated, what is the GPU
utilization, and so on. So we're going to be
learning a lot tomorrow. I hope you guys all stay tuned. And-- ANNIE WANG: That's a
really good summary. So by the end of
these two episodes, you're going to learn everything
about this end-to-end agentic system management. Yeah. AYO ADEDEJI: Yeah. So stay tuned. But until next time, I'm Ayo.

ANNIE WANG: I'm Annie. Bye. [MUSIC PLAYING]
