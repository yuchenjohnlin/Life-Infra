---
source_url: https://www.youtube.com/watch?v=njWyDHKYeVA
source_type: youtube
source_platform: youtube.com
title: "Self host Gemma 4: Deploy LLMs on Cloud Run GPUs"
author: Google Cloud Tech
video_id: njWyDHKYeVA
captured_at: 2026-04-22
duration_min: 48
status: raw
---

# Raw transcript — Self host Gemma 4: Deploy LLMs on Cloud Run GPUs

> Auto-generated English subtitles from yt-dlp, parsed to `[HH:MM:SS] text` with rolling duplicates removed.

## Chapters (official)

- 00:00:00 Intro
- 00:06:08 Getting started with Agentverse lab
- 00:07:57 Laying the foundations of the citadel
- 00:16:07 Forging the power core: Self hosted LLMs
- 00:28:02 Forging the citadel's central core: Deploy vLLM
- 00:43:59 Summary

## Transcript

[00:00:00] Hi everyone, welcome to hands-on AI,
[00:00:02] where we walk you through AI lab
[00:00:04] step-by-step and Annie and I am IO.
[00:00:07] And today
[00:00:08] you're going to learn how to deploy
[00:00:11] Gemma 4 model with Ollama or vLLM to
[00:00:15] Cloud Run. And essentially you can
[00:00:17] connect your agentic system to Gemma 4.
[00:00:21] But before we dive into in this
[00:00:22] architecture on the screen, let's take a
[00:00:25] step step back to understanding this
[00:00:26] end-to-end agent system management. So
[00:00:29] IO, why don't you start to explain the
[00:00:31] cost and capacity
[00:00:33] for this
[00:00:33] &gt;&gt; Yeah, so as you mentioned, so throughout
[00:00:35] this lab we're going to be learning the
[00:00:36] pillars of end-to-end agent system
[00:00:38] management. There's a lot of different
[00:00:39] considerations that go into that.
[00:00:40] There's cost and capacity
[00:00:41] considerations. So how do you optimize
[00:00:43] your your resources such as GPUs when
[00:00:46] you're deploying self-hosted models?
[00:00:48] Model strategy, when do you select open
[00:00:50] versus closed models for your use cases?
[00:00:52] Serving at scale, how do you optimize
[00:00:54] for you know, multi-throughput
[00:00:57] and serving multiple users at a time.
[00:00:59] Security and safety is another one
[00:01:01] as well as observability. So these are
[00:01:03] all the pillars we're going to be
[00:01:04] covering as part of this lab and yeah.
[00:01:07] Yeah, so before we go through how to
[00:01:10] deploy Gemma 4, we need to understanding
[00:01:12] the difference between closed model and
[00:01:14] open model. You know, closed model like
[00:01:16] Gemini is great, it's like it's state of
[00:01:19] art, it's fully managed, easy to start.
[00:01:21] Open model like Gemma is easy to take
[00:01:23] control, you can even fine-tune it. So
[00:01:25] why we're talking about Gemma 4 today,
[00:01:27] why why would you want to use an open
[00:01:29] model? IO
[00:01:31] Yeah, it's a good you mentioned you just
[00:01:32] talked about a lot of the pros of using
[00:01:34] open models. A lot of industries such as
[00:01:36] health care or finance, they're they're
[00:01:38] working industries where you may not be
[00:01:40] able to pass data over the internet or
[00:01:42] maybe limited with how you can kind of
[00:01:44] handle your data. In those use cases if
[00:01:46] you have to kind of
[00:01:47] call these models on premise or in kind
[00:01:50] of isolated scenarios, running
[00:01:52] self-hosted models is a really good
[00:01:53] solution for that. Um Ollama as you
[00:01:55] mentioned, you can customize the model.
[00:01:57] So a lot of use cases have very um
[00:02:00] uh domain-specific data where you can
[00:02:02] kind of improve performance by tuning.
[00:02:04] Um and you can do that with an open
[00:02:06] model as opposed to closed models like
[00:02:08] Gemini. Essentially they're great out of
[00:02:10] the box, they're state of the art, um
[00:02:12] but and they're really general, but you
[00:02:14] may not be able to customize it as much
[00:02:15] beyond tuning uh I mean beyond prompting
[00:02:19] um and you know, system instructions of
[00:02:20] of that nature. So those are the
[00:02:22] benefits of using uh open models. Yeah,
[00:02:25] and also cost is also another
[00:02:27] consideration. You can take a look at
[00:02:29] this diagram that the more you use, if
[00:02:31] you're using uh
[00:02:32] a closed model like Gemini, uh it's the
[00:02:36] cost is increased per API call. Whereas
[00:02:39] if you're using open model like Gemma,
[00:02:42] the cost is not linear growth, right?
[00:02:44] Cuz it's based on the infra. Yeah.
[00:02:47] So coming back to this model strategy,
[00:02:50] um
[00:02:52] Yeah, there's there's many dimensions to
[00:02:54] to consider. We talked about a few of
[00:02:55] them, but this is just ones to keep in
[00:02:57] mind. But beyond that, it's also
[00:02:58] important to know that um the reason why
[00:03:00] we're so focused on model strategy is at
[00:03:02] the end of the day, um these models act
[00:03:05] as the brain behind uh your agents.
[00:03:08] Um so when you're using something like
[00:03:09] Google's Agent Development Kit, not only
[00:03:11] could you use Gemini as the brain behind
[00:03:13] these agents, you can use open models as
[00:03:15] well. So that's something that people
[00:03:16] sometimes they don't know, they think
[00:03:17] you can only use Gemini, but in reality,
[00:03:19] um you could pretty much use any model
[00:03:21] that you want because Google ADK uh
[00:03:23] comes with a light LM wrapper that
[00:03:25] allows you to kind of connect models as
[00:03:27] you see fit. Um so later on in this lab,
[00:03:30] we're going to learn how we can use
[00:03:31] Gemma 4 as the brain behind an agent.
[00:03:34] Yeah, so essentially agent is that
[00:03:36] you're using the model as the brain and
[00:03:38] then doing reasoning to pick which tool
[00:03:40] you want
[00:03:41] to pick to make a decision. And as you
[00:03:44] can see on this diagram, this is agent
[00:03:45] architecture. So the model you're
[00:03:47] choosing really
[00:03:49] like can determine the like the upper
[00:03:51] bound, the capability of your agentic
[00:03:54] system. That's why it's very important
[00:03:56] and you want to be smart to choose your
[00:03:58] model. And when you choose a model, you
[00:03:59] can think about the performance of the
[00:04:01] model, the use case you want and also
[00:04:04] the cost. You have different angle to
[00:04:06] pick your model smartly.
[00:04:08] And so this is the overall architecture
[00:04:11] we're going to dive into today. As you
[00:04:13] can see that on the on this right-hand
[00:04:15] side, we're going to start with this
[00:04:17] runtime. So today
[00:04:19] we will deploy Gemma model, Gemma 4
[00:04:22] model
[00:04:24] with service vLLM and Ollama. But yeah,
[00:04:27] IO, why we have these two different two
[00:04:30] different way? What is the real
[00:04:31] difference between Ollama and vLLM?
[00:04:34] Yeah, they're both LLM serving
[00:04:36] frameworks, but you tend to see Ollama
[00:04:37] used more in development use cases. It's
[00:04:39] really easy to install and get up and
[00:04:41] running. Um so it's great for
[00:04:42] experimental POCs. And you can also use
[00:04:45] it for multi-GPU support use cases. vLLM
[00:04:47] is great for production use cases. It
[00:04:49] comes with page attention. It's great
[00:04:51] for uh memory efficiency
[00:04:54] um and allows you to kind of do uh
[00:04:55] multiple concurrency um when it comes to
[00:04:57] calls and dynamic batching. So again
[00:05:00] again, so Ollama is great when it comes
[00:05:01] to development, uh vLLM is great for
[00:05:03] production. And there's other LLM
[00:05:05] serving frameworks as well like
[00:05:06] TensorRT, um LLM and such. So there's a
[00:05:09] lot of options to choose from um in the
[00:05:11] world, but for this lab we're focusing
[00:05:13] on Ollama and vLLM.
[00:05:15] And don't forget you can also deploy a
[00:05:16] model to what's AI through Model Garden.
[00:05:19] That's also another choice. It's a
[00:05:20] managed uh service for you. Yeah, so
[00:05:23] Ollama is very easy to install and it's
[00:05:25] very good for you to try things in your
[00:05:27] local development. And let's get started
[00:05:29] with Ollama.
[00:05:31] Uh so this is the As As you can see from
[00:05:34] this diagram, how what we want to do is
[00:05:36] we want to first pull the model from
[00:05:39] Ollama and then we want to build this
[00:05:41] image with Docker. So once we have this
[00:05:43] image, we're going to send it to the
[00:05:45] artifact registry, which is a container
[00:05:47] on Cloud. And you can essentially deploy
[00:05:49] the image so that you can
[00:05:51] have this image hosted on Cloud Run. So
[00:05:53] that's essentially how your agentic
[00:05:55] system agent going to use connect to
[00:05:57] your deployed
[00:05:59] Gemma 4. And if you if you're
[00:06:02] interested, let's let's get let's start
[00:06:04] by going through this lab.
[00:06:06] If you uh so we will have this link on
[00:06:09] the screen about what is this lab link
[00:06:12] about, but as usual, you know, like IO,
[00:06:15] usually we wanted to start with the
[00:06:16] equipment have the credit, but today
[00:06:18] we're going to skip the credit part.
[00:06:20] &gt;&gt; Yes. Yeah, we're today we're skipping
[00:06:21] the credits because this lab does
[00:06:23] require GPU um such as like when we're
[00:06:26] deploying to Cloud Run, we will be
[00:06:28] equipping our Cloud Run instances with,
[00:06:30] you know, L4
[00:06:32] um you know, accelerators and such.
[00:06:33] Because of that, um we won't be giving
[00:06:36] credits for this lab, but please feel
[00:06:37] free to follow along. You can use your
[00:06:39] own uh credit accounts um if you have
[00:06:41] them um or you can kind of sign up for
[00:06:43] free trial credits on Google Cloud
[00:06:45] Platform if you're a first-time uh
[00:06:47] sign-upper.
[00:06:48] Um but uh yeah, please feel free to
[00:06:49] follow along. As always, we want to
[00:06:51] start our environment our environment in
[00:06:54] Cloud Shell on Google Cloud. To open
[00:06:56] that, making sure you go to
[00:06:58] console.cloud.google.com
[00:07:00] and on the right top right, there's a
[00:07:02] button
[00:07:03] uh saying the activate Cloud Shell. Just
[00:07:05] click that
[00:07:07] and you will see
[00:07:08] um this
[00:07:10] Yes, it's similar to uh our VS Code, but
[00:07:13] it's on Cloud. Essentially it's a VM
[00:07:15] that uh hosting it.
[00:07:19] Yeah.
[00:07:20] IO, anything to add? Yeah, as you
[00:07:22] mentioned, so the Cloud Shell editor is
[00:07:24] essentially like a VS Code on Cloud and
[00:07:26] it's persistent over time. So any code
[00:07:28] that you develop or files that you
[00:07:30] create, you can come back to it a day or
[00:07:32] a week later. Um so please feel free to
[00:07:34] use it as your development environment
[00:07:35] and that's exactly what we're going to
[00:07:36] be doing for today's lab.
[00:07:37] Yeah, but one thing you need to notice
[00:07:39] is uh you will time out every 70 minutes
[00:07:41] or so for security reasons. So if you
[00:07:44] see any error for like IP like address
[00:07:47] missing or some weird issue or you want
[00:07:49] you ask you to re-authenticate, then
[00:07:51] just making sure to refresh the page to
[00:07:52] refresh the token so that it will keep
[00:07:55] you authenticated. Uh and to get
[00:07:57] started, let's just uh
[00:07:59] set up our environment so that we are
[00:08:01] ready to deploy and host our Gemma 4
[00:08:03] model.
[00:08:05] And as always, let's uh just copy this G
[00:08:07] Cloud OS. Let me zoom in.
[00:08:11] I'm going to copy this and then paste it
[00:08:13] to my terminal. So you can see this is a
[00:08:16] terminal. Let me paste it.
[00:08:18] So that making sure this Gmail account
[00:08:21] is the same account you're you have your
[00:08:24] uh billing account
[00:08:26] uh connected.
[00:08:28] And next we need to clone this two repo.
[00:08:31] We we are cloning those two repo and one
[00:08:33] is the Agent Verse Dungeon and another
[00:08:34] one is the Agent Verse DevOps SRE. Um
[00:08:39] yeah, maybe would you mind explaining to
[00:08:40] our audience in case they haven't
[00:08:42] watched our previous episodes, they
[00:08:44] don't know about the Agent Verse
[00:08:45] concept? Yeah, so we're cloning two
[00:08:47] different repos. The first one, Agent
[00:08:49] Verse DevOps SRE, that one has all the
[00:08:51] template files for like the agent we're
[00:08:53] going to be
[00:08:54] deploying later on, the Cloud YAML
[00:08:56] scripts that we're going to be using
[00:08:57] for, you know, um deploying um our uh
[00:09:01] images to artifact registry and such. Um
[00:09:03] so essentially it has a a bunch of
[00:09:04] staging and template files that kind of
[00:09:06] gets us up and running a lot quicker.
[00:09:07] The Dungeon repo has essentially the the
[00:09:10] boss um
[00:09:11] uh you know, dungeon and and uh files
[00:09:14] that we're using for the boss fight
[00:09:15] later on in the lab. So once we build
[00:09:17] our agent, essentially we're going to be
[00:09:19] building up to a boss fight where our
[00:09:21] agent is fighting with another agent in
[00:09:22] the cloud via A2A. Um so that one just
[00:09:25] has files so that we can kind of get
[00:09:27] that up and running. So by the time we
[00:09:28] get to that point, um our boss fight is
[00:09:30] ready to go. Yeah.
[00:09:33] Let's come back to this uh setup page.
[00:09:36] And next you need to initialize a new
[00:09:39] project so that
[00:09:41] you have a Google Cloud project ready.
[00:09:44] And you can see that it always starts
[00:09:45] with Agent Verse Guardian. You may have
[00:09:47] a different number here.
[00:09:50] Essentially this script is creating a
[00:09:52] Google Cloud project for you. And then
[00:09:54] it's trying to link the billing to this
[00:09:56] project. So you can see now how this
[00:09:59] full setup uh uh complete. But for uh
[00:10:01] you if you're running the script, you
[00:10:04] probably notice that you have this uh
[00:10:06] when you fetch the billing account, it
[00:10:08] has a fetch failure. That because it's
[00:10:10] looking for a child account. Um
[00:10:13] So, what you can do is if you happen to
[00:10:15] have a billing account with your credit
[00:10:17] card uh
[00:10:18] linked to it, um this is what you can do
[00:10:20] manually in Google Cloud Console. Okay,
[00:10:22] now you're at console.cloud.google.com.
[00:10:25] And then uh in the search bar, so I just
[00:10:28] click this search icon in the search
[00:10:30] bar, I will search uh resources. So,
[00:10:34] when I type resources, I have something
[00:10:36] called manage resources.
[00:10:38] So, when I open the manage resources,
[00:10:39] this is where you can manage all your
[00:10:41] project and its corresponding billing
[00:10:43] account. So, you you can select this
[00:10:45] Agent Workspace Guardian uh project. And
[00:10:48] here you can just uh click this button
[00:10:50] action and go to the billing. So, now
[00:10:53] this one it's already attached to the to
[00:10:55] my account. For you for your case, you
[00:10:57] probably see a pop-up window to see
[00:10:59] manage billing and then you can select
[00:11:01] the billing that has your um
[00:11:03] has your payment information linked to
[00:11:05] it. Next is as always, we want to um to
[00:11:08] uh
[00:11:09] config the project. And why we need to
[00:11:11] config the project? Yeah, we're just
[00:11:13] making sure that our project is set in
[00:11:15] the G Cloud uh
[00:11:16] um environment. So, um there's two ways
[00:11:18] you can kind of double-check if you're
[00:11:20] in the Cloud Shell, you want to make
[00:11:21] sure that you see your project ID in
[00:11:23] yellow. And beyond that, you also want
[00:11:25] to make sure that again, the G Cloud
[00:11:26] it's set to the right project. So, what
[00:11:28] we just did was making sure that the G
[00:11:29] Cloud uh is set to the right project,
[00:11:31] which should match your Agent Workspace
[00:11:33] Guardian uh {slash} {dash} some unique
[00:11:35] ID. Yeah. Mhm.
[00:11:39] And next, we need to enable some Google
[00:11:41] Cloud API. Uh as you can see that those
[00:11:44] are the If you take a look at the API we
[00:11:47] want to enable, it's including the
[00:11:48] storage API, platform. Basically,
[00:11:51] storage uh is you essentially you want
[00:11:53] to store your uh later on when we do
[00:11:56] VLM, we want to store our model in
[00:11:58] Google Cloud Storage. And when we want
[00:12:00] to deploy to Cloud Run, we want to
[00:12:02] enable Cloud Build. And we also want to
[00:12:05] have Artifact Registry to store our
[00:12:07] image, so we want to enable this. And
[00:12:10] yeah, essentially, we want to stay our
[00:12:13] store our API keys, so you want to
[00:12:14] enable Secret Manager. Yeah, anything
[00:12:16] you want to uh mention, Iul?
[00:12:19] Yeah, so the only thing I would add is
[00:12:20] that um just by enabling these APIs does
[00:12:23] not mean you're going to be charged
[00:12:24] immediately for these APIs. Essentially,
[00:12:27] you're just enabling them to be used in
[00:12:29] the project. A lot of people ask, "If I
[00:12:31] enable AI Platform Google APIs, for
[00:12:33] example, will I start being charged by
[00:12:35] the second?" Uh no, you won't. You're
[00:12:37] only going to be charged when you
[00:12:38] actually use the API. So, that's just
[00:12:40] one thing to keep in mind.
[00:12:43] And let's coming back to this. Yeah, so
[00:12:46] now we successfully finish enabling. And
[00:12:49] next is we need to create this artifact
[00:12:53] registry uh
[00:12:54] repository so that later on we can
[00:12:56] deploy our image to it.
[00:12:59] So, coming back to this uh diagram that
[00:13:02] we want to build the image uh for for
[00:13:05] like we want to first pull the model
[00:13:06] from Ollama and build the image and
[00:13:07] later on deploy this to image uh
[00:13:11] repository. Yeah, Iul, do you know why
[00:13:13] we want to have this design? Like uh can
[00:13:16] we Is there any other way we can do?
[00:13:19] Yeah, this is just uh best practice when
[00:13:20] it comes to um you know, CI when it
[00:13:23] comes to Google Cloud where essentially
[00:13:24] you're building an image, you're storing
[00:13:26] it in Artifact Registry, you're
[00:13:27] deploying it to Cloud Run, and it's
[00:13:29] essentially this is the build process
[00:13:30] that we're going to be enabling with
[00:13:32] Cloud Build um that allows us to kind of
[00:13:34] programmatically specify each of these
[00:13:35] steps. And then we can go ahead and just
[00:13:38] execute that Cloud Build YAML file. So,
[00:13:40] you're going to see that later on once
[00:13:41] we get to that step.
[00:13:42] Yeah, and also you can see that the
[00:13:45] essentially we directly build it cuz we
[00:13:47] do not have to store our model anywhere
[00:13:49] cuz it's baked in in Ollama. You will
[00:13:52] see it really soon in our our lab. Yeah.
[00:13:56] And uh
[00:13:59] Yeah, so now we have this repo
[00:14:02] create like artifact repository created.
[00:14:05] And next one is set up the permission.
[00:14:08] And Iul, do you know what is service
[00:14:10] account? Why we need to grant this role
[00:14:12] to the service account? Yeah, great
[00:14:14] question. So, every Google Cloud project
[00:14:16] has a default service account. And um
[00:14:18] that's essentially going to be like the
[00:14:20] operator behind many um of your default
[00:14:22] actions. So, if we're uploading files to
[00:14:24] Cloud Storage or um you know, uh
[00:14:27] executing a Cloud Build deployment, you
[00:14:29] want to make sure that the default
[00:14:30] service account has certain permissions.
[00:14:31] So, that's pretty much all we're doing
[00:14:32] here. We're making sure that the the
[00:14:34] default service account has the ability
[00:14:36] to uh interact with Cloud Storage, has
[00:14:38] the ability to uh initiate Cloud Build
[00:14:41] jobs, has the ability to uh write logs
[00:14:44] and read the logs, um has the ability to
[00:14:46] interact with Secret Manager, which
[00:14:48] we're going to be using later on for
[00:14:49] storing our Hugging Face uh Secret
[00:14:51] Manager key. So, as Annie just mentioned
[00:14:53] for Ollama, we're going to be baking in
[00:14:55] the model directly into the um uh
[00:14:58] container image. But when we actually
[00:14:59] use VLM, we're going to be doing a
[00:15:00] different approach. We're going to be
[00:15:02] storing the model weights directly in
[00:15:03] Cloud Storage and pulling those model
[00:15:05] weights from Hugging Face. Um so,
[00:15:07] there's different approaches that are
[00:15:08] kind of um being enabled through this
[00:15:10] IAM permissioning.
[00:15:12] Yeah, one metaphor I can think of is you
[00:15:14] can think of service account like a
[00:15:15] robot account Yeah.
[00:15:18] of yourself. And then you have different
[00:15:20] robot controlling different permission.
[00:15:22] And so that you can manage the project
[00:15:25] permission.
[00:15:26] And here we're using the same account
[00:15:28] for easy demo. But in production, you
[00:15:32] can have different robot account like
[00:15:33] different service account for different
[00:15:34] permission
[00:15:36] configuration.
[00:15:37] And the last step is to uh warm up. As
[00:15:40] we need to run this warm up.sh uh
[00:15:43] warm up.sh script. So, essentially, we
[00:15:46] want to essentially using GCS FUSE for
[00:15:49] our VLM deployment, we want to run this
[00:15:51] warm up script uh here to warm up our
[00:15:55] GCS FUSE cache.
[00:15:56] And you If you want to know what is GCS
[00:15:58] FUSE and why we want to use that, uh
[00:16:00] stay tuned. We want to talk We will talk
[00:16:02] about it in VLM deployment. Yes, yeah.
[00:16:07] Now, it's finished.
[00:16:09] Let's start host our Gemma for uh
[00:16:13] Ollama. Let's get started. All right, so
[00:16:15] let's get start. Uh so, first we want to
[00:16:18] pull the image from Ollama. As uh Iul
[00:16:21] mentioned earlier, you know, Ollama is
[00:16:23] great for local development and it's
[00:16:25] great for quickly testing uh the any
[00:16:27] model because you know, Gemma for is
[00:16:29] baked in
[00:16:30] in Ollama. And you can see it's very
[00:16:32] easy like first we want to create a
[00:16:34] Dockerfile, build the image. And we just
[00:16:37] With only this line of the code, you
[00:16:39] just need to run Ollama
[00:16:42] and uh pull the this Gemma for
[00:16:45] from Ollama. So, now you can just uh
[00:16:48] have this model from Ollama. So, it's
[00:16:50] very straightforward.
[00:16:52] And uh just copy this
[00:16:55] and coming back to my terminal and paste
[00:16:58] it.
[00:17:00] So, now we just create a Dockerfile
[00:17:03] folder. And what's next is we want to
[00:17:06] create this Cloud Build YAML file. So,
[00:17:09] Iul, maybe you can explain um what is
[00:17:11] Cloud Build YAML file before we explain
[00:17:14] uh what are inside the Cloud Build YAML
[00:17:16] file. Yeah, yeah. So, as I mentioned
[00:17:17] before, Cloud Build is essentially the
[00:17:19] engine for CI/CD on on Google Cloud. So,
[00:17:22] essentially, it allows you to
[00:17:23] programmatically specify um steps you
[00:17:25] want to run as part of a as a process.
[00:17:28] So, pretty much all we're doing here is
[00:17:29] we just created the Dockerfile that
[00:17:31] defines our container image. Now, we're
[00:17:33] going to build the container image in
[00:17:34] step one. We're going to push the
[00:17:36] container image to Artifact Registry in
[00:17:38] step two. And then we're going to deploy
[00:17:40] that container image to Cloud Run
[00:17:42] in step number three. So, that's all
[00:17:44] we're we're specifying here in the Cloud
[00:17:46] Build YAML file. Yeah, so basically,
[00:17:48] it's like a blueprint file to specify
[00:17:50] all the step you need to do and exactly
[00:17:52] we're showing on this diagram. So, we
[00:17:54] just did is we just uh pull we have this
[00:17:57] uh Dockerfile to explain how to pull
[00:17:59] this image. So, you want to build this
[00:18:01] image and then and then put push to
[00:18:03] Artifact Registry and deploy the image.
[00:18:05] It's like put it's like a blueprint file
[00:18:08] to uh including all this process
[00:18:11] uh we want to have over here.
[00:18:13] And let's just uh
[00:18:15] copy this and uh coming back to our my
[00:18:18] terminal and paste it. But Iul, why we
[00:18:21] want to set the CPU to be four and why
[00:18:24] we want to be like concurrency to be
[00:18:25] four? For all those setting, anything we
[00:18:27] need to be aware when we trying to
[00:18:29] deploy our image to um Cloud Run? Yeah,
[00:18:32] um Cloud Run is a really powerful
[00:18:34] serverless platform and gives us a lot
[00:18:35] of configuration capability. Yeah, so as
[00:18:37] you see here, we're set we're specifying
[00:18:39] four CPU um minimum for each machine of
[00:18:42] the service. Um we're specifying memory
[00:18:44] to be at least 16 GB, which is really
[00:18:45] important. If we're going to be storing
[00:18:48] um Ollama or uh Gemma for uh model on
[00:18:51] the image, um you have to have a a lot
[00:18:54] of um memory capacity. Um so, we're
[00:18:56] working with a 2B um um version of Gemma
[00:18:58] for. Um so, 16 GB is uh sufficient um
[00:19:02] memory for that. So, that's why we're
[00:19:03] specifying that.
[00:19:05] Um we're specifying that we want to use
[00:19:06] the Nvidia L4 GPU type. Um we're
[00:19:09] specifying concurrency to four. We want
[00:19:10] to allow up to four parallel calls
[00:19:12] against the service.
[00:19:14] Um and yeah, so again, uh Cloud Run
[00:19:16] gives us a lot of configuration
[00:19:17] capabilities and we're just trying to
[00:19:19] optimize um for how we're going to be
[00:19:20] using it in the lab. As you can see at
[00:19:22] the bottom, we have min instances equals
[00:19:24] one, max instances equal to one. That's
[00:19:26] not going to be too common in
[00:19:27] production. You want to be able to scale
[00:19:29] beyond one machine. Um but for cost
[00:19:31] purposes, um um just so you're not kind
[00:19:33] of allocating more GPUs than you need,
[00:19:35] we're kind of just minimizing to one
[00:19:37] machine per service for this lab.
[00:19:40] Yeah, also we have this allow
[00:19:42] unauthenticated for this uh lab purpose,
[00:19:44] but you can like make it authenticated
[00:19:47] for security reason for your actual um
[00:19:50] image deployment.
[00:19:52] All right, so next one is we want So now
[00:19:55] we configure this Cloud Build YAML file.
[00:19:57] So next step is actually, you know,
[00:19:59] follow this
[00:20:00] this blueprint in the Cloud Cloud Build
[00:20:02] YAML file and then finish this process
[00:20:04] through this Cloud Build. So just uh
[00:20:06] copy this. Um basically, you put this uh
[00:20:08] Cloud Build YAML file in the specific
[00:20:10] file and then do the setting with the
[00:20:12] region and the repo name project ID you
[00:20:15] have. And let's just uh go ahead and go
[00:20:18] to our terminal and go ahead to deploy
[00:20:21] the whole process.
[00:20:23] You know, if you want to track the
[00:20:24] process after we can also go to Cloud
[00:20:27] um Google Cloud Console and the Cloud
[00:20:30] Build to see the process.
[00:20:32] So now you can see that um
[00:20:34] we just finished environment setup and
[00:20:36] now we're waiting for the build to
[00:20:38] complete.
[00:20:39] It's like trying to pull in the
[00:20:41] interval. So it's basically following
[00:20:42] the uh process like trying to first
[00:20:45] build the image through Docker. Yeah,
[00:20:48] and keep in mind uh this Cloud Build uh
[00:20:50] process will take um some time. So uh
[00:20:54] this step may take anywhere from 15 to
[00:20:56] 20 minutes depending on how long things
[00:20:58] take. So um feel free to take a coffee
[00:21:00] break and uh
[00:21:02] go grab some coffee. Um but uh yeah,
[00:21:04] we'll we'll be back once our uh Cloud
[00:21:07] Build job completes. Yeah, it finished
[00:21:09] finally. And uh as you can see that we
[00:21:12] can go to Google Cloud Console to also
[00:21:14] see the process um
[00:21:16] uh like you can search Cloud Build, we
[00:21:18] can see the process
[00:21:20] we just had
[00:21:22] earlier.
[00:21:24] And
[00:21:28] yeah, this is a building process
[00:21:30] we just uh having cuz we have two
[00:21:32] building process. One is for Dungeon,
[00:21:33] another one is for
[00:21:35] um this deployment. You can also see
[00:21:38] uh this
[00:21:40] image is uh industry deployed to Cloud
[00:21:43] Run. So let's just go to Cloud Run
[00:21:45] making sure that on the top left it's
[00:21:48] selecting the project and go through the
[00:21:50] Gemma Ollama big service. And here we
[00:21:52] go. We have this
[00:21:54] We have this URL that later we can
[00:21:56] connect to our agent. Okay, so now you
[00:21:59] have this URL, right? We have this URL
[00:22:01] and we want to verify this is working
[00:22:04] by sending it the post request. So here
[00:22:07] basically, what you want to do is this
[00:22:09] step, you know, this Ollama URL, this
[00:22:11] step uh is to try to grab that URL. You
[00:22:13] can also grab this URL just by copy this
[00:22:16] um but here this is a command for you to
[00:22:18] grab this URL. And once you have this
[00:22:20] URL, you're trying to test this URL by
[00:22:22] sending this prompt.
[00:22:24] As a guardian of Aetherius, what is my
[00:22:26] primary duty? Or you can send anything
[00:22:28] else and then what you expect to do is
[00:22:30] expected behind the scenes is you want
[00:22:32] uh this Gemma 4 model and like answering
[00:22:35] this question. And let's see what is the
[00:22:37] response. Let's me copy this and paste
[00:22:40] it to the terminal.
[00:22:45] Time to verify if everything's working.
[00:22:49] So and now all it's doing is resetting
[00:22:51] the environment variables
[00:22:53] um cuz we're running that set env.sh
[00:22:56] [clears throat] file each time just to
[00:22:57] make sure that in case you lose context
[00:22:59] cuz the build process takes a long time.
[00:23:01] So throughout this lab, we're setting
[00:23:03] that set env multiple times at the very
[00:23:05] top. So that's the reason why it takes a
[00:23:07] little bit longer for each step um but
[00:23:09] it's just important to run just in case
[00:23:11] you lose any context. And then yeah,
[00:23:13] it's going to print out the Cloud Run
[00:23:15] URL and then we're going to call the URL
[00:23:17] and see if we can get a response from
[00:23:19] the from the LLM.
[00:23:21] Yeah, so you have this URL and then
[00:23:24] can send a post request.
[00:23:27] We are expected to see a response look
[00:23:29] like this. But maybe you're not exactly
[00:23:32] same response here because, you know, AI
[00:23:35] cannot generate the same result every
[00:23:38] single time. But oh, let's see. This is
[00:23:39] the result.
[00:23:41] Oh, wow.
[00:23:43] Okay, here. Oh, yeah, the context.
[00:23:47] Oh, here's the result. This is the
[00:23:49] response. As a guardian of the
[00:23:50] Aetherius,
[00:23:52] the primary duty is this. Safeguard
[00:23:55] because of the Aetherius representing
[00:23:56] reality.
[00:23:59] Great. So that means the Gemma 4
[00:24:01] uh on Cloud Run with Ollama is working.
[00:24:04] All right. So I uh you know that we are
[00:24:06] using Ollama and it has it's really easy
[00:24:09] to get started and it's really easy to
[00:24:10] use and we have this model baking so
[00:24:12] that we have really fast cold start. You
[00:24:14] do not have to like start uh waiting for
[00:24:17] it to loading the model and to have the
[00:24:18] initial cold start problem. However, you
[00:24:21] have some disadvantages, right? So I
[00:24:23] will um
[00:24:24] what are some disadvantages with this
[00:24:26] Ollama use case?
[00:24:28] Oh yeah, so since we're baking in the
[00:24:29] model into the image, as you mentioned,
[00:24:32] it leads to very fast cold starts
[00:24:33] because the fact that the image is
[00:24:35] already deployed. Essentially, if you
[00:24:36] want to create a new uh version um of a
[00:24:39] or new instance of that machine for the
[00:24:41] service, it's really easy to spin up. Uh
[00:24:43] in our particular use case, we're only
[00:24:45] limited to one, but if we were, it would
[00:24:46] be really easy to spin up more instances
[00:24:48] for the service. But the downside to
[00:24:50] that is because we're baking it into the
[00:24:51] container image, if you want to change
[00:24:53] the model version or the parameters of
[00:24:56] the model, say you want to go from 2B um
[00:24:58] to a a larger version of the same uh
[00:25:00] model to a different model, you have to
[00:25:02] rebuild the image and then redeploy. Um
[00:25:05] so it's a it's a it's a long process and
[00:25:07] as you you saw, um building these images
[00:25:09] can take some time. Um so as I mentioned
[00:25:12] before, through the different
[00:25:13] development use cases, oftentimes when
[00:25:14] you're running these models locally, you
[00:25:16] may want to use Ollama.
[00:25:17] Uh
[00:25:18] but if you're baking it into the
[00:25:20] container image, it can be pretty
[00:25:22] inflexible uh when it comes to kind of
[00:25:25] rapid changes. But of course, when
[00:25:27] you're using something like Cloud Build,
[00:25:28] you can automate the changes to an
[00:25:29] extent. Um but uh yeah, that's just one
[00:25:32] thing to keep in mind. Yeah, also
[00:25:33] another uh another thing worth
[00:25:36] mentioning is if your production use
[00:25:38] case serve huge traffic and you want to
[00:25:40] improve the performance, that is where
[00:25:43] you should really consider using V RAM.
[00:25:46] And different from Ollama, Ollama has a
[00:25:49] model baking. But here you want to grab
[00:25:51] the model from Hugging Face and save
[00:25:54] that to Cloud Storage. And then, you
[00:25:57] know, this process is a little bit
[00:25:58] similar. We trying to You know, we we
[00:26:00] have this model the CI pipeline is kind
[00:26:03] of similar. You want to build the image,
[00:26:04] but this image it do not does not
[00:26:06] contain the model. It only contain the V
[00:26:09] RAM code. And then once you um
[00:26:11] uh save that, push that to the image
[00:26:14] repository and then deploy them to Cloud
[00:26:16] Run.
[00:26:17] And now you can see that the container
[00:26:19] image is tiny because you only have V V
[00:26:22] RAM code. And then the Gemma is going to
[00:26:25] store in the Google Cloud Storage and
[00:26:27] then we using Cloud Storage FUSE to
[00:26:29] mount the bucket as a local folder. So
[00:26:31] anything you change in the local folder
[00:26:33] will reflect it. I okay explain more
[00:26:35] about Cloud Storage FUSE?
[00:26:38] Oh yeah, so Cloud Storage FUSE is a
[00:26:39] great way of representing uh Cloud
[00:26:41] Storage folders and paths as local paths
[00:26:44] for your machine uh for the Cloud Run
[00:26:46] service. And that's what makes it so
[00:26:47] efficient. So as far as any um you know,
[00:26:50] package or uh service that's running on
[00:26:52] the Cloud Run service is concerned, it
[00:26:54] can actually access uh GCS files the
[00:26:57] same way that it would access local
[00:26:59] files, temp files that are running
[00:27:00] directly on the machine. Uh so Cloud
[00:27:02] Storage FUSE is essentially what
[00:27:03] mediates that connection between the
[00:27:05] Cloud Storage bucket and it being
[00:27:07] mounted as a local folder for access uh
[00:27:11] directly on the on the Cloud Run
[00:27:13] machine.
[00:27:14] Uh yeah.
[00:27:15] So anything we change in the local
[00:27:17] folder will also reflect here, right?
[00:27:19] Exactly. Yeah, so and what makes it
[00:27:21] really powerful is that not only could
[00:27:23] you read from that local folder that's
[00:27:24] been mounted uh the same way that you
[00:27:26] would read from like a GCS bucket, any
[00:27:28] files that you write to that local
[00:27:29] folder is almost as if you're writing to
[00:27:31] the GCS bucket as well for persistence
[00:27:34] uh down the line. So it's bidirectional
[00:27:36] sync.
[00:27:37] Yeah, bidirectional. Yeah.
[00:27:38] Yeah, pretty cool. And let's take into
[00:27:41] how we going to save the model to Cloud
[00:27:44] Storage and how to go through all the CI
[00:27:46] pipeline and set up that Cloud uh and
[00:27:50] set up that Cloud Storage FUSE.
[00:27:52] Let's get to step step five. All right,
[00:27:56] let's get started by first download this
[00:27:57] model from Hugging Face and then save
[00:27:59] that to Cloud Storage. So let's get
[00:28:01] started. And what you need to do is
[00:28:03] first you need to go to step five.
[00:28:06] And when you're scrolling down and you
[00:28:08] can see that we have instructions here.
[00:28:11] If you don't have a Hugging Face
[00:28:12] account, you can just create a account
[00:28:15] over here.
[00:28:16] Or if you can create account over here.
[00:28:18] If you already have it, you can just uh
[00:28:20] click uh login.
[00:28:23] And you now you're in this page
[00:28:25] and to login. And what's next is you
[00:28:27] need to click in this link to generate
[00:28:30] uh a token.
[00:28:32] So now I'm at this page. I'm going to
[00:28:33] click generate a new token. So uh you
[00:28:37] can use Aetherius workshop token as a
[00:28:39] name or any name you want. I'm just copy
[00:28:41] here for the Aetherius workshop name.
[00:28:44] When it comes to the permission, uh you
[00:28:46] can just use the read role. So we can
[00:28:49] choose read for this use case and create
[00:28:51] a token. And now you have this token
[00:28:53] ready. I just copy this to to save it.
[00:28:56] So yeah, next thing we want to do is we
[00:28:58] want to run this uh command so that it
[00:29:00] will save the token to uh Secret
[00:29:02] Manager.
[00:29:04] And the first we just copy this command
[00:29:06] and then going going back to our
[00:29:07] terminal, I will paste it. So first we
[00:29:10] want to enable this script uh and then
[00:29:13] we want to run the script. Essentially,
[00:29:14] behind the scenes is we want to save the
[00:29:16] token to Secret Manager. And uh I uh do
[00:29:19] you know what is Secret Manager? Might
[00:29:21] explain to everyone what is Secret
[00:29:23] Manager? Great question. So Secret
[00:29:24] Manager is a essentially um
[00:29:28] it's um it's it's eponymous. It's the
[00:29:30] speaks for its name. It's um our best
[00:29:32] practice way for managing secrets, API
[00:29:34] keys uh in in a Google Cloud context. So
[00:29:37] if you're working in a Google Cloud
[00:29:39] environment, um rather than you storing
[00:29:41] your API keys as environmental variables
[00:29:44] or um Um, you know, sometimes uh really
[00:29:46] not good practice is to embed a direct
[00:29:48] into the file. What we can do with
[00:29:50] something like Secret Manager is, um,
[00:29:51] you can call the Google Cloud uh, Secret
[00:29:53] Manager API or there's like Python SDK
[00:29:57] and then you can actually pull the
[00:29:58] secret, um, during your actual runtime
[00:30:01] into your application. Um, so it's a way
[00:30:03] of preventing you from having to
[00:30:04] actually kind of make visible your
[00:30:05] secrets in, uh, like a directly in the
[00:30:08] code or having to store it in an
[00:30:10] environmental file. That adds more data
[00:30:12] governance issues cuz now you have to
[00:30:13] start managing the environmental files
[00:30:15] and make sure that they don't get
[00:30:15] pushed, um, to uh, you know, uh, your
[00:30:18] code versioning repo, stuff like that.
[00:30:20] Um, so overall, Secret Manager is the
[00:30:21] best practice way for storing and
[00:30:23] managing your application secrets. All
[00:30:26] right. So now if you're coming back,
[00:30:27] it's asked you to paste your Hugging
[00:30:29] Face token. Uh, so what we want to do is
[00:30:31] we just want to copy the token here and
[00:30:34] and paste it over here. You don't see
[00:30:35] anything. Uh, so if you happen to paste
[00:30:38] it wrong, you can go to, uh, Secret
[00:30:41] Manager here and delete the token and
[00:30:43] redo it or you can update a token.
[00:30:49] And once it's finished, you will see
[00:30:51] the, uh, token saved in Secret Manager
[00:30:53] in Google Cloud console over here.
[00:30:58] All right. It says, uh,
[00:31:00] success and we can double check by
[00:31:02] refresh it.
[00:31:06] And yeah, we have this token created.
[00:31:09] And we have this one version. And if you
[00:31:11] want to see the value, you can also see
[00:31:12] view uh, value just verify this value is
[00:31:15] correct, is a correct token you just
[00:31:17] copied.
[00:31:19] So once it's verified, all right. So we
[00:31:21] just download the model from Hugging
[00:31:23] Face and we have this token saved to
[00:31:26] Secret Manager. What's next is you want
[00:31:28] to save this model to Cloud Storage. So
[00:31:31] how to do that?
[00:31:33] First, uh, you need to create this uh, G
[00:31:36] Cloud Cloud uh,
[00:31:37] Cloud Storage bucket using this command
[00:31:40] to create a Cloud Storage. And next is
[00:31:42] you're making sure the permission is
[00:31:44] ready. So I'm just, uh,
[00:31:46] uh, copy this command to prepare my
[00:31:48] Cloud Storage so that later I can save
[00:31:51] my model to Cloud Storage.
[00:31:53] Yeah. Now I finished. So, uh, we can
[00:31:56] verify it by go to Google Cloud Storage.
[00:32:00] Star Cloud Storage.
[00:32:04] You can search Cloud Storage here.
[00:32:06] And making sure we select, uh, agent
[00:32:08] verse. And here in the bucket,
[00:32:12] uh, as you can see that we have two
[00:32:14] Cloud Storage already. So this is the
[00:32:17] latest one cuz we have the previous one
[00:32:18] for, uh, our
[00:32:21] we have the previous one for our dungeon
[00:32:23] deployment.
[00:32:26] And yeah, we have this, uh, Guardians
[00:32:28] uh, storage ready so that later we can
[00:32:31] push, uh, and then we can push our model
[00:32:33] here.
[00:32:34] I hope you can see we have Cloud Build
[00:32:37] YAML file again. What is this file do?
[00:32:41] Yeah, great question. So what we're
[00:32:42] doing here is essentially we're not
[00:32:44] going to go through the Cloud Build
[00:32:45] process of actually
[00:32:47] specifying the model that we want to
[00:32:48] download, um, checking if the bucket
[00:32:51] exists. So that's step number one. You
[00:32:52] want to make sure that we've actually
[00:32:53] created the bucket and that's set as
[00:32:54] part of the environmental variable.
[00:32:56] That's all going to be true. Um, two, we
[00:32:58] actually now want to download it
[00:32:59] actually from Hugging Face. Uh, so we're
[00:33:02] download based off the ID. We're pip
[00:33:04] installing the Hugging Face, uh, uh,
[00:33:06] hub, uh, library.
[00:33:08] Um, we're authenticating with the token
[00:33:10] that we downloaded, um, and save this as
[00:33:12] part of Secret Manager. And then we're
[00:33:14] downloading the model and we're
[00:33:15] specifying that it should save to, um,
[00:33:18] our local directory. Again, we're using
[00:33:19] GCS Fuse here. Remember earlier on in
[00:33:21] the setup we did the warm-up, uh, for
[00:33:23] the GCS Fuse cache. Um, and we're
[00:33:25] specifying the model ID and then
[00:33:27] ultimately just copying that model to
[00:33:29] the GCS bucket. Um, and yeah.
[00:33:33] Great. So let's go ahead and create this
[00:33:36] Cloud Build download YAML file so that
[00:33:38] we can continue. Let's continue. And
[00:33:41] first,
[00:33:42] you will create this Cloud Build, uh,
[00:33:44] Cloud Build download YAML file
[00:33:47] for us to follow. This will take about,
[00:33:49] uh, anywhere from two to three minutes.
[00:33:51] It's a pretty quick process here.
[00:33:53] Yeah. So here we're just creating this
[00:33:55] Cloud Build download file, uh, with our
[00:33:57] command.
[00:33:59] And next is let's using G Cloud Build
[00:34:02] uh,
[00:34:03] G G Cloud Build command to run this
[00:34:07] it will actually do all the process we
[00:34:09] wrote in the blueprint.
[00:34:11] So let's go ahead and copy this.
[00:34:14] Yeah, so while we're waiting, we can
[00:34:15] just the mapping each of the step, uh,
[00:34:18] to our diagram over here.
[00:34:21] Uh, as I I'll mention earlier that first
[00:34:24] step is making sure my our model bucket
[00:34:27] exists. So this is like a pre-check. And
[00:34:31] once we have the model to log in to
[00:34:32] Hugging Face and using the token, so
[00:34:34] basically this is the step we want to
[00:34:36] like making sure we get access to
[00:34:37] Hugging Face.
[00:34:39] And then we copy the model, uh, download
[00:34:41] the model to GCS bucket. So this this is
[00:34:43] the next step is we want to like once we
[00:34:45] have the token, we download the model
[00:34:47] and then from the GCS bucket.
[00:34:50] And once we, uh,
[00:34:52] have this, we want to make sure the
[00:34:54] secret available for this built
[00:34:56] environment. Yeah, I finished.
[00:34:58] So what we done so far is, you know, we
[00:35:01] are have this token so that we can
[00:35:03] install this model and copy the model
[00:35:05] and save everything to the Google Cloud
[00:35:07] Storage. So this is what we done so far
[00:35:10] with
[00:35:12] this, um,
[00:35:14] with this Cloud Build download YAML
[00:35:16] file. So this is basically the
[00:35:17] downloading processing and we can verify
[00:35:20] everything in the bucket.
[00:35:23] I'm going to refresh the
[00:35:25] Everything downloaded in your Cloud
[00:35:27] Storage.
[00:35:29] Great.
[00:35:31] What's next is
[00:35:36] Oh, you can also verify Cloud, uh,
[00:35:39] GCS bucket with a command over here.
[00:35:42] You can just copy this with a G Cloud
[00:35:45] uh, storage LS command to recursively
[00:35:47] verify things in the G Cloud
[00:35:49] bucket. There's another way to verify.
[00:35:52] all the weights downloaded, the
[00:35:53] optimizers, all of that. Um, so yeah,
[00:35:56] it's just listing out the files.
[00:36:00] So now we verified it.
[00:36:02] The next thing is we need to
[00:36:05] So the next thing is we need to finish
[00:36:07] this, uh,
[00:36:08] pipeline.
[00:36:10] So I don't know what is, uh, when we
[00:36:12] when we talk about network subnet, what
[00:36:14] is the subnet and why we need to, uh,
[00:36:17] compute this network subnet here? Yeah,
[00:36:19] great, uh, question. So private Google
[00:36:21] access is a great, um, kind of, uh, tool
[00:36:24] and feature that you can use, uh, when
[00:36:26] you have different services
[00:36:27] communicating with each other. In our
[00:36:29] use case, what we have is our model
[00:36:30] weights being stored in Cloud Storage
[00:36:32] and then we're going to have a deployed,
[00:36:34] uh, model on Cloud Run.
[00:36:36] Uh, we want to be able to pull these
[00:36:38] weights without these weights having
[00:36:39] without the data having to traverse over
[00:36:41] the public internet. Um, to kind of
[00:36:43] accomplish that, we're going to enable
[00:36:44] private Google access. So this will
[00:36:46] allow our Cloud Run service to
[00:36:47] communicate with our GCS, um, files
[00:36:50] without actually having to pull the data
[00:36:52] over the public internet. So it's going
[00:36:53] to traverse to our private subnet. Um,
[00:36:55] so it's a really, um, smart way of kind
[00:36:57] of keeping data secure when you have,
[00:36:59] again, connections between different
[00:37:00] services on Google Cloud. In our use
[00:37:02] case, we have, uh, Cloud Run
[00:37:04] communicating with, uh, Cloud Storage to
[00:37:06] pull the model weights. Uh, so that's
[00:37:08] the benefit of that.
[00:37:10] Yeah, so you can see we have this line
[00:37:12] over here, Cloud Run pull from Cloud
[00:37:14] Storage. All right. So let's just copy
[00:37:16] this and
[00:37:18] continue. All right. So we should
[00:37:21] continue, uh, once we download this
[00:37:23] model and we set up VPN, a VPC.
[00:37:26] And, uh, next we want to configure our
[00:37:29] CI pipeline.
[00:37:31] Uh, so I don't know why we want to like
[00:37:35] create a Docker file for this VLM and
[00:37:38] everything. Like what what are what are
[00:37:40] they? Why we why need why we need to do
[00:37:42] all those process here with Docker file?
[00:37:45] doing in the very first step, since
[00:37:47] Gemma 4 just was released just last
[00:37:50] week, um, there's actually, uh, a
[00:37:52] version of the VLM, uh, you know, image
[00:37:55] that's kind of specialized for Gemma 4.
[00:37:57] So what essentially we're pulling is the
[00:37:58] Gemma 4 version of VLM just so it's
[00:38:00] optimized for, you know, inference with
[00:38:02] Gemma 4. And then what we now want to do
[00:38:05] is make sure that we're using a
[00:38:06] Transformers, uh, library that's, uh,
[00:38:08] compatible with the newest version of
[00:38:10] Gemma 4. So what we're doing is making
[00:38:12] sure that we are, uh, setting the right
[00:38:14] version of the Transformers library uh,
[00:38:16] to a version that's compatible with
[00:38:18] Gemma 4. And then all we're doing
[00:38:20] afterwards is cleaning up any default
[00:38:21] models that were pulled and uh, setting
[00:38:23] the environment, um, as part of the, you
[00:38:26] know, uh, development process. And then
[00:38:29] we're setting the entry point for the
[00:38:30] VLM server when it's being deployed on
[00:38:32] Cloud Run and that's it. So pretty much
[00:38:34] all we're doing again is we're, uh,
[00:38:36] specifying the VLM, uh, default
[00:38:38] container image that we want to use, one
[00:38:40] that's specialized for Gemma 4. We're
[00:38:42] making sure that our Transformers
[00:38:43] library is, uh, compatible from a
[00:38:45] version standpoint. And then we're just
[00:38:47] doing some cleanup afterwards and then,
[00:38:50] uh, specifying the entry point for the
[00:38:51] Cloud Run service.
[00:38:53] Yeah, how do we know the right
[00:38:55] Transformer for the version for this
[00:38:58] Gemma 4 VLM? Or how do we change it for
[00:39:00] different model?
[00:39:02] Yeah, great question. So there's
[00:39:03] multiple ways you can do this.
[00:39:04] Sometimes, uh, if you just want to kind
[00:39:06] of, uh,
[00:39:07] be a little bit more general, you can
[00:39:09] just say, uh, pip install Transformers,
[00:39:12] uh, uh, dash dash upgrade and that'll
[00:39:13] kind of make sure that you're installing
[00:39:15] the very latest version. Uh, other times
[00:39:17] you can look at the documentation and
[00:39:18] see what uh, version of the library was
[00:39:20] used for a particular model. So if you
[00:39:22] look at the Gemma 4 documentation for
[00:39:24] VLM, you'll notice that it's using 5.50.
[00:39:26] So it's just a good way to be
[00:39:27] consistent, um, but, uh, yeah.
[00:39:30] Got it. Thank you. So let's configure it
[00:39:34] by coding this Docker file. Okay, so now
[00:39:37] we want to create this Cloud Build this
[00:39:40] pipeline. So to create this pipeline,
[00:39:42] basically is like we want to define a
[00:39:44] blueprint for this whole process. And
[00:39:46] the first is, as always, we want to
[00:39:48] build the image with
[00:39:50] Docker. So, we want to build this image.
[00:39:52] So, we have this image with VLM.
[00:39:55] And then, next is you want to push this
[00:39:57] to
[00:39:59] artifact registry like this. And then,
[00:40:02] what's next step is you want to deploy
[00:40:05] everything, you know, the service and
[00:40:07] VLM fuse service to Cloud Run. So, while
[00:40:10] I'm deploying,
[00:40:12] uh I'm going to copy this. I'm going to
[00:40:14] pre-create this cloudbuild.yaml file.
[00:40:16] Oh, I do we have different setting here
[00:40:18] for VLM compared to Olama
[00:40:21] uh setting previously?
[00:40:23] &gt;&gt; Great Great question. It's pretty
[00:40:24] similar. There are some slight
[00:40:25] differences, um especially because we're
[00:40:27] taking a mounted approach with VLM. So,
[00:40:29] as I mentioned before, we have the model
[00:40:31] weights in GCS, and we're mounting it um
[00:40:34] uh on the Cloud Run machine. So, there's
[00:40:36] a few extra parameters for that
[00:40:37] mounting. But beyond that, when you
[00:40:39] actually look at the machine sizing, the
[00:40:40] memory, the CPU, it's uh it's the same.
[00:40:42] And the reason why is because we're
[00:40:43] pretty much using the same exact model
[00:40:46] with the same exact amount of
[00:40:47] parameters. So, the same memory
[00:40:48] constraints are the same across Olama
[00:40:50] and VLM. But as I mentioned before, we
[00:40:52] have a few other parameters to kind of
[00:40:54] one address the private Google access
[00:40:56] that we enabled, so to make sure that we
[00:40:57] can kind of communicate with Cloud
[00:40:59] Storage over private network. And then,
[00:41:02] two, to kind of actually mount the the
[00:41:04] Cloud Storage uh you know, bucket
[00:41:07] as a local path. So, you can kind of see
[00:41:09] there's some volume mounts that have
[00:41:10] been added as parameters. But beyond
[00:41:12] that, it's very similar. Mhm.
[00:41:14] Great. So, once we have this Cloud Build
[00:41:17] Oh, yeah. So, this is the Cloud Storage
[00:41:19] FUSE that we mentioned earlier that can
[00:41:21] mount Google Cloud Storage bucket with
[00:41:24] local file. So, this is like earlier we
[00:41:26] mentioned.
[00:41:28] And so, yeah, we have this Cloud Storage
[00:41:31] FUSE explanation before, and you can
[00:41:33] check this facts over here by configure
[00:41:36] the volume for enable Cloud Storage
[00:41:38] FUSE. Next, we have this cloudbuild.yaml
[00:41:42] file configured. And next is let's run
[00:41:45] this gcloud builds submit file as always
[00:41:48] to follow this whole instruction so that
[00:41:50] you will actually
[00:41:54] so that you will actually um
[00:41:56] follow this CI pipeline. Yeah, build,
[00:42:00] uh push, and then deploy [clears throat]
[00:42:02] to Cloud Run. Yeah.
[00:42:05] And it probably take like 20 minutes or
[00:42:07] so, right?
[00:42:08] Yeah, 20 to 30 minutes. Yeah.
[00:42:11] All right. Looks like it's finished.
[00:42:14] Yay. So, what's next is let's take a
[00:42:16] look at this Google Cloud Build history.
[00:42:19] So, if you click if you click this link,
[00:42:20] it will take a look at this whole
[00:42:22] building summary, the building process.
[00:42:24] And also, you can see the Cloud Run
[00:42:27] service page by go to Cloud Run service.
[00:42:32] making sure pick this project. And you
[00:42:35] can see that we have Olama that deployed
[00:42:37] from the previous one, and VLM is this
[00:42:39] one. And yeah, you can see that we have
[00:42:41] this uh URL here. This is like the link
[00:42:43] you can connect to uh Gemma 4 model. And
[00:42:47] just to Now, we want to verify
[00:42:49] everything's working. So, again, we want
[00:42:51] to like send the post request with this
[00:42:54] URL link. And this is the endpoint with
[00:42:57] our chat completion. And we want to ask
[00:42:59] the same question like, "As a guardian
[00:43:01] of Aethelred, what is my primary duty?"
[00:43:04] And we want to verify if this um
[00:43:06] whole deployed version of Gemma Gemma 4
[00:43:09] on hosted Cloud Run is that working or
[00:43:11] not. So, let's give it a try. I copy
[00:43:13] this. So, I'm going to come into the
[00:43:14] terminal, and I'm going to paste it
[00:43:17] So, let's take a look at what is the
[00:43:20] result.
[00:43:28] Yeah, as you can see that because the
[00:43:30] first time initial load, we have some
[00:43:31] cold start.
[00:43:36] So, let's look. So, we see the response,
[00:43:38] "As a guardian of the Aethelred, your
[00:43:40] primary duty is multifaceted and so on."
[00:43:42] If you recall the response from Olama
[00:43:44] before, as Annie mentioned, these models
[00:43:46] are stochastic. So, you can call the
[00:43:48] same model the same multiple times to
[00:43:50] get a different response. But overall,
[00:43:51] very similar response to the same
[00:43:53] question as before.
[00:43:55] Um and overall, it's everything looks
[00:43:56] like it's working. Yeah. Great. All
[00:43:58] right. So, just have a quick overview of
[00:44:02] what we've done so far with VLM. So,
[00:44:03] first, we download this image uh we
[00:44:06] download the model from Hugging Face to
[00:44:08] Google Cloud Storage, and then we have
[00:44:10] this pipeline that we build the image of
[00:44:12] your VLM code, and then and then deploy
[00:44:15] the whole thing to Cloud Run. And then,
[00:44:17] we set up the
[00:44:18] GCS FUSE so that it will sync to the it
[00:44:21] will mount the Cloud Storage with a
[00:44:23] local file.
[00:44:24] And let's talk about the advantages or
[00:44:27] disadvantages of this approach. Cuz
[00:44:29] compared to Olama, that Olama is is very
[00:44:33] easy very easy to start and try anything
[00:44:36] do the local development, VLM is a great
[00:44:38] option for production use case. And it's
[00:44:41] very flexible to update the model as
[00:44:43] swap the You can just simply swap the
[00:44:45] file in the bucket and restart. However,
[00:44:47] it has some uh initial cold start
[00:44:49] because it doesn't have the baking the
[00:44:51] model uh baking the model baking in as
[00:44:53] Olama does. Anything to add, Io, for the
[00:44:55] tradeoff is uh VLM? No, that's that's a
[00:44:58] great summary. Where essentially with
[00:45:00] VLM and with the approach that we took,
[00:45:02] essentially you can use something like
[00:45:03] GCS FUSE to dynamically update the model
[00:45:05] weights if you need to. But on
[00:45:07] essentially, there's a longer cold
[00:45:08] start. But um one caveat with that is
[00:45:11] that's really meant for the initial
[00:45:13] invocation or initial user. Um if you
[00:45:15] have multiple concurrent users, a
[00:45:16] thousand users calling the same endpoint
[00:45:18] at a time, that warm instance actually
[00:45:20] won't, you know, obviously have that
[00:45:21] cold start for future users. Um so, it's
[00:45:24] really meant that cold start you tend to
[00:45:25] experience really meant for the first
[00:45:27] call to that, you know, newly created
[00:45:29] machine. But um yeah.
[00:45:32] Yeah, so here is the overview of, you
[00:45:35] know, so far we have Olama and VLM. So,
[00:45:39] those are the advantages of Olama for
[00:45:41] local development and prototyping.
[00:45:43] And also has multi-GPU support. However,
[00:45:46] if you the production use case like uh
[00:45:48] VLM has the page attention for product
[00:45:50] efficiency and parallel parallelism for
[00:45:53] like maximize GPU usage. So, yeah, it's
[00:45:56] really good for production use case.
[00:45:58] So, let's just coming back for this
[00:46:01] high-level architecture we have. And for
[00:46:04] today's episode, we learned how do you
[00:46:06] host Gemma 4 model with Olama, VLM to
[00:46:10] Cloud Run. So, this is this is this is
[00:46:12] the piece we covered for today. We
[00:46:14] covered like how do you using um
[00:46:16] how do you pull model from Olama and
[00:46:19] host it on Cloud Run. And we also know
[00:46:20] how to download the model from Hugging
[00:46:22] Face, and then host it with VLM.
[00:46:24] And what's next
[00:46:25] uh what's next, Io? What are we going to
[00:46:27] cover next?
[00:46:28] Yeah, great question. We're going to
[00:46:30] learn uh lots of things. So, we're going
[00:46:31] to learn how can you serve and scale
[00:46:33] these models at a global scale using
[00:46:35] something like a load balancer. How can
[00:46:37] you secure these models and protect
[00:46:39] against things like model uh prompt
[00:46:40] injection and jailbreaking? How can you
[00:46:42] determine if your model's actually
[00:46:44] leaking sensitive data? The answer for
[00:46:46] that is also something like Model Armor.
[00:46:48] How can you use these models as the
[00:46:49] brain behind a deployed agent? We talked
[00:46:52] a little bit about Light LLM uh earlier
[00:46:54] today. We're actually going to put this
[00:46:55] in practice tomorrow and use Light LLM
[00:46:58] to kind of connect with our
[00:46:59] self-deployed models so we can use them
[00:47:01] as the brain behind these agents. And
[00:47:02] lastly, we're going to learn how can you
[00:47:04] actually observe um the metrics being
[00:47:06] generated by these models. So, you know,
[00:47:08] we talked about cost earlier, and how
[00:47:10] can you actually monitor that um from
[00:47:12] like a how many tokens are being
[00:47:13] generated um by these models? You can
[00:47:15] use something like a Prometheus sidecar
[00:47:17] associated with the Cloud Run instance
[00:47:19] that actually be extracting metrics such
[00:47:21] as how many tokens are being generated,
[00:47:23] what are the what is the GPU
[00:47:24] utilization, and so on. So, we're going
[00:47:26] to be learning a lot tomorrow. I hope
[00:47:27] you guys all stay tuned.
[00:47:29] Um and uh
[00:47:30] &gt;&gt; Yeah.
[00:47:31] That's a really good summary. So, by the
[00:47:33] end of this two episode, you're going to
[00:47:34] learn everything about this end-to-end
[00:47:37] system management. Yeah. Yeah, yeah. So,
[00:47:41] stay tuned. Um but until next time, I'm
[00:47:43] Io. I'm Annie. Bye. Peace.
[00:47:46] &gt;&gt; [music]
[00:47:53] [music]
