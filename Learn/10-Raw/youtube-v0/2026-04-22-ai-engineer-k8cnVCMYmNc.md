---
source_url: https://www.youtube.com/watch?v=k8cnVCMYmNc
source_type: youtube
source_platform: youtube.com
title: OpenAI + Temporal.io — Building Durable, Production Ready Agents
author: AI Engineer
video_id: k8cnVCMYmNc
captured_at: 2026-04-22
duration_sec: 4710
status: raw
---

[00:00:21] I'll introduce myself in in just a
[00:00:23] moment, but I'd like to get to know a
[00:00:24] little bit about you. So, you know, you
[00:00:26] can see that there's there's two brands
[00:00:29] up on the screen here. There's OpenAI
[00:00:32] agents SDK in particular, and there's
[00:00:35] Temporal. I work for Temporal. I'll tell
[00:00:37] you more about myself in just a second.
[00:00:39] Um, I'm curious, how many folks are
[00:00:42] using the OpenAI agents SDK today?
[00:00:46] Okay, about a quarter of you. um
[00:00:51] any other um a agentic frameworks?
[00:00:56] Okay, about the same set of you. So,
[00:00:58] it's it looks like there's a hand quite
[00:01:00] a number of you who are not using an
[00:01:02] agent framework just yet. So, I'll teach
[00:01:05] you a little bit about that. Okay, next
[00:01:07] question. How many folks are doing
[00:01:09] anything with temporal?
[00:01:12] Not very many. Awesome. I'm gonna get to
[00:01:15] teach you some stuff. Um, okay, cool.
[00:01:19] So, uh, we're going to talk today about
[00:01:21] both those technologies. I'm going to
[00:01:23] talk about them each independently, but
[00:01:25] I'm going to spend a lot of time on them
[00:01:27] together. Uh, spoiler, we actually have
[00:01:30] an integration between the two products
[00:01:32] that Temporal and OpenAI worked on
[00:01:34] together. Um, and so, and and you'll see
[00:01:38] it's it's really quite sweet. So, let me
[00:01:41] very briefly introduce myself. My name
[00:01:43] is Cornelia Davis. I'm a developer
[00:01:45] advocate here at Temporal. Um I have
[00:01:48] spent a lot of time I think the bulk of
[00:01:50] my career has been spent in this
[00:01:51] distributed system space. So I was super
[00:01:54] fortunate to be at Pivotal um working on
[00:01:57] Cloud Foundry from the early 2010s. So I
[00:02:00] was really there during the kind of
[00:02:01] movement toward micros service
[00:02:03] architectures, distributed systems,
[00:02:06] those types of things. Um any Cloud
[00:02:08] Foundry folks in the room? Oh, just a
[00:02:12] few. Um, so for those of you who don't
[00:02:14] know Cloud Foundry, Cloud Foundry was um
[00:02:17] the early the early container technology
[00:02:20] out on the market. It was incubated as a
[00:02:23] open- source project at VMware and it
[00:02:26] used um uh container images, Linux
[00:02:28] containers, container orchestration,
[00:02:31] eventual consistency, all of that stuff
[00:02:34] before Docker even existed and well
[00:02:37] before Kubernetes existed. So I was very
[00:02:40] very fortunate that I was there at the
[00:02:42] beginning of that movement o over toward
[00:02:45] platforms that supported this more agile
[00:02:47] distributed systems way of doing things
[00:02:49] and because I spent so much time in the
[00:02:51] microservices world I also wrote this
[00:02:53] book. Okay. So what we're going to talk
[00:02:57] about today is we're going to talk about
[00:02:59] the open agent a uh open AI agents SDK.
[00:03:03] Then I'm going to give you a temporal
[00:03:05] overview. I'm going to do lots of demos
[00:03:07] and I'm going to show you the repos. If
[00:03:09] you want to if you want to follow along,
[00:03:11] you can go ahead and grab the repos.
[00:03:14] Both of my demos I actually changed this
[00:03:16] morning so they're sitting in branches
[00:03:19] instead of in the main branches, but I
[00:03:20] will make that very clear as well. Going
[00:03:23] to do lots of demos there and then I'm
[00:03:25] going to do uh move over to the
[00:03:27] combination of the OpenAI agents SDK and
[00:03:30] temporal together and we'll do more
[00:03:32] demos there as well. And then I'm going
[00:03:34] to talk a little bit about orchestrating
[00:03:36] agents kind of in the general sense.
[00:03:39] So this here is a notebook that we're
[00:03:42] I'm not going to use today. And so I
[00:03:46] decided I just ran this workshop earlier
[00:03:48] this week and I decided that for the AIE
[00:03:51] crowd it was way too basic. That said,
[00:03:54] if you're interested, you can go there.
[00:03:57] It will take you through. It's it's set
[00:03:58] up with Jupyter notebooks. You can run
[00:04:00] it in code spaces on GitHub and you can
[00:04:04] run your first OpenAI agents SDK agent.
[00:04:07] Then you can run your first 101 temporal
[00:04:10] a uh not agent but temporal application.
[00:04:13] Then you can move all the way through
[00:04:15] the agenda that way. But it's pretty
[00:04:17] basic and I decided that for this crowd
[00:04:19] I wanted to do something more advanced.
[00:04:22] So we're not going to use that today. Um
[00:04:24] and I just crafted some of these demos
[00:04:26] this morning. Okay. So without further
[00:04:29] ado, this is going to be the shortest
[00:04:30] part of the presentation is I'm going to
[00:04:32] give you an intro to the OpenAI agents
[00:04:34] SDK. This was launched in I think around
[00:04:37] the May time frame or so. Um and I I'm
[00:04:42] not going to read you these slides and
[00:04:44] oh just so you know where we're going. I
[00:04:46] am going to use some slides because I'm
[00:04:47] one of those people where I think the
[00:04:49] pictures really help. I've got lots of
[00:04:51] diagrams in here, but we are going to
[00:04:54] spend a lot of time stepping through the
[00:04:56] code as well. I don't think I need to
[00:04:58] define what an agent is. I will tell you
[00:05:00] that that for me personally the
[00:05:03] distinction that I make between Genai
[00:05:06] applications and then when they get to
[00:05:08] agents is when we give the LLM's agency
[00:05:11] when the LLMs are the ones that are
[00:05:12] deciding on the flow of the application.
[00:05:14] That to me is what what an agent is. And
[00:05:18] these frameworks like the OpenAI agents
[00:05:20] SDK are designed to make it easier for
[00:05:23] you to get started with those. And in
[00:05:25] fact, we'll see that really we'll see a
[00:05:28] contrast on that with the two major
[00:05:30] demos that I'm going to show you today.
[00:05:32] It's available um in both Python and
[00:05:35] Typescript.
[00:05:37] And here is the most basic application.
[00:05:40] So what you see here is that we've
[00:05:42] defined an agent. We've given it a name
[00:05:45] and we've given it instructions and it's
[00:05:47] taken defaults for the rest of it. Other
[00:05:50] things things that are defaulted are
[00:05:51] things like the model itself. I don't
[00:05:54] know what the default is right now. And
[00:05:56] then all you can all you need to do
[00:05:58] after that is you basically need to run
[00:06:00] it. And anytime you see that runner.run,
[00:06:03] what that corresponds to is an agentic
[00:06:06] loop. And we'll talk about the agentic
[00:06:08] loop several times throughout the
[00:06:10] presentation. Every time you see one of
[00:06:12] those runner.runs, it's its own agentic
[00:06:14] loop. And when we get to the
[00:06:16] orchestration stuff later on, you'll see
[00:06:18] why I make that distinction.
[00:06:21] It also as as I said this is really
[00:06:23] simple here but it has a lot of other
[00:06:25] options that you can put in place into
[00:06:27] the agent configurations that that drive
[00:06:31] how the agentic loop works. You can have
[00:06:34] handoffs. We will talk about those. So
[00:06:36] I'll clarify that later. But you could
[00:06:38] put guard rails in place. You can you
[00:06:40] can add tools. And we're going to see
[00:06:42] both of my examples are heavy duty on
[00:06:45] LLM agency and it deciding which tools
[00:06:48] to use. So, I'm going to show you tools.
[00:06:50] So, there's a lot more that you can do
[00:06:52] in here, and I'll show you examples of
[00:06:54] that as we go along. And really, this is
[00:06:57] the picture of what I'm talking about is
[00:07:00] that every one of those runner.runs
[00:07:02] basically has a loop that is constantly
[00:07:04] going back to the LLM. And after the LLM
[00:07:07] call, it decides to do things. And if
[00:07:10] the LLM, for example, has said, I want
[00:07:12] you to invoke some tools, it will go
[00:07:14] ahead and invoke those tools. And then
[00:07:16] it'll take the output from the tools and
[00:07:18] route it back to the LLM and keep going.
[00:07:21] And the LLM gets to decide when it's
[00:07:23] done following the system instructions
[00:07:26] and we'll see that. Okay. So that is the
[00:07:30] basic um you know agent framework
[00:07:33] overview and there's lots of a agent
[00:07:36] frameworks out there. Okay. Since very
[00:07:39] few of you know know temporal I'm going
[00:07:41] to slow down a little bit here and tell
[00:07:43] you more about temporal. So, Temporal is
[00:07:46] an open-source project. It's been around
[00:07:48] for about five or six years. So, yes, it
[00:07:52] well predates the Gen AI boom that we're
[00:07:55] in. It's designed for distributed
[00:07:58] systems and what are AI applications if
[00:08:02] not distributed systems? So, it turns
[00:08:04] out that temporal is beautifully suited
[00:08:06] for these this category of AI of use
[00:08:09] cases. Now, it's used in a lot of nonAI
[00:08:13] use cases. So, for example, every snap
[00:08:18] Snapchat goes through Temporal. Every
[00:08:20] Airbnb booking goes through Temporal.
[00:08:23] Pizza Hut, Taco Bell orders go through
[00:08:25] Temporal. Um, there's lots of other ones
[00:08:28] that I'm not remembering. OpenAI Codeex
[00:08:31] runs on Temporal. So, now we start
[00:08:34] moving into the AI use cases. Codeex
[00:08:36] runs on Temporal. OpenAI's image gen
[00:08:39] runs on temporal. Those are the two I
[00:08:41] can tell you about. Those are the two
[00:08:42] that are publicly known. Um, so we've
[00:08:45] got lots of others out there, lovable
[00:08:47] runs on on temporal. So we're definitely
[00:08:50] making, you know, inroads, lots lots of
[00:08:52] use in the AI space. So I've told you
[00:08:55] who's using it, but let me tell you what
[00:08:58] it is. What it is is distributed systems
[00:09:03] as a backing service. So I think
[00:09:06] everybody's familiar with the notion of
[00:09:08] Reddus as a backing service or Kafka as
[00:09:11] a backing service or a database as a
[00:09:13] backing service. So I've got my
[00:09:15] applications that are running and I use
[00:09:17] these back-end services to serve, you
[00:09:19] know, to play a part of my application.
[00:09:22] Temporal is a backing service. What it
[00:09:25] delivers is distributed systems
[00:09:27] durability.
[00:09:28] And I'll make that clearer as we go
[00:09:31] through the presentation. What that
[00:09:33] means is that you as the developer get
[00:09:36] to program the happy path. You get to
[00:09:39] program your business logic. And the
[00:09:42] business logic that we're going to
[00:09:43] program today are AI agents. So you get
[00:09:46] to say, you know what, what I want to do
[00:09:49] is I want to call an LLM. Then I want to
[00:09:52] take the output from the LLM and I might
[00:09:53] want to invoke some other APIs and then
[00:09:56] I want to loop back to the LLM. And you
[00:09:59] don't have to build the logic in there
[00:10:00] that says what happens if the LLM is
[00:10:03] rate limited. What happens if my
[00:10:05] downstream API is down for a moment?
[00:10:08] What happens if my application crash
[00:10:11] crashes? You don't have to program any
[00:10:14] of that. We do it for you. And I'll show
[00:10:16] you a few pictures on how this works in
[00:10:18] just a moment.
[00:10:20] So there's a a temporal service that is
[00:10:23] the backing service. And the way that
[00:10:25] you connect to the backing service is
[00:10:26] through an SDK. And so the SDK sits
[00:10:30] alongside your business logic. So you
[00:10:32] get to program your business logic. And
[00:10:35] the way that you craft your business
[00:10:36] logic, you put wrappers around certain
[00:10:39] functions. And that allows the SDK to
[00:10:42] say, "Oh, hang on. You're making a a
[00:10:45] downstream API call. I'm going to step
[00:10:48] in and I'm going to provide you some
[00:10:50] service. So I'm going to provide you
[00:10:53] retries. If that downstream service uh
[00:10:56] succeeds, I'm going to record that for
[00:10:58] you. I'm going to record the answer for
[00:11:00] you so that in in the event that
[00:11:03] something happens and we need to go
[00:11:05] through the flow again, I can just get
[00:11:07] the the result that you called before.
[00:11:10] What that means is, for example, if you
[00:11:12] have used temporal to lend durability to
[00:11:15] your agents, when you're on the 1,350
[00:11:19] second turn to the LLM and your
[00:11:22] application crashes, no sweat. We have
[00:11:25] kept track of every single LLM call and
[00:11:28] return and you will not be reburning
[00:11:31] those tokens. That's what it means.
[00:11:33] That's what durability means in this
[00:11:35] space. We support um we formally support
[00:11:40] seven different programming languages,
[00:11:42] but Apple just a couple of weeks ago um
[00:11:45] released a Swift SDK as well. So there's
[00:11:48] support in just about any language.
[00:11:50] There's also experimental stuff out
[00:11:51] there in Closure, those types of things.
[00:11:54] I said it's an open- source project. The
[00:11:57] vast majority of it is MIT licensed. Um
[00:12:00] there's a little bit of Apache 2 left
[00:12:02] over from in the Java SDK. So very very
[00:12:05] permissive licenses and um those of you
[00:12:08] who don't know the history uh temporal
[00:12:11] was a fork of a project that was created
[00:12:15] out of Uber called Cadence. Anybody know
[00:12:17] Cadence? Yeah. Okay. So a few people
[00:12:19] know Cadence. So Cadence pretty much
[00:12:22] every application running at Uber runs
[00:12:24] on Cadence and it's because they can
[00:12:26] program the happy path and all the
[00:12:28] durability is just taken care of for
[00:12:29] you. So that's kind of the overview of
[00:12:32] what temporal is. So there's really kind
[00:12:36] of I'm going to talk about two
[00:12:37] foundational abstractions. There's a
[00:12:39] handful of others as well, but the two
[00:12:42] foundational abstractions that you need
[00:12:44] to know about as a developer is you need
[00:12:46] to know about an activity. And an
[00:12:48] activity is just a chunk of work. This
[00:12:52] is work that either is going to make
[00:12:54] external calls. So it's work that might
[00:12:57] fail. It's like a lot of work that might
[00:13:00] fail. or if you are doing a lot of work
[00:13:03] that you don't want to have to redo in
[00:13:05] the event that something goes wrong, you
[00:13:07] might want to put that in an activity as
[00:13:09] well. So, it's things like withdrawing
[00:13:12] from an account, depositing into an
[00:13:14] account. We'll get to the AI use cases
[00:13:16] in just a moment. So, those are
[00:13:18] activities you wrap that Oh, and I
[00:13:20] didn't mention it, but the SDKs are not
[00:13:23] just thin wrappers that are sitting on
[00:13:26] top of a REST API. These are SDKs where
[00:13:29] as you can imagine be let uh delivering
[00:13:33] durability across distributed systems
[00:13:35] means that all of those algorithms that
[00:13:37] you thought that you had to implement
[00:13:40] like worry about concurrency and and and
[00:13:43] um uh quorum and all of that stuff
[00:13:46] that's all implemented in temporal and
[00:13:48] so our SDKs have a lot of that logic is
[00:13:51] in the SDK. The service is mostly
[00:13:55] persistence for that. So there's a lot
[00:13:57] of intelligence in the SDK.
[00:14:00] So these activities, if you've said,
[00:14:02] look, here's my work. Here's a heavyduty
[00:14:05] piece of work or something that's going
[00:14:06] external. Let's put an activity
[00:14:09] decorator on that. Then the SDK says,
[00:14:11] oh, okay, I'm going to give you some
[00:14:13] special behavior. Then you orchestrate
[00:14:16] those activities together into your
[00:14:19] business logic. And what we call those
[00:14:21] orchestrations is workflows.
[00:14:24] Okay? So, and you'll see that what
[00:14:27] happens when you put activities and
[00:14:29] workflows together, that's where the
[00:14:31] magic really happens. There is some
[00:14:33] level of magic in the activities and in
[00:14:35] fact, we're just starting to release
[00:14:38] what we call standalone activities. So,
[00:14:40] you'll be able to use activities without
[00:14:41] workflows and get some of those
[00:14:43] durability benefits there as well. So,
[00:14:45] there's all sorts of evolution that's
[00:14:47] happening. But the type of magic that
[00:14:49] I'm talking about when you um bring
[00:14:53] workflows and activities together is
[00:14:55] that I overlaid
[00:14:57] um a bunch of icons on here. So I
[00:15:00] overlaid these little retry icons. So
[00:15:04] what you do is you specify in your
[00:15:05] workflow logic you specify the um retry
[00:15:10] uh configuration. So you can decide are
[00:15:13] you going to do exponential backoffs?
[00:15:15] Are you going to do unlimited retries?
[00:15:17] Are you going to top out at five
[00:15:19] retries? Are you going to have a maximum
[00:15:22] window between retries? You get to
[00:15:24] configure all of that. And as soon as
[00:15:26] you do that and you orchestrate these
[00:15:27] things together, now you get retries.
[00:15:30] And you'll see the code in just a minute
[00:15:33] simply by calling these activities. I
[00:15:36] don't have to implement the retry logic.
[00:15:38] I don't have to implement any of this
[00:15:40] other logic. It just happens for me. So
[00:15:43] I get retries. I also get these little
[00:15:46] cues. So what looks to you like a single
[00:15:50] process application I'm calling this
[00:15:52] then I'm calling this and I'm calling
[00:15:54] this every single time you call into an
[00:15:57] activity every time you come back from
[00:15:59] an activity to the main workflow all of
[00:16:02] that is facilitated over cues so that
[00:16:05] what looks like just a single monolithic
[00:16:08] application is already turns into a
[00:16:10] distributed system. So you can go and
[00:16:13] deploy a whole bunch of instances of
[00:16:15] those and you can basically scale by
[00:16:17] just deploying more instances of it. You
[00:16:20] don't have to manage and I you don't
[00:16:22] have to manage Kafka cues any of that
[00:16:24] stuff. It's all built in. I spoke with
[00:16:26] somebody this week here at AI Engineers
[00:16:29] um who's who's a an open source user
[00:16:32] actually a customer of ours and I asked
[00:16:34] him it's a relatively small startup and
[00:16:37] I said you know why did you pick
[00:16:38] temporal and he said because we tried to
[00:16:41] build all of this with Kafka cues and we
[00:16:43] ended up spending all of our time doing
[00:16:45] operations on Kafka and spending 25% of
[00:16:49] our time on the business logic when we
[00:16:51] switched over to temporal we're spending
[00:16:54] 75% of our time on business logic and
[00:16:56] they're using temporal cloud. I didn't
[00:16:58] mention our business model is that we
[00:17:00] have it that that that service we offer
[00:17:03] that as SAS. So they're using temporal
[00:17:05] cloud. So they basically shifted from
[00:17:08] 2575
[00:17:10] to 7525 by moving over here. No longer
[00:17:13] have to manage Kafka cues or red reddus
[00:17:16] or anything like that. And speaking of
[00:17:18] Reddus, you see in the upper right hand
[00:17:20] corner you see state management. And so
[00:17:23] one of the things that we do as well is
[00:17:24] we keep track of where you are in the e
[00:17:27] execution of your application. We do
[00:17:29] that by recording the state. Again,
[00:17:31] every time you're making calls to an
[00:17:33] activity and coming back, we record
[00:17:35] that. It's basically event sourcing.
[00:17:38] That's what we're doing. It's not only
[00:17:40] event- driven architectures, but we're
[00:17:42] doing event sourcing as a service. So
[00:17:45] you you get to do that. So, we store all
[00:17:47] of that state so that if something goes
[00:17:49] wrong, and I'm going to demo that, we're
[00:17:51] going to see things going wrong, um, it
[00:17:54] will pick up where it left off because
[00:17:56] we will just run run through the event
[00:17:58] history and pick up where we left off.
[00:18:02] So, those little icons that I showed
[00:18:04] overlaid on the logical diagram, I'll
[00:18:06] get to your question one second.
[00:18:08] Actually, all of those services live up
[00:18:10] here in the service. So, they're all
[00:18:12] durable. So it's not that they're living
[00:18:15] in the process, but they're living here
[00:18:17] in the service. You have a question?
[00:18:19] &gt;&gt; Not sure it's relevant. So a lot of the
[00:18:22] agents I have, they handle streaming
[00:18:25] data.
[00:18:26] So I wanted to see if help with that.
[00:18:29] &gt;&gt; Oh, great question. So yeah, so the
[00:18:31] question was a lot of the agents that
[00:18:33] I'm building are doing streaming. Do you
[00:18:35] do streaming? And the answer right now
[00:18:37] is a very simple no, we don't. But it is
[00:18:40] one of the things. and my colleague at
[00:18:42] the back, Johan, um is uh head of AI
[00:18:46] engineering. Um so chat with him, chat
[00:18:50] with either of us. It is one of the two
[00:18:52] top priority things that we're working
[00:18:54] on right now. Um the other one is large
[00:18:56] payload storage. If I don't have a
[00:18:58] chance to to talk about it here during
[00:19:01] the workshop, come find one of us. We
[00:19:03] can tell you about that. You can imagine
[00:19:04] what large payload storage is. is that
[00:19:07] you're doing LLMs, you're gonna you're
[00:19:08] gonna passing big stuff around. Instead
[00:19:11] of passing it around by value, pass it
[00:19:13] by reference. That's what large payload
[00:19:14] storage is. That's Johan.
[00:19:16] &gt;&gt; I'll just mention there are a bunch of
[00:19:18] people using workarounds.
[00:19:20] &gt;&gt; True.
[00:19:21] &gt;&gt; Screening in production today at scale.
[00:19:24] So happy to talk about that, but there's
[00:19:25] going to be more integrated solution
[00:19:28] coming.
[00:19:29] &gt;&gt; Yeah. So I ju I'm just going to repeat
[00:19:31] what Johan said in case you you couldn't
[00:19:33] hear it. So we do have customers that
[00:19:35] have built streaming support on top of
[00:19:38] temporal, but what we're doing is
[00:19:40] building it in natively. So, yep. So,
[00:19:43] you can do it today. It's just a little
[00:19:45] bit more work. It's not the happy path.
[00:19:47] So, okay. Um, so with that, uh, I want
[00:19:52] to give you a demo. So, this is going to
[00:19:54] be my first demo that I move over here.
[00:19:56] Let's see if I can get my screen back.
[00:19:58] Okay. So, if you want to follow along,
[00:20:01] the first thing I'm going to do is I'm
[00:20:02] going to come over here and I am going
[00:20:04] to let me increase the font size. Um, so
[00:20:09] I'm going to point you to two
[00:20:10] repositories. This is actually the
[00:20:12] second repository, but what I have up on
[00:20:14] the screen right now is that if you want
[00:20:17] to get started with temporal, super
[00:20:19] simple, you don't have to use temporal
[00:20:21] cloud. You can just run a temporal
[00:20:23] service. So, the backing service, you
[00:20:26] can just run it locally on your machine.
[00:20:28] So you can do it by curling this. You
[00:20:30] can homebrew install it as well. Um and
[00:20:33] then to run that local server, you can
[00:20:35] just say temporal server start dev. And
[00:20:38] now you've got a temporal service that's
[00:20:40] running locally. And all of my um
[00:20:42] applications here are just connecting to
[00:20:44] my local host. Um and we we'll see the
[00:20:47] UI in just a moment. Um I'll come back
[00:20:50] to this uh repository in just a moment.
[00:20:53] The repo that I'm going to demo for you
[00:20:55] is this one. And um sorry I don't know
[00:20:59] how to uh increase the font size but you
[00:21:01] can see that the org and the repository
[00:21:04] here is the org is temporal io. That's
[00:21:08] also where you'll find all of the open
[00:21:10] source for temporal. Um and then we have
[00:21:13] something called the AI cookbook and
[00:21:16] that's one of the examples. I I I
[00:21:19] actually extended the example just this
[00:21:20] morning, but um and you're going to find
[00:21:23] that um in the the branch that we're
[00:21:27] going to demo here today is called the
[00:21:29] agentic loop de branch. So if you want
[00:21:33] to, you know, go back and take a look at
[00:21:35] this later on um yourself, that's what
[00:21:37] we're going to be looking at. Okay. So
[00:21:40] with that, let me get to my right
[00:21:44] terminal.
[00:21:46] And um so this is where I'm going to run
[00:21:50] it, but I want to show you the code
[00:21:52] first.
[00:21:54] Okay. So am I in the right uh
[00:21:59] one? OpenAI. Nope. This is the wrong
[00:22:01] one. My other cursor. Here we go. So
[00:22:04] this is the agentic loop. So I'm doing
[00:22:06] two demos throughout today.
[00:22:10] And so what you see here on the left
[00:22:12] hand side, let me make it just one tick
[00:22:14] bigger is that remember that I talked
[00:22:17] about activities and I talked about
[00:22:20] workflows. So that's the first thing I'm
[00:22:22] going to do is I'm going to show you the
[00:22:23] activities. Remember we had withdraw and
[00:22:26] and and uh and deposit, you know, that
[00:22:29] type of thing. Here, of course, what
[00:22:31] we're doing is an agentic loop. So my
[00:22:33] activities are going to be um call the
[00:22:38] OpenAI API, not the agents SDK yet, just
[00:22:42] the OpenAI a um API and invoke some
[00:22:45] tools. So these are my two activities.
[00:22:47] So let's look at the first one and
[00:22:49] you'll see how simple it is. I promised
[00:22:52] you the happy path. It really is that.
[00:22:55] So here is my call to the OpenAI
[00:22:58] responses API. Okay, it is exactly what
[00:23:01] you would expect. I'm passing in the
[00:23:03] model. I'm passing in some instructions.
[00:23:06] Um, the user input is going to come in
[00:23:09] my tools, which I'll show you in just a
[00:23:11] moment. And then I've got some timeouts
[00:23:13] that I can configure there. That's for
[00:23:14] the OpenAI.
[00:23:16] What I've done is I've wrapped that in a
[00:23:18] function. It takes in that request. So,
[00:23:21] all of those parameters came from a
[00:23:23] request that I'm passing in. And you'll
[00:23:25] see how I invoke this in just a moment.
[00:23:27] And here is that annotation. Now the
[00:23:30] different SDKs have different
[00:23:32] approaches. TypeScript for example
[00:23:34] doesn't require a bunch of annotations.
[00:23:36] It just figures it out. It knows where
[00:23:39] the activities are. Java has um
[00:23:42] annotations. Those types of things. But
[00:23:43] this is Python. So you can see here that
[00:23:46] we just have an activity decorator. So
[00:23:48] by just having that decorator, so you
[00:23:50] can see it's not complicated at all. All
[00:23:53] you need to do as a developer is say,
[00:23:55] "Here's a a bunch of work that I want to
[00:23:57] do that I want to kind of encapsulate
[00:24:00] into a step." And you just put an you
[00:24:03] put it in a function. You put an
[00:24:04] activity decorator on that.
[00:24:07] So, I'll come back to the tool invoker
[00:24:09] in just a minute because there's
[00:24:10] something interesting that's going on
[00:24:12] here. So, now if we go to the workflow,
[00:24:14] the workflow is also pretty darn
[00:24:17] straightforward. So what I have here is
[00:24:21] I have my workflow definition. You can
[00:24:23] see it's a class. The reason it's a
[00:24:25] class is because there when you create a
[00:24:28] workflow you create the application main
[00:24:30] what I call the application main and
[00:24:32] that's what has the workflow.run on it.
[00:24:36] But this workflow also I'm not going to
[00:24:38] cover these abstractions today but we
[00:24:40] have a handful of other abstractions
[00:24:41] like signals.
[00:24:44] So for a running workflow, you can
[00:24:46] signal into it and we also have an
[00:24:49] abstraction called an update. It's a
[00:24:51] special kind of a signal. And we also
[00:24:53] have the analog which is queries.
[00:24:56] So those things are added to this
[00:24:59] workflow class as just functions that
[00:25:01] are annotated with signal update or
[00:25:04] query. So that's why we've got a class
[00:25:06] for the the the workflow. And if we take
[00:25:10] a look at what the logic is in here, you
[00:25:12] can see that I have a while true. So
[00:25:15] this simple application is just that
[00:25:19] same picture that I showed you earlier
[00:25:21] where I said the LLM is we're just
[00:25:23] looping on the LLM. And if the LLM makes
[00:25:26] the decision to do so, we're going to
[00:25:28] call tools. That's the whole
[00:25:30] application. But you're going to see
[00:25:32] that I'm doing a couple of interesting
[00:25:34] things with temporal here. So in order
[00:25:37] to invoke the LLM, I execute that
[00:25:39] activity. So you can see that I'm
[00:25:41] passing in my model. Um the instructions
[00:25:44] here, I I won't show it to you, but you
[00:25:46] can see it all in the repository. The
[00:25:48] helpful agent system instruction
[00:25:50] basically just says you're a helpful
[00:25:52] agent. If if you if the user says
[00:25:55] something and you think you should be
[00:25:56] using a tool, let me know. You know,
[00:25:59] choose a tool. Otherwise, respond in
[00:26:01] haikus. You'll see that in just a
[00:26:03] moment. Like haikus are like the fooar
[00:26:05] of the AI world, right? Ever we're all
[00:26:08] we're all going to write agents. It's
[00:26:09] the hello world of of the agentic space.
[00:26:12] So we're going to respond in haikus. Um
[00:26:16] and that's it. So we're doing this at a
[00:26:18] while true. And I've got a couple of
[00:26:19] print statements there. You're you're
[00:26:20] going to see how this runs in just a
[00:26:22] moment.
[00:26:24] Simplifying assumption here. I'm making
[00:26:26] the assumption that it's only calling
[00:26:27] one tool at a time. So I'm grabbing the
[00:26:29] output of that. And then I just take a
[00:26:31] look at it and say, is it a function
[00:26:33] call? And if it if it is a function
[00:26:36] call, then I'm going to handle that
[00:26:38] function call. I'll show you that code
[00:26:39] in just a second. And then I'm going to
[00:26:41] take the output from that function call
[00:26:43] and I'm going to add it to the
[00:26:44] conversation history. So I'm not doing
[00:26:46] any fancy context engineering here. None
[00:26:49] of that. I'm just basically tacking onto
[00:26:51] the end of the conversation history.
[00:26:53] Okay.
[00:26:55] Now, handling the function call is
[00:26:58] really straightforward as well. So the
[00:27:00] first thing that I'm doing is I'm adding
[00:27:02] the response from the LLM. So there's
[00:27:05] we're going to by the time we're done
[00:27:06] with this function call, we're going to
[00:27:08] have added two things to the
[00:27:10] conversation history. We're going to
[00:27:12] have added the response from the LLM
[00:27:14] which says please make a function call
[00:27:17] and then we're going to do the function
[00:27:18] call and then we're going to add the
[00:27:20] result. And I just showed you where
[00:27:21] we're adding the result of the function
[00:27:23] call. So here, this is just me adding
[00:27:25] that to the um and this is some of the
[00:27:28] squirrel stuff. I'm I have this this
[00:27:31] application running against the um
[00:27:33] Gemini API as well. And the biggest pain
[00:27:37] in the butt in all of this stuff is that
[00:27:39] the formats are different. So I have to
[00:27:42] rewrite because the JSON formats of
[00:27:44] conversation history are different
[00:27:45] between the different models. Yes, I
[00:27:48] know there's um light LLM out there, but
[00:27:50] I don't like least common denominators.
[00:27:52] And also I like to understand what those
[00:27:54] formats look like. So um but you can see
[00:27:57] here that I'm just doing some ugly
[00:27:59] parsing and then I'm executing remember
[00:28:03] I'm handling the tool call here. I'm
[00:28:05] executing the activity with that tool
[00:28:08] call. So I've p pulled the tool call out
[00:28:10] of the response from the um LLM and then
[00:28:15] I'm going to invoke that activity which
[00:28:17] is execute activity and the item name is
[00:28:20] the tool.
[00:28:22] Now one of the things that I was really
[00:28:25] intent on here is that I didn't want to
[00:28:27] build one aentic loop application that
[00:28:31] does one set of tools and then have to
[00:28:34] rebuild a whole another one when I have
[00:28:37] a different set of tools. the agent
[00:28:39] itself and we heard I don't remember who
[00:28:41] talked about this but somebody talked
[00:28:42] about this on stage this week where they
[00:28:44] said look the agentic pattern is the is
[00:28:48] is fairly standard and what we're doing
[00:28:51] now is we're inserting things into this
[00:28:54] standardized agentic loop and that's
[00:28:56] exactly what these um AI frameworks are
[00:28:59] doing these agent frameworks and I
[00:29:01] wanted to do that here in the temporal
[00:29:02] code as well the cool thing is that
[00:29:05] temporal has something called a dynamic
[00:29:07] activity
[00:29:08] The dynamic activity allows you to call
[00:29:12] an activity by name, but that that
[00:29:15] activity is dynamically found at
[00:29:18] runtime. So the activity handler here,
[00:29:21] and I'm going to show you the code in
[00:29:22] just a second, is basically going to
[00:29:24] take in that name and say, oh, okay, I
[00:29:27] and remember this is event driven. So we
[00:29:30] have an activity that's waiting for
[00:29:32] things on a queue. And so you can
[00:29:34] configure an activity. You can configure
[00:29:37] one of our workers to say, "Hey, this is
[00:29:39] a worker that will basically pick up
[00:29:41] anything off of an activity queue.
[00:29:44] Doesn't matter what the name is." So you
[00:29:46] don't have to tightly bind to a specific
[00:29:49] topic name for example. Yes. Question.
[00:29:51] &gt;&gt; I need in advance map which tools would
[00:29:56] be available for the agent based on the
[00:29:59] activity.
[00:30:00] &gt;&gt; Um that is separate and I'm going to
[00:30:03] show you that module. There's a module
[00:30:05] here that you see that's called tools.
[00:30:06] If you see the tools directory, the way
[00:30:09] that I'm running it here, it is it loads
[00:30:12] that stuff at the time that I load the
[00:30:14] application. So, I'm not doing any
[00:30:15] dynamic loading, but I can swap in and
[00:30:19] out that tools module and the agentic
[00:30:22] code does not change at all. So, I'm not
[00:30:24] going all the way to the point where
[00:30:26] I've implemented a registry and I'm
[00:30:28] doing dynamic calling of those things.
[00:30:31] You can do that, but this simple example
[00:30:33] has basically just put that all into a
[00:30:36] separate module. And you'll see how that
[00:30:38] module can be switched in and out
[00:30:39] because I'm loading it at at at um at
[00:30:42] start of runtime. So, um simplifying,
[00:30:46] but yes, you could do that. Okay. So,
[00:30:49] I'm just going to call an activity. And
[00:30:52] so, let's take a look at what that
[00:30:54] activity looks like. It's this tool
[00:30:56] invoker. And so you can see here that it
[00:30:59] has the activity decorator just like I
[00:31:01] showed you before, but now it says
[00:31:04] dynamic equals true. So that means that
[00:31:07] this activity handler will pick up
[00:31:10] anything that is showing up on a queue
[00:31:12] that isn't being picked up by some other
[00:31:15] activity already. So it'll pick up it'll
[00:31:18] pick up get weather. It'll pick up get
[00:31:20] random number. It'll pick up whatever
[00:31:22] shows up in there. You have to register.
[00:31:25] Um, you do have to register. No, you
[00:31:27] don't have to register all of those.
[00:31:29] Those things can be done dynamically.
[00:31:30] You don't have to register them into the
[00:31:32] worker.
[00:31:34] And what you can see here is that we
[00:31:35] basically grab that. We get the tool
[00:31:38] name. And then what you can see here is
[00:31:41] that I'm effectively looking up the
[00:31:44] function. You can see here there's no
[00:31:46] tool names in here at all. It's
[00:31:49] basically looking up the tool name from
[00:31:52] a dictionary. it and it it's
[00:31:55] metaphorically a dictionary. I'll show
[00:31:57] you those those uh um functions in just
[00:31:59] a second. So I have one function which
[00:32:02] is a get tools function um which by the
[00:32:05] way let me go back to that. So in the
[00:32:06] open AI responses uh no sorry it's down
[00:32:09] in the workflow when I invoke the LLM
[00:32:13] right here. Notice that I made this get
[00:32:16] tools call. I'll show you that get tools
[00:32:18] call in just a second. It's completely
[00:32:21] outside of the scope of the workflow and
[00:32:23] the activities. It's in its own module.
[00:32:25] I'll show you that um function in just a
[00:32:27] second.
[00:32:29] Okay. So, back to the tool invoker. It's
[00:32:31] basically now taking the name and then
[00:32:34] it's doing a get handler. So, somewhere
[00:32:38] here is a get handler call.
[00:32:41] Here's the handler.
[00:32:43] &gt;&gt; You just passed it.
[00:32:44] &gt;&gt; I just passed it. Sorry.
[00:32:46] &gt;&gt; 17.
[00:32:47] &gt;&gt; 17. Thank you. I appreciate it. So
[00:32:50] here's the get handler and I'll show you
[00:32:51] that function in just a second. So great
[00:32:54] question on the like how tightly bound
[00:32:56] are these things. Let me show you where
[00:32:58] that binding is right now. So I have a
[00:33:00] tools module here and I have in the init
[00:33:04] is where I've got those two functions
[00:33:06] defined. So, I've got the get tools
[00:33:09] and the get tools are basically just
[00:33:12] taking the list of functions and I'll
[00:33:15] show you those functions and those
[00:33:17] functions what we're passing in here is
[00:33:19] we are passing in the JSON blobs that
[00:33:22] are passed to the LLM as the tool
[00:33:24] descriptions. So, these are the tool
[00:33:26] descriptions. So, for example, let me
[00:33:29] show you the get weather one. So, if we
[00:33:31] go over here to get weather, you can see
[00:33:33] that the um the JSON blob is right here.
[00:33:39] And it's interesting because OpenAI
[00:33:42] um in in the completions API, they had a
[00:33:46] public API that allowed you to take any
[00:33:50] function that has dock strings on it and
[00:33:53] generate the JSON for the completions
[00:33:55] API for the tools. The responses API has
[00:33:59] no no such public API. So there's a
[00:34:03] warning in here that says this API that
[00:34:05] I'm using um which is in this tool
[00:34:08] helper. I'll show you the tool helper.
[00:34:12] Where is my tool helper? Uh helpers.
[00:34:15] Here we go. I guess I could put that in
[00:34:17] tools. Is that there's a thing in there
[00:34:19] that says warning. There is currently no
[00:34:22] public API to generate the JSON blob of
[00:34:25] tools for the responses API. So I'm
[00:34:28] using an internal one. There is an open
[00:34:30] issue on this. So there's just a warning
[00:34:33] in there that I'm using an internal one.
[00:34:34] So if we go back there, I've used an
[00:34:37] internal API to just take my get weather
[00:34:41] alerts um request which is the uh it's a
[00:34:46] pyantic model that has the the functions
[00:34:48] in there and has some you know
[00:34:51] additional metadata around it and it
[00:34:53] generates the JSON blob. So again,
[00:34:56] that's what you see when we go into the
[00:34:58] agent is we that's what you're getting
[00:35:00] with get tools is you're getting the the
[00:35:02] the array of JSON blobs for each of the
[00:35:05] tools. And then as I said the get
[00:35:09] handler basically has it it's it's
[00:35:12] basically a dictionary that I've
[00:35:14] implemented as as a set of ifns. So it's
[00:35:17] a takes the tool name and then it picks
[00:35:19] up what the actual function is
[00:35:22] completely independent. And so this
[00:35:24] particular example has a set of and I'm
[00:35:27] going to demo those for you in just a
[00:35:28] second. It has a set of tools here. Um
[00:35:31] and you can just switch those things
[00:35:33] out. You do have to restart your Python
[00:35:35] pro process at the moment just because
[00:35:36] of the way that I've implemented it.
[00:35:39] Okay. Make basic sense. All right. Let
[00:35:42] me show you this in action.
[00:35:46] Um and so what I've got here is I'm
[00:35:48] running uh the worker. I'm not spending
[00:35:51] a lot of time here talking about
[00:35:52] workers, but you remember that I said
[00:35:54] that this is all event driven. Um, and
[00:35:57] so there's something that is picking up
[00:35:59] work off of event cues and then
[00:36:02] executing the right workflows and
[00:36:04] activities based on what it's pulled off
[00:36:06] of the event cues. The the um the thing
[00:36:09] in temporal that does that is what we
[00:36:11] call a worker. So a worker is a process
[00:36:14] that you run. with that worker, you
[00:36:16] register the activities and the
[00:36:18] workflows that that worker is going to
[00:36:19] be responsible for. So it's going to be
[00:36:21] looking for things on the queue to pull
[00:36:23] off of those. That worker itself is
[00:36:25] multi-threaded. So it is not one worker
[00:36:28] one process. Um in general people run it
[00:36:32] depends you can do worker tuning but in
[00:36:34] general people run several hundred
[00:36:36] threads. So you run one worker and it's
[00:36:39] already a a a you know concurrent
[00:36:42] multi-threaded architecture. Okay. So
[00:36:45] this is some solid stuff. Temporal is
[00:36:48] just the coolest stuff. It's really
[00:36:49] truly is distributed systems designed.
[00:36:52] Okay. So I'm running the worker up here,
[00:36:54] which is effectively where you're going
[00:36:55] to see the outputs coming from the
[00:36:57] activities and the workflows. And I'm
[00:36:59] going to go ahead and run um run a
[00:37:03] workflow. And so
[00:37:06] let's say are there any weather alerts
[00:37:10] in California? That's where I'm from.
[00:37:13] And I think a lot of you are from and
[00:37:15] hopefully where I will be headed back to
[00:37:17] tonight. And so we're going to start.
[00:37:20] And what you can see here is the way
[00:37:22] that this application is written is
[00:37:24] basically I I um say whether or not I'm
[00:37:28] calling a tool. And so you can see here
[00:37:30] that it said, oh, I made a call to get
[00:37:32] weather alerts. Um and that is what's
[00:37:35] happening. So there's a tool call that's
[00:37:37] happening. And in just a moment, I
[00:37:39] happen to know that as soon as we get a
[00:37:41] few drops of rain in California, you
[00:37:42] know, there's alerts all over the place.
[00:37:45] So, here we go. Here's a whole bunch of
[00:37:47] weather alerts in California. You'll see
[00:37:49] why I'm I'm pointing that out. It's kind
[00:37:51] of fun. Um, okay. Now, let me show you
[00:37:54] what this looks like in the temporal UI.
[00:37:59] So, over here I have the temporal UI,
[00:38:01] and you can see that I've run a bunch of
[00:38:02] workflows this morning. And so, let me
[00:38:05] refresh refresh this. And this is the
[00:38:07] one that I just ran. And what we see
[00:38:10] here is, yep, there's all of that dense
[00:38:12] fog advisory. That's that's about as as
[00:38:15] extreme as we get in California. A
[00:38:16] little bit of fog, a little bit of wind,
[00:38:18] high surf, beach hazards. But here is
[00:38:23] what happened. So you can see in the
[00:38:25] temporal UI, you can see each one of
[00:38:28] those activities that I called. You can
[00:38:30] see that I made a call to an LLM. That's
[00:38:33] the create line that you see on the
[00:38:34] bottom. So we're working from bottom to
[00:38:36] top. Then you can see that I did a
[00:38:40] dynamic activity, but the dynamic
[00:38:42] activity that I did in particular, it
[00:38:44] doesn't say generic dynamic activity. It
[00:38:46] says I did a get weather alerts. And
[00:38:49] then as we do with agentic loops, we
[00:38:52] take the output of the tool and we send
[00:38:54] it back into the LLM and we get this.
[00:38:57] Now
[00:38:59] I want to show you something here. I'm
[00:39:01] gonna show you a different example. So,
[00:39:05] I'm going to ask the question, are there
[00:39:07] any weather alerts where I'm at? So,
[00:39:10] does it know where I'm at? And I'm going
[00:39:12] to start this. And I'm very going to
[00:39:14] quickly going to come over here and
[00:39:16] we'll see this one running. And you can
[00:39:19] see Oh, I'm going to be too slow it
[00:39:21] looks like, but I'll I'll come back and
[00:39:24] I'll redo this demo. But you can see how
[00:39:25] it just it's, you know, brought those
[00:39:27] things in. So, the other So, I have
[00:39:30] three tools registered right now. I have
[00:39:32] a tool that takes in a state. I have a
[00:39:34] tool that takes in um an IP address and
[00:39:37] returns a state. And I have a tool that
[00:39:40] gives me an IP address for the currently
[00:39:42] running computer. And so I didn't I
[00:39:45] didn't wire that up that the LLM made
[00:39:48] those decisions just based on the tools.
[00:39:50] So all I did was I provided those tools.
[00:39:53] But you can get that visibility across
[00:39:55] this in temporal. So, you can see that
[00:39:58] we started with get IP address, then we
[00:40:00] got the location info from that IP
[00:40:02] address, then we got the weather alerts.
[00:40:04] And here's the ironic thing is there are
[00:40:08] no weather alerts in New York. So, I
[00:40:10] think of New York as a place that has
[00:40:12] much more weather, but maybe today is
[00:40:13] cal. You have fog, but there's no fog
[00:40:16] advisories. So, y'all are a lot more
[00:40:18] resilient than than the rest of us
[00:40:20] Californians.
[00:40:22] Okay. So, I want to show you one other
[00:40:24] thing, which is I'm gonna come back over
[00:40:27] here. I'm gonna run this again, and I'm
[00:40:31] going to try to be I I can be a lot
[00:40:33] quicker. So, I'm going to hit okay. And
[00:40:36] now I'm going to come up here and I'm
[00:40:39] going to control C. No workers running.
[00:40:43] My agent is not running. It's not
[00:40:46] running at all.
[00:40:48] And so if we come over here and we take
[00:40:50] a look at what this looks like in
[00:40:51] temporal and this is going to give you
[00:40:53] the clearest picture of what I mean by
[00:40:55] durability and durable agents is that I
[00:40:58] have this agent running and you can see
[00:41:01] that it made the first LLM call. Then it
[00:41:04] got the made the tool call to the IP
[00:41:06] address and now it's it's stuck. It
[00:41:11] started to call the LLM but hang on it
[00:41:15] something went wrong. the agent itself
[00:41:17] is not running. And by the way, I could
[00:41:19] have also done a demo. And I don't have
[00:41:21] the time to do all of those today, but I
[00:41:23] could have done a demo where I cut the
[00:41:25] the network. So I could have cut the
[00:41:28] network. And what you would have seen
[00:41:29] here in this little red bar is you would
[00:41:31] have seen it. Create attempt one, create
[00:41:34] attempt two, create attempt three. I
[00:41:36] could have brought the network back and
[00:41:37] then it would have gotten through. But
[00:41:39] for brevity here, because I still want
[00:41:40] to I still have more stuff to cover. I'm
[00:41:43] just showing you one of the failure
[00:41:44] scenarios. There's tons of failure
[00:41:46] scenarios that are covered. So, I'm
[00:41:48] going to come back over here and I'm
[00:41:49] going to restart the worker. And what we
[00:41:52] should see happen is, oh, sure enough,
[00:41:55] it keeps going. So, it picked up where
[00:41:58] it left off. Now, when I say it picked
[00:42:00] up where it left off, of course, I
[00:42:03] killed the process. There was nothing
[00:42:06] running in memory anymore. So, when I
[00:42:09] brought the worker back, it had to
[00:42:11] reconstitute the state of the
[00:42:12] application. It did that through event
[00:42:15] sourcing.
[00:42:17] So that's the way temporal works
[00:42:19] fundamentally. Any questions on that?
[00:42:22] Yes.
[00:42:22] &gt;&gt; Can we delegate one agent to another
[00:42:24] agent?
[00:42:25] &gt;&gt; Can you delegate one agent to another
[00:42:27] agent? Absolutely. Now we do not yet
[00:42:30] have native support for A to A if you're
[00:42:32] thinking about that protocol in
[00:42:34] particular. But one of the things that
[00:42:36] you can certainly do is that you can
[00:42:38] have an agent act as a tool. And so
[00:42:42] there are a number of different ways to
[00:42:44] do that. You can either have an activity
[00:42:46] invoke another agent or you can use some
[00:42:49] other mechanisms. We have child
[00:42:50] workflows and those types of things. I'm
[00:42:52] not going to cover that more advanced
[00:42:53] use case. But yeah, absolutely.
[00:42:56] &gt;&gt; A couple of questions. One thing is the
[00:42:58] way you are coding it. It seemed the
[00:43:00] functions very itemed. There was like
[00:43:02] one single line essentially. uh how to
[00:43:06] make sure that the developers are you
[00:43:08] know creating function so that the
[00:43:09] retries are posing a lot so
[00:43:14] &gt;&gt; second question is the latency just
[00:43:15] added through because of the framework
[00:43:17] &gt;&gt; okay I'll so first question is about
[00:43:19] around item potence so you have
[00:43:22] recognized that um the activity
[00:43:26] activities themselves should be item
[00:43:28] potent um we don't require it we don't
[00:43:32] check on it because We really don't get
[00:43:34] into the inner workings of the
[00:43:35] activities. We leave that up to the
[00:43:37] developers. Um but that is the the
[00:43:40] guidance is that if they're not item
[00:43:42] potent because remember that when we do
[00:43:44] retries on your behalf, we don't know wh
[00:43:50] why we never heard back from the first
[00:43:52] invocation. So we are going to keep
[00:43:54] retrying until we get back a response.
[00:43:57] Of course it could be that the request
[00:43:59] never made it to the activity. It could
[00:44:01] be that it made it and it invoked the
[00:44:03] downstream function could have gone
[00:44:05] wrong in a number of places. So how do
[00:44:07] you make sure that your developers are
[00:44:08] doing uh creating your activities to be
[00:44:11] item potent education. So we don't have
[00:44:14] any silver bullets there. The second
[00:44:16] question was around latency because yes
[00:44:19] I am going up to the server here um with
[00:44:22] every one of those activity calls and so
[00:44:26] when we when we think about agents um we
[00:44:30] the type of latency and Johan I don't
[00:44:33] remember the exact numbers do you
[00:44:34] remember what the numbers are I mean
[00:44:36] it's tiny the latency to go up to the
[00:44:38] server around activities
[00:44:40] &gt;&gt; u so it's going to depend a bit where
[00:44:42] the server is but it's tens of
[00:44:44] milliseconds
[00:44:45] &gt;&gt; tens of millc seconds. So it's pretty
[00:44:47] small. Um so whether I I I think I have
[00:44:51] heard of several customers who are using
[00:44:53] this in quite realtime applications. But
[00:44:56] in the case of agents, especially agents
[00:44:58] where they're long running and they're
[00:45:00] running over minutes, hours, days, or
[00:45:03] they have user interaction, tens of
[00:45:05] milliseconds is is is tolerable. So
[00:45:07] there might be use cases where it's not
[00:45:10] applicable because of that latency, but
[00:45:12] it's pretty small. It's applicable in
[00:45:14] most cases.
[00:45:16] Okay. All right. So, that is the
[00:45:18] temporal overview. Now, I want to switch
[00:45:21] back over to the agents SDK now and show
[00:45:25] you the differences and the
[00:45:28] similarities. So, let's come back over
[00:45:31] here. I'm going to go through a few more
[00:45:33] pictures.
[00:45:37] Okay. So the OpenAI agents SDK the
[00:45:41] combination of these two things at a
[00:45:43] very high level looks like this. At the
[00:45:46] foundation we have the OpenAI models and
[00:45:50] the OpenAI API not the SDK but the
[00:45:53] OpenAI API. So you might have noticed
[00:45:56] that I've already been using the OpenAI
[00:45:58] API and we're now going to start using
[00:46:00] the agents SDK. And then we also have
[00:46:03] temporal as a foundational element. And
[00:46:07] now that's what the agents SDK is
[00:46:10] layered over the top. So those are two
[00:46:12] foundational components. So it isn't
[00:46:14] that we're making that temporal sitting
[00:46:17] on the side or open AI models are
[00:46:20] sitting on the side. We have actually
[00:46:21] integrated these things and I'll make
[00:46:23] some comments when we get to the code on
[00:46:25] how we did that integration and I'll
[00:46:27] totally invite Johan to add to that as
[00:46:30] well because he led the in led the the
[00:46:32] engineering for the integration here. So
[00:46:34] now you've got the agents SDK and now
[00:46:36] you're going to use the agents SDK to
[00:46:38] build your agents to add guard rails.
[00:46:42] We're going to I'm going to show you
[00:46:43] some tracing. So I showed you the
[00:46:45] temporal UI, but the agents SDK has some
[00:46:48] really cool tracing features as well.
[00:46:50] And you'll see that we've integrated
[00:46:52] those things together. You're going to
[00:46:53] see those come together. And of course
[00:46:55] tools.
[00:46:57] So I've been talking about these
[00:46:59] temporal activities and we already saw
[00:47:01] this. I'll skip that. uh skip that. Um
[00:47:04] and so now uh we're I'm going to take
[00:47:07] the same exact example that we just went
[00:47:10] through. I'm going to have three tools.
[00:47:13] One is the weather API and the other two
[00:47:16] are those location APIs. And what are we
[00:47:19] going to do? Well, we're going to put
[00:47:20] activity decorators around them. And
[00:47:23] I'll show you what that looks like in
[00:47:24] the other codebase in just a moment. We
[00:47:26] are going to make sure we have doc
[00:47:28] strings in there because I showed you
[00:47:31] how the open AAI API had the um the uh
[00:47:37] the internal helper function that
[00:47:39] allowed us to generate the JSON blobs to
[00:47:41] describe the tools. Well, the agents SDK
[00:47:44] actually does even more of that for us.
[00:47:46] So, you'll see that some of my code went
[00:47:48] away. Um and then uh yeah, and then
[00:47:51] we'll we'll car continue on from that.
[00:47:53] And then and this is going to be our
[00:47:54] loop here.
[00:47:56] I'm going to show you when we get to the
[00:47:58] code that the um the way that we create
[00:48:02] that JSON blob is part of the
[00:48:04] integration. So you can take an activity
[00:48:07] and we have provided for you a function
[00:48:10] called activity as tool that will take
[00:48:13] in the activity the function itself. So
[00:48:15] you don't have to worry about
[00:48:16] serializing it yourself. No internal
[00:48:18] APIs. This is a public API. It's part of
[00:48:21] the in the integration. and you're going
[00:48:23] to call activity as tool which is going
[00:48:25] to generate the um the JSON blob and
[00:48:27] then you can have your timeouts as well.
[00:48:30] There's another part which is really
[00:48:32] important which is that you have to
[00:48:35] configure the integration. So you have
[00:48:38] to the agents SDK alone doesn't use
[00:48:42] temporal and if you want to use temporal
[00:48:45] you need to make sure that you include a
[00:48:47] plugin and I'll show you the code for
[00:48:49] that in just a second. And then of
[00:48:52] course we're going to run it and we're
[00:48:54] going to run it the same basic way.
[00:48:57] Okay. So let's demo that. So we're going
[00:49:00] to spend a lot more time in code and
[00:49:02] demo again. Let me come back over to
[00:49:04] cursor. Okay. So I've got four four
[00:49:08] files that I want to show you here. I'm
[00:49:10] going to start with the activities
[00:49:12] again. So here's the get weather
[00:49:14] activity and you'll see that it actually
[00:49:16] got a bit simpler. It's just has the
[00:49:20] activity decorator on the get weather
[00:49:23] alerts and then here's the function
[00:49:24] where it actually makes the the U
[00:49:26] National Weather Service API. So there
[00:49:29] was another there was a bit of um code
[00:49:31] in there that was doing some formatting
[00:49:35] where it made that API call to generate
[00:49:37] the JSON blob that goes away because we
[00:49:39] have a a supported function for that.
[00:49:42] The location activities equally simple.
[00:49:45] So literally this is the entire file. So
[00:49:48] I've got these two functions with the
[00:49:50] activity decorators and my dock strings.
[00:49:54] So the doc strings are describing the
[00:49:56] the arguments and so on. Okay. So now
[00:50:02] what about the agent itself? So remember
[00:50:05] activities were just the things that
[00:50:07] those were the tools that the agent was
[00:50:09] using. What I showed you before was an
[00:50:11] agentic loop written in Python that was
[00:50:15] orchestrating the LLM call and the tool
[00:50:17] invocations.
[00:50:19] So now if I come over to the workflow,
[00:50:22] what does my workflow look like? This is
[00:50:24] it.
[00:50:26] So I have
[00:50:28] sorry this is it. This is the workflow.
[00:50:32] Okay. And it's basically let me increase
[00:50:35] the font size because I have plenty of
[00:50:37] space. is notice that I'm using the
[00:50:40] agents SDK. So I'm defining an agent
[00:50:43] right here on line 18. I'm giving it a
[00:50:46] name, your helpful agent, and I'm giving
[00:50:49] it a set of tools. Those tools were
[00:50:52] implemented as activities.
[00:50:55] And there you can see that I've made the
[00:50:57] function call that says activity as tool
[00:50:59] that generates the JSON blob.
[00:51:02] That's it.
[00:51:04] That's all there is to it. That's the
[00:51:06] way I've implemented it. Now notice that
[00:51:08] I'm still doing it within the workflow
[00:51:10] because remember earlier I said we've
[00:51:12] got activities, we've got workflows.
[00:51:14] When you put them together, that's where
[00:51:15] the magic happens. So putting this agent
[00:51:18] inside of a workflow, that's what adds
[00:51:21] all of these durability capabilities.
[00:51:24] Now I am not going to demo the
[00:51:26] non-durable version of this because
[00:51:28] again we just have constrained time here
[00:51:31] today. But if I had implemented this
[00:51:34] with just the agents SDK, which is just
[00:51:37] a Python library, I would have had a
[00:51:39] single process. And if I killed that
[00:51:42] process, it everything would have gone
[00:51:44] away with it. I there's no way for me to
[00:51:46] scale that process. And remember, I've
[00:51:49] got an a runner.run right down here,
[00:51:52] right? So every one of those runners I
[00:51:55] it's just it's just a it's a monolithic
[00:51:58] agent, right? It's just one Python
[00:52:01] process. By doing it this way, you can
[00:52:04] see that if I'm running multiple
[00:52:06] workers, I can just keep scaling this
[00:52:07] out by just running multiple workers who
[00:52:09] are just pulling other things off of the
[00:52:11] queue.
[00:52:13] &gt;&gt; Yes.
[00:52:13] &gt;&gt; Do handoffs to other agents work?
[00:52:15] &gt;&gt; Do handoffs to other agents work? Yes.
[00:52:18] And I'm going to come back to that in
[00:52:19] the final section where we're going to
[00:52:20] talk about orchestrations. Um, yes, they
[00:52:23] do. Absolutely. Um, okay. So, now let me
[00:52:28] go to uh I need to I do need to get one
[00:52:31] other thing out of here. I need to get
[00:52:33] my worker.
[00:52:35] Um where is my worker?
[00:52:42] Here's my worker.
[00:52:47] because it's in the worker where
[00:52:54] where's the plugin? Johan, help me out.
[00:52:58] &gt;&gt; I just passed it. Oh, here we go. OpenAI
[00:53:01] agents plugin. Okay, so it's in the
[00:53:04] worker. Remember the worker is where all
[00:53:06] the execution is happening. Think of it
[00:53:08] as kind of like a logical metaphorical
[00:53:10] container. And oftentimes you are
[00:53:12] running the workers in containers. And
[00:53:15] here's the configuration that you need
[00:53:16] to put in there. It's those and notice
[00:53:19] that it's doing things like it it is um
[00:53:22] configuring some of the retry behavior
[00:53:25] around the LLM. You'll notice, did you
[00:53:28] notice that I did not give you an
[00:53:30] activity for invoking the LLM
[00:53:33] that's done as a part of the agent, but
[00:53:35] we still want that to be durable. And
[00:53:38] that's what one of the things that our
[00:53:40] implementation does here. So you're
[00:53:42] doing some retry policies for the LLM
[00:53:44] and you're basically saying hey a open
[00:53:47] AI agents SDK use these parts of
[00:53:50] temporal.
[00:53:52] So let me tell you a little bit about
[00:53:54] what we did as a part of the
[00:53:56] integration. What we did if you go back
[00:53:59] and you look at the commit history of
[00:54:01] the OpenAI agents SDK you'll find a
[00:54:03] commit where it says make the runner
[00:54:06] class abstract.
[00:54:09] They did that for us because that's how
[00:54:11] we imple that's how we got this
[00:54:13] durability. That's how we were able to
[00:54:15] make the LLM calls durable along with
[00:54:18] all of the tools that you just saw. So
[00:54:21] we have our own implementation of the
[00:54:24] abstract runner class. So that is the
[00:54:28] way that this works. Okay. So we've
[00:54:31] looked at the activities, we've looked
[00:54:33] at the workflow, and then we run the
[00:54:36] tools workflow. So, I don't think
[00:54:38] there's anything more to look at there.
[00:54:40] So, let's go over
[00:54:42] to
[00:54:45] this. Um, let me find my right window.
[00:54:51] It is this window.
[00:54:54] Okay. So, what I'm doing in this window,
[00:54:57] let me go ahead and increase my font
[00:54:58] size a little bit. Is up here in the top
[00:55:02] window. And I'm going to exit out of
[00:55:03] these because I only need two.
[00:55:07] Okay. So, in the top window, I'm running
[00:55:10] my worker again. You saw that before.
[00:55:12] So, I'm running the worker up there. And
[00:55:15] so, it's got a little bit of, you know,
[00:55:16] log messages that are going to come out.
[00:55:19] And then down here is where I'm starting
[00:55:21] the workflow. Here's where I'm
[00:55:22] interacting with the agent. So, I'm
[00:55:26] going to I just pushed some of this
[00:55:28] stuff. Oh, I'll show you the the
[00:55:29] repository in just a second. So, are
[00:55:32] there any weather alerts in California?
[00:55:35] And remember the code. The code is just
[00:55:37] that agent, right? We've still
[00:55:39] implemented our activities, but the code
[00:55:41] is that agent and we are checking and
[00:55:45] you can see the things that are
[00:55:46] scrolling up there. So, you can see
[00:55:48] actually the uh API calls to the LLM.
[00:55:52] You can see the API call to the National
[00:55:54] Weather Service. And so if we come back
[00:55:56] over to the temporal
[00:56:00] UI,
[00:56:04] it's a different it's called tools
[00:56:05] workflow. Here you can see it looks
[00:56:09] exactly the same,
[00:56:12] right? And that's why I wanted to spend
[00:56:14] some time showing it to you with
[00:56:16] temporal because temporal, if you're
[00:56:17] building these temporal native
[00:56:19] applications, you get all this
[00:56:20] durability. You get this visibility. It
[00:56:23] looks exactly the same, but you were
[00:56:25] using the agents SDK to implement your
[00:56:28] agents, which I think is just so cool.
[00:56:30] So, let's run a second one.
[00:56:34] And uh I'll show you the repository in
[00:56:38] just a second. We're going to run this
[00:56:40] second example which are are there any
[00:56:42] weather alerts where I am. And we're
[00:56:44] going to come over here. We'll watch it
[00:56:46] in progress.
[00:56:48] So here it's running.
[00:56:50] And it's running exactly the same way.
[00:56:54] And I'm going to run it one more time
[00:56:56] when it comes back. And it says, "Nope,
[00:56:58] you're good in New York." Let me run it
[00:57:00] one more time. I'll let it get started.
[00:57:03] Get part of the way in. Control C out of
[00:57:06] this. And we come back here
[00:57:12] and we see the same thing that we saw
[00:57:14] before, right? Agents SDK durable,
[00:57:20] which is so sweet. I I sorry I get I I
[00:57:25] do this all the time, but I still get so
[00:57:26] excited about this. Um
[00:57:30] and there it goes.
[00:57:32] I'm going to share with you like um um a
[00:57:35] a way to think about this intuitively
[00:57:37] what we're doing here. I've been writing
[00:57:39] software for over 30 years. Yes, I have
[00:57:42] the gray hair to prove it, right? I have
[00:57:45] I have written that software where I
[00:57:47] when I'm writing the software, I'm
[00:57:49] thinking about the processes that it
[00:57:51] runs in. I'm thinking about the fact
[00:57:54] that oh I've got a process here and what
[00:57:56] happens if something happens to that
[00:57:57] process or as I'm scaling things out and
[00:58:00] things might not run in the same
[00:58:01] processes I'm always thinking about
[00:58:04] processes
[00:58:05] with temporal what you get to do is you
[00:58:08] get to write your program thinking about
[00:58:10] a process as a logical entity and just
[00:58:14] let temporal map it down to the actual
[00:58:17] physical processes that are there. This
[00:58:19] is particularly
[00:58:22] it it's it's so cool to look at when you
[00:58:24] do things like human in the loop. So
[00:58:26] earlier this week I did another I've
[00:58:28] done another I another one of the talks
[00:58:30] that I do is around human in the loop
[00:58:31] with agents and one of the big pains of
[00:58:35] human in the loop is that when you're
[00:58:37] thinking about building these things and
[00:58:39] you're thinking about the processes
[00:58:41] you're like okay I need to run for a
[00:58:43] little while and now I'm going to wait
[00:58:44] for the human in the loop and it might
[00:58:46] take a second it might take a minute
[00:58:48] likely it's going to take hours or days
[00:58:51] before this human comes back. What do I
[00:58:53] do with that process that's waiting for
[00:58:55] that response in the meantime? Like you
[00:58:58] as a developer have to figure that out.
[00:59:00] With temporal, you don't. You just code
[00:59:03] it as if that process. And by the way,
[00:59:06] the way that the worker architecture
[00:59:08] works is that if it's waiting on
[00:59:11] something like human input,
[00:59:13] it it'll keep it in memory for a little
[00:59:15] while, few seconds, then it'll take it
[00:59:18] out of active memory, but it's still
[00:59:20] sitting in a cache. And after a little
[00:59:22] bit more time, it'll come out of the
[00:59:24] cache and it'll be just as if you had
[00:59:27] just killed that process. So that when
[00:59:29] it does come back after days or weeks,
[00:59:32] when the user comes back and gives you
[00:59:33] that input, it just reconstitutes memory
[00:59:37] the way that it was when it was waiting
[00:59:38] for the user and continues on. So
[00:59:42] remember I said it's a crash or it might
[00:59:43] be other things, operational things, all
[00:59:46] of those types of things. So, it's so
[00:59:49] freeing once you start to really get
[00:59:51] into this temporal thing. It is so
[00:59:53] freeing to realize that I don't have to
[00:59:56] think about physical processes anymore.
[00:59:58] To me, the processes are just logical.
[01:00:00] Temporal takes care of the rest for me.
[01:00:03] Super cool stuff. All right, we have
[01:00:06] about uh 20 minutes left. I'm going to
[01:00:10] go through just a couple more slides to
[01:00:12] answer one of the questions around
[01:00:13] handoffs.
[01:00:15] um and just show you just a little bit
[01:00:18] more content and then we're we'll have a
[01:00:20] little bit of time in the last I don't
[01:00:22] know maybe 10 you know 10 or 15 minutes
[01:00:24] I'm happy to take more questions and
[01:00:26] Johan would be I'm sure very happy to to
[01:00:29] jump in as well. Okay. So, let me
[01:00:34] So, um
[01:00:37] there are with the OpenAI agents SDK.
[01:00:40] This is what I'm talking about here is
[01:00:42] somewhat specific to the agents SDK, but
[01:00:44] this does kind of generalize to agents
[01:00:48] in general, which is with the open AI
[01:00:51] agents SDK. The kind of paradigm that
[01:00:54] they use there is to build lots of small
[01:00:57] agents that have their own independent
[01:01:00] agentic loops and then orchestrate them
[01:01:03] together. And there's two ways that you
[01:01:06] can orchestrate them together in the
[01:01:07] agents SDK. And I'm going to show you
[01:01:10] both of those in just a moment. So what
[01:01:12] we see here on the screen are just a
[01:01:14] couple of diagrams of like, okay, I've
[01:01:18] got a triage agent. I've got a
[01:01:20] clarification agent. Then I've got a
[01:01:22] human in the loop. That's not an agent.
[01:01:24] Although you might think of the human as
[01:01:27] the agent in this application, right?
[01:01:30] Then I've got an instructions agent
[01:01:32] that's going to craft some stuff. Then
[01:01:34] I've got a planning agent. Then you can
[01:01:35] see that we're doing things in parallel.
[01:01:37] I didn't talk about this, but temporal
[01:01:40] has all those abstractions. You can
[01:01:42] anything that you can write in a regular
[01:01:44] programming language, you want to do
[01:01:47] multi-threaded and have a bunch of
[01:01:49] different threads and do things in
[01:01:50] parallel and then wait for them to come
[01:01:52] back together. You can do that. You want
[01:01:54] to have some kind of an await that says,
[01:01:56] you know what, as they start coming in,
[01:01:58] I'll start processing them. No problem.
[01:02:00] You can do that. Anything that you can
[01:02:02] do in code, you can do with temporal
[01:02:04] because you're just coding. So that's
[01:02:07] effectively the way that it works here
[01:02:08] with the agent SDK as well. Um I'll show
[01:02:11] you those things again as well. So you
[01:02:13] can do parallel, you can have long
[01:02:15] weights. Um and you can have loops. So I
[01:02:19] already showed you the fact that I
[01:02:21] didn't have to craft my logic in the
[01:02:25] Python. The logic the LLM made the
[01:02:28] decisions on how the flow was going to
[01:02:29] happen in that application. Right? So I
[01:02:32] just had a loop that the loop itself is
[01:02:35] like fixed, but what happens in the loop
[01:02:37] is entirely determined by the LLM. So
[01:02:40] that those are all things that you can
[01:02:42] do. So there's two ways with the agents
[01:02:45] SDK that you can orchestrate these
[01:02:47] microaggents. And by the way, I just
[01:02:50] have to say I love the term microaggent.
[01:02:52] As I mentioned early on, um I uh I spent
[01:02:56] a lot of time in the microservices world
[01:02:58] and oh my gosh, did we get a lot of
[01:03:00] mileage out of that, right? That's the
[01:03:03] reason that we can deploy software
[01:03:04] multiple times a day. That's the reason
[01:03:06] why we can scale the way we can scale.
[01:03:09] Microservices have proven themselves to
[01:03:11] be very valuable. we I think we're going
[01:03:14] to see a very similar paradigm, very
[01:03:17] similar success when it comes to
[01:03:19] building AI agents, MCP tools, and all
[01:03:21] of that kind of stuff. So, I love the
[01:03:23] the notion of microaggents that do one
[01:03:26] thing and one thing well. I've spent
[01:03:27] enough time in the land of Unix as well
[01:03:30] that makes my heart sing.
[01:03:32] So, just code and handoffs. The just
[01:03:35] code is really simple. It's what I
[01:03:37] described um before. So, you can see
[01:03:39] here that I have a runner.run. I'm
[01:03:41] executing an agent. I get back a result
[01:03:44] from that agent and I pass that result
[01:03:46] into the next agent. I can parallelize,
[01:03:50] I can loop, I can do whatever I want.
[01:03:53] The second way that Oh yeah, and I
[01:03:56] already showed all that. Um, so yeah.
[01:03:59] Yeah, I I mentioned all of those
[01:04:01] already. Um, the second uh uh way that
[01:04:05] Open AAI and were you talking about Open
[01:04:06] AI specifically when you were asking
[01:04:08] about handoffs? Yeah. So for those of
[01:04:10] you who don't know, OpenAI has a second
[01:04:13] way of doing orchestrations which are
[01:04:15] called handoffs. And so what you see
[01:04:17] here is that in my definition of an
[01:04:19] agent, I can define handoffs. Those
[01:04:22] handoffs are other agents. They've been
[01:04:25] defined. I probably should have it on
[01:04:27] the slide, but I have a weather agent
[01:04:29] that is defined very similarly. It's
[01:04:31] using agent has a name, has
[01:04:34] instructions, might have tools.
[01:04:37] So these two are agents.
[01:04:40] Um and all of this works with the the
[01:04:42] the e the integration with with um
[01:04:45] temporal and but what's interesting here
[01:04:48] is that those microaggents when it hands
[01:04:51] off to an agent it is not doing a
[01:04:55] separate agentic loop. it effectively
[01:04:58] and this is my wacky attempt at trying
[01:05:02] to describe what's happening here is
[01:05:04] that when you do a handoff what you're
[01:05:06] effectively doing is just changing the
[01:05:08] context of the agentic loop so the a
[01:05:12] there's one single agentic loop you have
[01:05:15] a triage agent for example it decides
[01:05:18] that it's going to go into delivering I
[01:05:21] worked at Alexa for a while so did you
[01:05:23] ask how late is Costco open or did you
[01:05:25] ask what the current temperature is
[01:05:27] right. So those are two different
[01:05:28] agents, the weather and the local info
[01:05:31] agent. And what you're effectively doing
[01:05:33] is you are that that agentic loop is
[01:05:36] taking on a different persona. You're
[01:05:38] just switching the context. And we heard
[01:05:40] lots of talks this week about context
[01:05:42] engineering because that's the beautiful
[01:05:44] thing about the LLMs being forgetful is
[01:05:46] that you can just you can completely
[01:05:47] control what you want, what the context
[01:05:50] is that's going into them. So this works
[01:05:52] exactly. So temporal is totally handoff.
[01:05:55] I don't have a live demo of that. Um,
[01:05:58] and so that's it. Okay. So, with that,
[01:06:01] we're going to have a few minutes left
[01:06:02] for questions. I want to leave you with
[01:06:05] a few resources. So, what you see here
[01:06:08] on the um left hand side is you see a QR
[01:06:12] code for the uh temporal Python SDK.
[01:06:18] You'll find lots of great info on our
[01:06:20] Python SDK, but you'll also find a
[01:06:22] contrib directory and that's where all
[01:06:25] of the integration code to the OpenAI
[01:06:28] agents SDK is. And you'll find lots of
[01:06:31] samples in there. On the right hand
[01:06:33] side, I didn't have a QR code for it
[01:06:36] because my marketing folks don't work on
[01:06:38] Saturday mornings. Good for them. Um, is
[01:06:41] you will see a URL UR URL here. So, if
[01:06:45] you go to our documentation, so
[01:06:46] docs.temper temporal.io. At in the top
[01:06:49] banner, you'll find AI cookbook. We have
[01:06:51] an AI cookbook that implements a bunch
[01:06:54] of patterns. The one that I showed you
[01:06:56] today, the Agentic Loop, is in a um
[01:06:59] branch at the moment. It is ready to be
[01:07:01] merged. It's been reviewed, but my
[01:07:03] reviewer didn't actually give it an
[01:07:05] approval review. They just reviewed it
[01:07:07] and said, "Looks good, but I need an
[01:07:09] approved, so I couldn't merge it this
[01:07:10] morning." Um, but that uh recipe will be
[01:07:13] up there. And there's a number of
[01:07:14] others. There's a recipe in there for
[01:07:16] OpenAI agents SDK. So you'll find that
[01:07:18] in there as well. Um, so summing it up,
[01:07:22] I don't I'm not going to belabor that. I
[01:07:24] think we went over that as well. Two
[01:07:26] other resources that I want to leave you
[01:07:28] with is on the left hand side you'll
[01:07:30] find our blog where we describe the
[01:07:33] integration of the OpenAI agents SDK and
[01:07:36] Temporal. So that's the blog on the left
[01:07:38] hand side. The other thing you'll notice
[01:07:41] is that that I have a paidantic blog
[01:07:43] there. And so this idea of in bringing
[01:07:47] durability to these otherwise
[01:07:49] non-durable a you know agent frameworks
[01:07:52] is a very popular one. So after we did
[01:07:55] open AAI agents SDK pyantic themselves
[01:07:59] integrated temporal into their agent
[01:08:01] framework and Johan do you I I don't
[01:08:04] know which ones we can talk about. We
[01:08:06] have a whole bunch of other ones in
[01:08:08] progress. Is that all we want to say or
[01:08:10] do you want to talk about any of those
[01:08:11] in specific? That's that's all for
[01:08:13] today, but there's more coming.
[01:08:14] &gt;&gt; Yeah, I think we have two or three or
[01:08:17] four that are in progress right now that
[01:08:20] will be popping out either from us or
[01:08:22] from some of the other agentic
[01:08:24] frameworks. So, this idea of bringing
[01:08:27] durability to what is otherwise kind of
[01:08:29] just a a proof of concept tool is is
[01:08:33] turning out to be quite powerful. And
[01:08:35] then finally, if you would be so
[01:08:37] inclined, here's a QR code and a URL. If
[01:08:40] you want to give us some feedback on
[01:08:42] this workshop, we'd really appreciate
[01:08:44] it. Um, and include in that feedback.
[01:08:47] There's some free form in there. Include
[01:08:49] in that feedback what you'd like to see
[01:08:51] more of. Like, hey, this was cool, but
[01:08:54] it didn't go far enough or you mentioned
[01:08:56] this. I'd really I'd really like to see
[01:08:58] more about Human in the Loop. By the
[01:09:00] way, if you go on our YouTube channel,
[01:09:01] you will find a bunch of different
[01:09:04] presentations. So, the human in the
[01:09:06] loop, I did a webinar on that like three
[01:09:08] weeks ago. We've done some MCP module,
[01:09:10] MCP things, even advanced. So, we did an
[01:09:13] advanced one where where we showed you
[01:09:15] how you can use temporal to implement an
[01:09:17] MCP server that is durable and supports
[01:09:20] sampling and elicitation in a much more
[01:09:23] durable way than it otherwise is. Um,
[01:09:27] and with that, we still have now about
[01:09:30] eight minutes. Um, so, oh, I'll also
[01:09:33] mention, especially if you're in the Bay
[01:09:35] Area, but if you even if you're not, is
[01:09:38] that our conference, our replay
[01:09:40] conference, the temporal conference, um,
[01:09:42] is in May and it's going to be at
[01:09:45] Moscone. And so, we sure would love to
[01:09:47] see you there as well. And oh, I you
[01:09:50] know this this QR code here was meant
[01:09:53] for the workshop that I did on Tuesday,
[01:09:55] but heck, might as well use it here. 75%
[01:09:59] off. Yes, 75% off the registration um
[01:10:04] for uh replay. So, invite you to come
[01:10:07] there. You'll find me, you'll find
[01:10:09] Johan, you'll find a whole bunch more of
[01:10:11] us. And you can see that we've got all
[01:10:12] sorts of really cool people like Samuel
[01:10:14] Coven is coming and we've got like
[01:10:17] people from Replet and Nvidia and lots
[01:10:21] more coming. So I'll leave the feedback
[01:10:23] up there. So we have a few minutes left
[01:10:25] for questions.
[01:10:28] &gt;&gt; Um how state saved temporal
[01:10:30] &gt;&gt; how is state saved?
[01:10:31] &gt;&gt; You shut down the server it just loses
[01:10:33] all memory of all the workers.
[01:10:36] &gt;&gt; Yeah. Okay. So you're talking about the
[01:10:38] temporal server that I showed you how
[01:10:39] you can run it locally. So when you're
[01:10:41] running it locally, you can put a switch
[01:10:42] on there that says, "Hey, store it in a
[01:10:44] like SQL light or something like that."
[01:10:47] So you can there is there's state that
[01:10:49] backs it. I usually don't run that way
[01:10:52] because I want to throw away things
[01:10:53] anyway. Um,
[01:10:56] so Temporal is open source and we have
[01:10:59] lots of users that self-host it. Because
[01:11:01] it's open source, we literally at events
[01:11:03] like this always run into people. I ran
[01:11:05] into somebody yesterday or something who
[01:11:07] was like, "Oh yeah, we're using
[01:11:09] Temporal." And I'm like, and they're
[01:11:10] just using the open source. Um, so it's
[01:11:13] it truly is open- source. Um, and so we
[01:11:16] do have people who are self-hosting it
[01:11:18] and we support relational database and
[01:11:20] Cassandra as the backing stores on
[01:11:22] temporal cloud. Part of the reason that
[01:11:25] um that people come to cloud is that
[01:11:28] first of all, we run cloud in 15
[01:11:30] different Amazon regions. Uh I don't
[01:11:33] know four, five, six Google regions. We
[01:11:36] have multi-reion namespaces. All of that
[01:11:38] durability. And then we do also have
[01:11:40] some special sauce on the persistence
[01:11:43] that allows us to do things more
[01:11:44] efficiently. Um uh but we have people
[01:11:47] who are hosting it quite quite
[01:11:49] successfully using the Cassandra or the
[01:11:51] database options. So yeah,
[01:11:56] any other questions? Yes.
[01:11:58] &gt;&gt; Start and stop the agents.
[01:12:00] &gt;&gt; When I start and stop the instance the
[01:12:02] agent you mean? I mean how do we stop it
[01:12:05] if the user wants to stop it
[01:12:08] &gt;&gt; the work so
[01:12:09] &gt;&gt; the workflow
[01:12:10] &gt;&gt; yeah
[01:12:12] um so there there are a couple of
[01:12:14] different ways that you can start a
[01:12:16] workflow you can start a workflow
[01:12:17] expecting it to be you know synchronous
[01:12:19] and it just ends and you would have to
[01:12:20] have some kind of a kill on that but
[01:12:22] more commonly you're going to start it
[01:12:24] in an async mode and you're going to get
[01:12:26] back a handle and then you can do things
[01:12:28] against that handle to stop workflows.
[01:12:31] Um but generally the the most common
[01:12:33] thing is that you are going to define in
[01:12:35] your logic what it means to have
[01:12:38] completed that agentic experience or
[01:12:40] completed that workflow in some way
[01:12:42] shape or form. And so you will decide oh
[01:12:45] I'm done now and you'll just return. So
[01:12:48] it's really as simple as doing a return
[01:12:50] from it. It's that's a good question
[01:12:52] though since we're talking about these
[01:12:53] asynchronous things. I didn't talk about
[01:12:55] it in this session, but one of the
[01:12:57] really powerful things is that these
[01:12:59] workflows can run for hours, minutes,
[01:13:01] days, weeks, months, years, and it's
[01:13:04] super efficient. And what we what a
[01:13:07] pattern that a lot of our users use is
[01:13:09] they use it they use a workflow as kind
[01:13:12] of a digital twin of something else. We
[01:13:15] call it entity workflows as well. So,
[01:13:18] for example, you might have a workflow
[01:13:20] that corresponds to a loyalty customer
[01:13:25] and every time that loyalty customer
[01:13:27] scans their QR code at the checkout
[01:13:29] register, it'll send a signal into the
[01:13:32] workflow and the workflow is otherwise
[01:13:34] not consuming any resources and it will
[01:13:37] just pop up, take the signal, process
[01:13:39] what it needs to and go away again. So
[01:13:42] that is a very very common pattern is
[01:13:44] this notion of digital workflows as
[01:13:46] digital twins of some um other processor
[01:13:50] some other entity. Super super powerful.
[01:13:53] Lots of people use that.
[01:13:56] &gt;&gt; Another one.
[01:13:56] &gt;&gt; Yeah.
[01:13:57] &gt;&gt; Um so if work goes down and you've got
[01:14:00] it like in that block state where it's
[01:14:02] just sitting,
[01:14:03] &gt;&gt; how do you guys have any kind of
[01:14:05] integration with like incident
[01:14:06] management things that would like
[01:14:07] trigger an alert so that engineer can
[01:14:10] come in the worker? Yeah. So we we as
[01:14:14] far as I know we do not have those
[01:14:15] integrations but we our customers build
[01:14:18] those integrations.
[01:14:19] &gt;&gt; Yeah. Yeah. They absolutely build those
[01:14:21] on top. Whether we have some of those in
[01:14:23] cloud I'm not sure but it isn't
[01:14:25] something like we don't have like native
[01:14:27] Slack connectors or those types of
[01:14:29] things. And some of that of course
[01:14:31] wouldn't necessarily be a temporal
[01:14:33] thing. Like if you're running your
[01:14:34] workers on Kubernetes, you might have um
[01:14:38] set up your Kubernetes configuration so
[01:14:40] that when the when the um when the
[01:14:42] container goes down, you're going to get
[01:14:44] alerts or when you see something in the
[01:14:46] Kubernetes dashboard where oh gosh, like
[01:14:48] my autoscaler and of course you can have
[01:14:50] these workers and you you can have them
[01:14:52] running in on Kubernetes with
[01:14:54] autoscalers. So a lot of that or you
[01:14:57] know that like it orchestration stuff
[01:15:00] probably would come through your
[01:15:01] operational environment. Um you are
[01:15:04] that's actually a really good point is
[01:15:05] that we host the server but we do not
[01:15:07] host the workloads for you. So you're
[01:15:10] hosting the work workloads yourself.
[01:15:12] Most people love that because they want
[01:15:14] complete control over that. We are
[01:15:16] toying with the idea in some instances
[01:15:19] of maybe hosting workers in the future
[01:15:20] but that's nothing on the road map right
[01:15:23] now.
[01:15:24] So yes,
[01:15:26] &gt;&gt; examples of people building like voice
[01:15:29] agents with temporal or
[01:15:31] &gt;&gt; examples of people building voice agents
[01:15:33] with temporal. I don't know of any
[01:15:35] offhand.
[01:15:37] I
[01:15:37] &gt;&gt; I don't know of any that are deployed.
[01:15:40] Um people are experimenting with it.
[01:15:42] We're experimenting with voice agents.
[01:15:44] Um and it's definitely something that
[01:15:46] that makes sense. That's one of the
[01:15:49] places where we expect agents to go in
[01:15:50] the future.
[01:15:51] &gt;&gt; Yep. Yes. question in the back.
[01:16:02] &gt;&gt; So, I do not have Claude up in keep an
[01:16:05] eye on the cookbook. I do not have
[01:16:06] examples for Claude just yet. Um, I have
[01:16:10] Gemini almost done. Um, and yeah, we
[01:16:13] want to we want to add Claude to the the
[01:16:14] cookbook as well. We'll also happily
[01:16:17] take PRs. So if you want to take this
[01:16:18] example and map it over to to Claude,
[01:16:21] we'd love to have PRs on that as well.
[01:16:23] So yeah, this this is the cookbook is
[01:16:25] all open source. It's all in MIT
[01:16:28] licensed in our main repository, our
[01:16:30] main org.
[01:16:34] &gt;&gt; Any example agents on extracting
[01:16:36] information from Excel, PDF?
[01:16:39] &gt;&gt; Example agents of extracting from Excel
[01:16:41] or PDF? I don't have any personally.
[01:16:44] um you know we one of the other things
[01:16:46] that I'll mention is that we have a code
[01:16:48] exchange so we have um the cookbook is
[01:16:51] ours and that's where we're very we're
[01:16:53] very careful about making sure that it
[01:16:56] demonstrates best practices and we we do
[01:16:59] rigorous reviews on those because we
[01:17:01] don't want to mislead you at all. We
[01:17:03] also have a code exchange which we have
[01:17:05] literally I think 20 or 30 or 40
[01:17:08] examples in there. There might be
[01:17:10] something in there. I'm I'm honestly not
[01:17:12] sure. Um, yeah.
[01:17:14] &gt;&gt; Is it like a GitHub?
[01:17:15] &gt;&gt; Yes, it is. So, you'll find the code
[01:17:17] exchange on our website and all and I
[01:17:20] believe all of the entries in the code
[01:17:22] exchange have GitHub URLs. We don't own
[01:17:25] most of them um because they're from the
[01:17:27] community, but they're in other people's
[01:17:28] repositories. So, yeah, you would find
[01:17:31] that.
[01:17:36] &gt;&gt; All right. Well, this has been Oh, is
[01:17:39] there another question? No, I I just
[01:17:40] want to comment that uh we've mentioned
[01:17:42] a few times that's coming or that would
[01:17:44] be really really cool to do and um you
[01:17:47] know uh my team is hiring uh for folks
[01:17:51] &gt;&gt; the hiring plug
[01:17:52] &gt;&gt; on these AI applications of temporal.
[01:17:55] &gt;&gt; Okay. And since he said that I am a I'm
[01:17:57] in developer advocacy. We're looking for
[01:17:59] developer advocates too. So if you fit
[01:18:02] the engineer profile talk to Johan. If
[01:18:04] you fit the developer advocate profile
[01:18:06] come talk to me.
[01:18:08] So, okay. Well, thank you so much.
