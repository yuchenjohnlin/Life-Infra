---
source_url: https://www.youtube.com/watch?v=am_oeAoUhew
source_type: youtube
source_platform: youtube.com
title: "Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI"
author: AI Engineer
video_id: am_oeAoUhew
captured_at: 2026-04-22
duration_min: 46
status: raw
---

# Raw transcript

[00:00:00] Our
[00:00:15] next speaker is here to speak about
[00:00:17] harness engineering. How to build
[00:00:20] software when humans steer and agents
[00:00:23] execute. Please join me in welcoming to
[00:00:26] the stage member of technical staff at
[00:00:28] OpenAI, Ryan Leopo.
[00:00:40] Good morning, London.
[00:00:46] I'm super excited to be here today. I'm
[00:00:48] Ryan Laapo and for the last nine months
[00:00:51] I have had the privilege of building
[00:00:53] software exclusively with agents. Uh I
[00:00:57] am a token billionaire and I believe
[00:00:59] that in order for us to get into our AGI
[00:01:02] future, we want everybody to be token
[00:01:04] billionaires to use the models to do the
[00:01:07] full job. And what that means is to lean
[00:01:13] into the idea that the models are
[00:01:15] capable of being a full software
[00:01:16] engineer. And I've lived that experience
[00:01:18] by banning my team from even touching
[00:01:20] their editors, to have to work through
[00:01:22] the models in order to get the job done.
[00:01:25] And today I'm going to talk to you a
[00:01:27] little bit about what it means to lean
[00:01:28] into that and operationalize the way you
[00:01:31] work, the code spaces you live in, and
[00:01:33] the processes on your teams in order to
[00:01:35] get the agents to do the full job.
[00:01:40] I believe I'm preaching to the choir
[00:01:42] here when I say that the way we build
[00:01:44] software has changed. In the last six
[00:01:46] months, we have seen coding agents take
[00:01:48] over the world and capability has
[00:01:51] continually advanced at a super fast
[00:01:54] pace to have these models and the
[00:01:56] harnesses within which they live take
[00:01:58] more complex actions, do more
[00:02:01] complicated work with higher reliability
[00:02:04] over longer time horizons.
[00:02:06] And the place we've gotten to here is
[00:02:09] that implementation is no longer the
[00:02:11] scarce resource of what it means to do
[00:02:13] the job of software engineering. Code is
[00:02:15] free. We have an abundance of code to
[00:02:18] solve the problems that we come across
[00:02:20] in our day-to-day as we run our teams,
[00:02:23] build software, and solve user problems.
[00:02:27] Hiring the hands on the keyboards as
[00:02:30] part of our teams is only constrained by
[00:02:32] GPU capacity and token budgets. And each
[00:02:36] engineer today in this room has access
[00:02:38] to five, 50, or 5,000 engineers worth of
[00:02:42] capacity 247 every day of the year. The
[00:02:47] only thing that needs to happen, our
[00:02:49] roles is to figure out how to
[00:02:51] productively deploy these resources into
[00:02:53] our code and into our teams to make use
[00:02:56] of this new capacity.
[00:02:59] And in this world, skill sets are
[00:03:02] shifting more towards systems thinking,
[00:03:04] system design, and delegation in order
[00:03:06] to make use of this abundant capacity to
[00:03:09] produce code to solve problems. And
[00:03:12] there are three reasons that this
[00:03:13] happened. All of which happened in late
[00:03:16] 2025.
[00:03:19] For me, the magic moment was GPT 5.2,
[00:03:22] which when it came out was able to do
[00:03:24] the full job of a software engineer. The
[00:03:26] models at this point are good enough
[00:03:28] where they're isomeorphic to you and I
[00:03:31] in terms of the ability to produce code
[00:03:33] at high quality that solve real user
[00:03:36] problems in real code bases.
[00:03:39] Code is free. And I know this is maybe a
[00:03:43] scary thing to hear because code carries
[00:03:45] maintenance burden, but it's free to
[00:03:47] produce, free to refactor, and it is not
[00:03:51] a thing to get hung up on anymore.
[00:03:54] We think of code as burden because it
[00:03:57] it's a synchronous attention drain on
[00:03:59] the human engineers on our team. But the
[00:04:02] models are incredibly patient. They are
[00:04:04] infinitely parallel. So the ability to
[00:04:06] produce, maintain, refactor, and delete
[00:04:08] code is no longer a forcing function on
[00:04:12] figuring out how to allocate resources
[00:04:14] on your engineering teams. So sort of be
[00:04:17] agi pill here is to believe that the
[00:04:20] models are capable of producing every
[00:04:22] line of code we could ever possibly
[00:04:23] need, figuring out when to delete them,
[00:04:26] figuring out when to refactor them or
[00:04:28] make them more reliable. And it's your
[00:04:31] role as software engineers to figure out
[00:04:33] how to unblock your team of agents and
[00:04:36] humans driving those agents from being
[00:04:38] able to drive them over long horizon
[00:04:40] work to do the full job.
[00:04:44] The idea here is that every one of you
[00:04:46] is a staff engineer. You have as many
[00:04:49] team members as you can possibly drive
[00:04:51] concurrently and have tokens to support
[00:04:54] and you need to look one day, one week,
[00:04:58] six months into the future to figure out
[00:05:00] what structures you need to put in place
[00:05:02] to productively harness this infinite
[00:05:05] capacity to produce code.
[00:05:10] The scarce resources in this world that
[00:05:12] we see today are three things. human
[00:05:16] time, human and model attention and
[00:05:20] model context window. And in the world
[00:05:23] where human time and attention is
[00:05:25] scarce, the role is to think about where
[00:05:29] that time is going, figure out ways to
[00:05:31] productively automate it and move that
[00:05:35] synchronous human time into higher
[00:05:37] leverage activities.
[00:05:40] In a world where human time is scarce
[00:05:43] and human time is required to produce
[00:05:46] code, we have a stack rank. Things are
[00:05:48] either P zeros or P2s. Those P3s will
[00:05:52] never get done. However, in a world
[00:05:54] where code is free and infinitely
[00:05:56] abundant, all those P3s get kicked off
[00:05:59] immediately, maybe 4x in parallel. We
[00:06:02] pick one that solves the problem and in
[00:06:05] it goes.
[00:06:06] I've had the privilege of building a ton
[00:06:08] of agents internally at OpenAI to
[00:06:11] improve the productivity of my
[00:06:12] co-workers. And when code is free, all
[00:06:16] these internal tools can have good
[00:06:20] localization and internationalization
[00:06:21] from day one. I can make tools that my
[00:06:26] colleagues in London, Dublin, Paris,
[00:06:28] Brussels, Zurich, and Munich are able to
[00:06:30] experience in their native languages
[00:06:33] without really having to trade against
[00:06:36] any of my other teams capacity in order
[00:06:38] to make highquality tools.
[00:06:40] We should be working with the assumption
[00:06:42] that the best parts of software
[00:06:44] engineering that we all know, live, and
[00:06:47] breathe are available in any product
[00:06:49] that we could ever build all the time.
[00:06:52] Humans no need no longer need to concern
[00:06:54] themselves with implementation. The
[00:06:57] important thing is not the code but the
[00:06:58] prompt and the guardrails that got you
[00:07:00] there. This is why leaving breadcrumbs,
[00:07:03] documentation, ADRs, persona oriented
[00:07:07] documentation around what a good job
[00:07:08] looks like. All the historical logs of
[00:07:11] tickets and code reviews. This is the
[00:07:13] process that got you and your teams to
[00:07:15] the code and products that you have
[00:07:17] today. And this is what is need needs to
[00:07:19] happen in order to get your agents there
[00:07:21] as well. Your job is to build systems,
[00:07:25] software and structures that enable your
[00:07:28] team to be successful. And to do that,
[00:07:31] we need to make them legible to those
[00:07:34] agents that are driving the
[00:07:35] implementation. That means structuring
[00:07:37] them in a way that's native to the
[00:07:39] agents. Writing them in a way that is
[00:07:41] respecting of scarce context, which is
[00:07:43] this other scarce resource here, and
[00:07:46] figuring out ways to make the tokens
[00:07:48] that are required to do the job easy to
[00:07:50] predict. That means making things the
[00:07:52] same as much as possible so we can limit
[00:07:54] the amount of attention the model needs
[00:07:56] to activate in order to do the job.
[00:07:59] Large scale refactoring in this world is
[00:08:02] free. So making things the same is
[00:08:04] something that you are all able to do.
[00:08:07] There's never going to be a migration
[00:08:09] that hangs open for six months now that
[00:08:11] you can't get the last parts of the
[00:08:12] codebase to do because you can just fire
[00:08:14] off 15 agents to drive that work to
[00:08:16] completion. This is what it means to
[00:08:18] have a migration, right? We can finish
[00:08:20] them now. Come on. That's good. That's
[00:08:22] good. Clap.
[00:08:28] There's sort of this like meta
[00:08:29] epistemological question here about like
[00:08:31] what it means to do a good job and doing
[00:08:35] a good job as a software engineer is
[00:08:37] hard. It requires us years of being in
[00:08:40] the industry to fully internalize what
[00:08:42] it means to write highquality
[00:08:44] maintainable reliable code that our
[00:08:47] teammates are able to build on top of
[00:08:49] that is going to acrue leverage to the
[00:08:51] codebase
[00:08:52] to do a single patch. well, probably
[00:08:55] requires 500 little decisions along the
[00:08:58] way around the underspecified
[00:09:01] non-functional requirements that go into
[00:09:03] producing good code. The agents, the
[00:09:06] models during their training have seen
[00:09:09] trillions of lines of code that make
[00:09:11] every possible choice of those
[00:09:13] non-functional requirements that you
[00:09:14] could ever imagine. So, it's our job to
[00:09:17] specify those non-functional
[00:09:19] requirements to write them down in a way
[00:09:21] that the agents can see this is what it
[00:09:23] is to do a good acceptable job that's
[00:09:26] going to produce a merged patch. And if
[00:09:28] the agents aren't doing that, it's our
[00:09:31] job to figure out ways to refine and
[00:09:33] restrict their output such that the code
[00:09:36] they write is acceptable. You can just
[00:09:39] simply say do not produce slop. Don't
[00:09:41] accept slop. You won't get slop in your
[00:09:43] codebase. But to do that requires taking
[00:09:46] short-term velocity hits in order to
[00:09:48] back up or doubleclick into a task to
[00:09:50] figure out what it is the agents are
[00:09:52] struggling with in your environment.
[00:09:55] Put the guardrails in place so they stop
[00:09:57] making those mistakes
[00:10:00] and then figure out ways to step back
[00:10:02] and spend your time on higher leverage
[00:10:04] activities once you solve some of the
[00:10:06] blockers in the short term.
[00:10:09] When I think about empowering my team in
[00:10:11] this way, everyone is an expert in what
[00:10:14] it is they bring. I have a diverse full
[00:10:17] stack team that is experts in front-end
[00:10:19] architecture, backend scalability, being
[00:10:22] productminded. And each one of those
[00:10:25] different personas fleshes out the skill
[00:10:27] set of my team by bringing a different
[00:10:29] understanding, a different set of solves
[00:10:31] for those non-functional requirements.
[00:10:34] Getting teammates to write those down
[00:10:36] actually means that every engineer
[00:10:38] driving agents gets the best of every
[00:10:41] single person on my team. I don't need
[00:10:43] to block on low signal code review in
[00:10:46] order to learn what it means to write a
[00:10:48] good QA plan. To have one engineer on my
[00:10:52] team document that in a durable way
[00:10:54] means every agent trajectory is going to
[00:10:57] get a good QA plan. And we can do this
[00:10:59] once in a high lever way that we're able
[00:11:01] to stack on top of.
[00:11:05] So how can we get the agents to do a
[00:11:07] good job? What are some of the tools and
[00:11:09] techniques we have in order to
[00:11:12] essentially prompt inject our agents and
[00:11:13] continually remind them of what it means
[00:11:15] to make those specific choices that we
[00:11:18] expect around those non-functional
[00:11:20] requirements. And there's a bunch of
[00:11:22] ways we can do this. We can write good
[00:11:24] agents.mmd files. However, with autoco
[00:11:28] compaction, which is a thing that has
[00:11:29] continued to improve,
[00:11:31] GPT 5.4 and CEX is fantastic at autoco
[00:11:34] compaction. I essentially never have to
[00:11:36] write slashnew anymore. I've got some
[00:11:39] pictures on my Twitter of me strapping
[00:11:40] my laptop into the back of my car so I
[00:11:42] can continue do running inference while
[00:11:44] I'm commuting to and from work. And in
[00:11:47] this world, you have to kind of build
[00:11:50] for that expectation that context will
[00:11:53] get paged out over time. We need to be
[00:11:56] continually refreshing context as the
[00:11:58] agent goes about doing a task. And the
[00:12:00] ways we can do that are by having
[00:12:03] reviewer agents look at the code along
[00:12:05] the way through the lens of what it
[00:12:07] means to be successful. Right? We have
[00:12:10] security and reliability review agents
[00:12:12] in our codebase that are continually
[00:12:14] running as part of every push and CI
[00:12:16] that look at those documentations and
[00:12:18] the proposed patch and do simple things
[00:12:20] like say, are there timeouts and retries
[00:12:24] on this bit of network code? Has the
[00:12:26] code that has been introduced have a
[00:12:28] secure interface that is impossible to
[00:12:30] misuse?
[00:12:32] I'm sure everyone here has been paged at
[00:12:34] some point for network code that failed
[00:12:37] in production causing an outage that
[00:12:39] could have been remediated by a retry
[00:12:41] and a timeout. And I know I'm guilty of
[00:12:45] putting that retry and timeout in
[00:12:47] merging the bug fix and otherwise
[00:12:49] ignoring that. I am not a reliable
[00:12:51] reviewer or author of code with respect
[00:12:54] to this non-functional requirement.
[00:12:56] However, taking the time to write some
[00:12:59] docs, write a lint that is bespoke to my
[00:13:02] codebase that is going to look at every
[00:13:04] time I call fetch to make sure that
[00:13:06] there's a retry and a timeout wrapped
[00:13:08] around it means I've durably solved this
[00:13:10] problem and I'm able to do it because I
[00:13:12] lean on this axiom that code is free
[00:13:15] that the agents are able to do a good
[00:13:17] job that I can completely migrate the
[00:13:19] codebase to solve this problem durably
[00:13:21] once and for all. And in order to kind
[00:13:25] of operate in this way, we need to step
[00:13:28] back and look at the durable classes of
[00:13:31] failures that the agents and the humans
[00:13:33] in the codebase are making time after
[00:13:35] time. Figure out why we're spending time
[00:13:39] on it. Devise a solution to
[00:13:41] systematically eliminate this class of
[00:13:42] misbehavior and then continue to
[00:13:45] observe, refine, and make additional
[00:13:48] choices on those non-functional
[00:13:49] requirements.
[00:13:51] One really neat trick I use here is that
[00:13:55] you can write tests about the source
[00:13:56] code as well that are separate from
[00:13:59] lints. Right? If we know that context is
[00:14:01] limited, we can write a test that limits
[00:14:05] the fact that files are no longer than
[00:14:07] 350 lines. We're adapting our codebase
[00:14:10] to the harness to the models to do a
[00:14:13] little bit of engineering to be context
[00:14:15] efficient and squeeze more juice out of
[00:14:17] the model capability that we have today.
[00:14:22] The other things we can think about are
[00:14:25] providing good error messages that give
[00:14:27] actual remediation steps to the model
[00:14:30] and to humans for how to proceed next.
[00:14:33] It's not enough to say we've got a lint
[00:14:36] failure because we're awaiting in a loop
[00:14:39] or that we have an unknown at this deep
[00:14:41] part of the codebase and why is the
[00:14:43] model writing a function called is
[00:14:45] record. What we need to do is provide a
[00:14:47] prompt via a lint or a test failure that
[00:14:52] says no no no you shouldn't have an
[00:14:53] unknown here at all because we parse
[00:14:57] don't validate at the edge and you
[00:14:59] certainly have a type here which was
[00:15:00] derived from zot loadbearing
[00:15:02] infrastructure for our AI future
[00:15:10] you can just prompt things
[00:15:12] I've talked about here today is a prompt
[00:15:14] you can do this without touching the
[00:15:16] model weights at all.
[00:15:19] Kind of a funny digression here is it
[00:15:22] seems like each advancement we've had in
[00:15:24] the complexity of the way we write code
[00:15:27] to interact with these models comes from
[00:15:30] both increasing capability in the models
[00:15:32] and increasingly
[00:15:34] niche ways for injecting prompts into
[00:15:36] those models. prompts I'm sure you're
[00:15:39] aware are prompts powers prompts rules
[00:15:42] files prompts skills prompts these lint
[00:15:46] error messages that I am talking about
[00:15:48] prompts review agents that inject
[00:15:50] comments onto the PR that we require the
[00:15:52] agent to address before it is able to
[00:15:54] propose it for merge prompts
[00:15:57] you're going to find lots of ways to
[00:15:59] insert prompts into your code and one
[00:16:02] way you can do that is by embedding
[00:16:04] agent SDKs into your tests that are
[00:16:07] going
[00:16:08] review the codebase for acceptability
[00:16:10] using prompts that get embedded into the
[00:16:12] code. And if I find myself spending a
[00:16:15] ton of time writing prompts, we can
[00:16:17] actually shell out to the agent for that
[00:16:19] as well. Uh I've pointed codecs at all
[00:16:23] of the prompting cookbooks we have on
[00:16:25] the OpenAI developer guide and told to
[00:16:27] synthesize a skill out of them for how
[00:16:29] to write prompts. Which means when I
[00:16:31] find a need to write prompts in order to
[00:16:33] improve my agent performance locally in
[00:16:35] the code, I use the skill to write
[00:16:37] prompts that I wrote with the agent
[00:16:39] looking at the prompts to write the
[00:16:40] prompts.
[00:16:45] All the leverage that you're encoding in
[00:16:47] in to your repository, your team, and
[00:16:50] the agents in this way stacks incredibly
[00:16:53] well. to kind of pull back to this idea
[00:16:57] that a single product-minded engineer on
[00:16:59] my team was able to give us a big lift.
[00:17:03] They know what it means to write a good
[00:17:04] QA plan. To write a good QA plan though,
[00:17:07] you have to document all the features
[00:17:09] that you have, the critical user
[00:17:10] journeys, and how users engage with your
[00:17:13] applications, web apps, APIs, and
[00:17:16] services.
[00:17:17] Once you write those down on how to
[00:17:20] write a good QA plan with the
[00:17:22] expectation that all userfacing work has
[00:17:24] a QA plan, now a review agent is able to
[00:17:28] assert expectations around what it means
[00:17:30] to prove that you have effectively
[00:17:31] written the feature. A QA plan indicates
[00:17:34] what media should be attached to the PR
[00:17:37] for the humans and agents to know that
[00:17:39] you've done a good job, which has the
[00:17:41] consequence of me trusting the output
[00:17:43] more, needing to shoulders surf the
[00:17:45] agent less.
[00:17:47] and removing myself from the loop even
[00:17:49] more to delegate more and more of the
[00:17:52] work to agents. And all of this is just
[00:17:55] making sure the agents have the tools
[00:17:58] and tokens and context
[00:18:01] to do the full job to remove myself from
[00:18:04] the need as a synchronous driver. The
[00:18:07] models crave tokens. We can
[00:18:09] operationalize our codebase to give them
[00:18:12] tokens to drive them forward using sub
[00:18:14] agents and all these other techniques to
[00:18:16] refine the agent output.
[00:18:20] I'm excited to let you all know today in
[00:18:22] the way you all do that you can just go
[00:18:24] build things. Do not hesitate to remove
[00:18:28] yourselves from the loop by getting the
[00:18:29] agents to do the full job because they
[00:18:31] can. Thank you.
[00:18:34] &gt;&gt; Very excited to bring on our guest.
[00:18:38] We've got Ryan Leapo today. He just gave
[00:18:40] the keynote. Um, very exciting speaker.
[00:18:42] The man is full send hyperengineering at
[00:18:45] OpenAI. So, uh, a little bit of
[00:18:48] background. We did a Laten Space episode
[00:18:50] with him. We shipped it the other day.
[00:18:52] The the story he wrote this great
[00:18:54] article called Harness Engineering and
[00:18:56] we're like, "Wow, this is pure gold." We
[00:18:58] have him on the podcast. He's a token
[00:19:00] billionaire spending over a billion
[00:19:02] output tokens a day. That's like over
[00:19:04] $1,000. So, you know, man is really
[00:19:06] living it. Uh, we want to keep this
[00:19:08] exciting. Ask good questions, ask
[00:19:10] interesting stuff, ask things that
[00:19:12] people can learn from. But, you know,
[00:19:13] let's welcome Ryan onto the stage.
[00:19:20] &gt;&gt; Hi folks, how's it going? Excited to be
[00:19:21] here. Uh, London has been fantastic and
[00:19:24] uh, excited to kind of walk through what
[00:19:27] it is, uh, that we do and how we work
[00:19:28] here.
[00:19:29] &gt;&gt; I think you got to come on. This camera
[00:19:31] is just here. So,
[00:19:32] &gt;&gt; I got blinded by the QR code. So, we're
[00:19:35] &gt;&gt; Okay. So, background. We have about an
[00:19:37] hour. Um, scan this QR code. You should
[00:19:40] get Slido. Slido will let you ask
[00:19:43] questions. If you see interesting stuff,
[00:19:45] you can thumbs them up and we'll try to
[00:19:47] get through them. Unfortunately, the
[00:19:49] first one I can't superdo, but let's
[00:19:51] just kick it off. Ryan, can you show us
[00:19:53] your actual working setup with no
[00:19:55] laptop? Um,
[00:19:56] &gt;&gt; uh, yeah. Uh, here. Beach
[00:19:59] Margarita
[00:20:01] linear, right?
[00:20:02] &gt;&gt; Oh, wow.
[00:20:04] Um, I'll say watch the podcast we put
[00:20:07] out. We go through some of the work, but
[00:20:09] if you want to talk about it, I guess
[00:20:10] without actually showing us what's your
[00:20:12] what's your workflow like? What's your
[00:20:13] setup? How do you how do you approach a
[00:20:15] task?
[00:20:16] &gt;&gt; Sure. So, uh, the way me and my team
[00:20:21] work is to start with tickets, right? We
[00:20:24] have chunks of work that we want to do,
[00:20:26] features we want to add to our apps,
[00:20:28] reliability work that we want to do. uh
[00:20:30] we give that ticket to an agent along
[00:20:32] with a couple of skills that enable it
[00:20:34] to manipulate our app. Uh we want the
[00:20:38] entry point to the development process
[00:20:40] to be codecs not an environment which we
[00:20:43] build around it. So we kind of do things
[00:20:46] um outside in right like codeex is the
[00:20:49] entry point the same way you would be
[00:20:50] and we give it tools we give it
[00:20:52] instructions on how to cook. So rather
[00:20:54] than like creating a shell that our app
[00:20:56] and CEX get spawned into, we have a
[00:20:59] skill that teaches Codex how to launch
[00:21:00] the app that teaches Codeex how to spin
[00:21:02] up that local observability stack to
[00:21:04] give it logging and telemetry. We give
[00:21:06] it a skill that enables it to uh boot up
[00:21:10] Chrome DevTools and attach to the
[00:21:13] application with a you know local CLI
[00:21:16] that will connect via some Damon that we
[00:21:18] have. So the whole way we have set up
[00:21:21] the repository and all of the local dev
[00:21:23] tools is for codeex to invoke them
[00:21:25] first. Um that means we have kind of
[00:21:28] like a bunch of little mini harnesses
[00:21:30] within the codebase that make it really
[00:21:31] easy for us to slot in additional guard
[00:21:33] rails. Uh you know a big package of
[00:21:37] custom ESLint rules which get wired into
[00:21:39] every PNPM package in the workspace. We
[00:21:42] have another sort of local dev harness
[00:21:44] that allows us to add sort of like
[00:21:46] higher level wholesome tests that assert
[00:21:49] the structure of the code itself rather
[00:21:51] than like either the syntax or the
[00:21:53] behavior of the code. Things like you
[00:21:56] know package privacy dependency edges
[00:22:00] between different layers of our stack.
[00:22:01] these sorts of things. Uh making sure
[00:22:03] that you know across multiple files zod
[00:22:07] schemas are dduplicated that there's a
[00:22:08] single canonical implementation of like
[00:22:10] our async helpers. Uh these sorts of
[00:22:13] things because you know the way we have
[00:22:15] seen the agents work is to sometimes
[00:22:18] optimize for local coherence of a
[00:22:20] package rather than using like our
[00:22:22] shared utilities and things like that.
[00:22:24] So having observed that behavior, we
[00:22:26] kind of have built a bunch of little
[00:22:28] pseudo llinter source code verification
[00:22:31] things that shake out some of that bad
[00:22:34] behavior so the humans don't get
[00:22:35] distracted paying attention to that in
[00:22:37] reviews, stuff like that. But uh the
[00:22:40] setup optimizes for the agent to do the
[00:22:44] job and for the humans to not have to
[00:22:45] keep track of the high churn in the
[00:22:47] codebase. Um we kind of centralize our
[00:22:50] leverage around five to 10 skills. uh we
[00:22:53] don't go super wide on skills preferring
[00:22:55] to make the existing skills better
[00:22:58] because at least I find that the
[00:23:02] infrastructure within the repository all
[00:23:03] the local developer tools change super
[00:23:06] frequently uh and I don't really have
[00:23:08] the bandwidth to keep track of this. So
[00:23:10] we hide all that complexity beneath the
[00:23:13] skills that the human has to invoke and
[00:23:16] let the agent just kind of figure it
[00:23:17] out. One one kind of neat thing here is
[00:23:20] um when we moved from using uh Chrome
[00:23:23] DevTools protocol directly to having
[00:23:24] this like Damon thing like I didn't know
[00:23:26] that had happened for like three weeks.
[00:23:28] Uh it was like totally fine because
[00:23:30] Codex was able to do the thing uh you
[00:23:32] know with the documentation and things
[00:23:34] that we had in place
[00:23:35] &gt;&gt; and part of this you can get more detail
[00:23:37] in your article. So some background you
[00:23:39] wrote a great piece called harness
[00:23:40] engineering. There's a whole section in
[00:23:42] there on how you thought about skills,
[00:23:44] thousands of skills versus simplifying
[00:23:46] it to just quite a few. But okay, uh,
[00:23:49] continuing on, how do you stop yourself
[00:23:52] from overgineering harnesses? And a
[00:23:55] little bit of a similar followup is, do
[00:23:58] you often build small tools for
[00:24:00] yourself, if ever? Uh, do you do you
[00:24:02] build custom tools?
[00:24:04] &gt;&gt; Yeah. So, I think this is kind of
[00:24:06] gesturing in the direction of the bitter
[00:24:07] lesson here, right? which is how do I
[00:24:09] make sure the work that I do isn't like
[00:24:12] completely obsoleted by an increase in
[00:24:14] model capability and the way I have
[00:24:17] thought about that is doing sort of the
[00:24:19] bare minimum amount of context
[00:24:21] management to kind of pull in
[00:24:23] requirements uh for the agent to do an
[00:24:26] acceptable job over the course of its
[00:24:28] work and context is a thing that I don't
[00:24:31] think will ever be obsoleted right like
[00:24:33] the the models must be told like the
[00:24:35] requirements of the task which
[00:24:37] guardrails to pay attention patention to
[00:24:38] these sorts of things. So a good harness
[00:24:41] is really operationalized around giving
[00:24:44] the model text at the right time so it
[00:24:46] can look at the work it has done and the
[00:24:49] information around what a good job looks
[00:24:50] like and you know fundamentally the
[00:24:54] models are trained to follow
[00:24:55] instructions. All the harness should do
[00:24:57] is surface instructions to the model at
[00:24:59] the right time. So we do want to
[00:25:02] minimize that too, right? You don't want
[00:25:04] to frontload all those instructions
[00:25:05] because then you kind of like overwhelm
[00:25:07] the agent, but all of these sort of
[00:25:10] requirements around what a good job do
[00:25:12] need to be paid attention to over the
[00:25:13] entire course of a PR, right? So
[00:25:16] figuring out ways to either defer or
[00:25:18] just in time surface those instructions
[00:25:20] is kind of what uh a good harness should
[00:25:23] do, right?
[00:25:24] If you know that uh you want your React
[00:25:29] components, right, to be decomposed so
[00:25:31] that they make good snapshot tests for
[00:25:33] individual more stateless pieces, right?
[00:25:35] You don't need to load that up front.
[00:25:37] Instead, you should kind of let the
[00:25:38] agent cook and prototype and experiment
[00:25:40] with the UI you want to build and then
[00:25:42] at lint or test time say, "Okay, you've
[00:25:45] done the work. In order to finish it,
[00:25:47] you have to break this apart so that
[00:25:48] your components are small and as
[00:25:50] stateless as possible and have local
[00:25:52] dependencies on hooks instead of prop
[00:25:53] drilling or whatever it is that you want
[00:25:55] uh the code to look like. And then the
[00:25:57] agent will say, "Oh, this is a new
[00:25:59] instruction for me. Let me take the
[00:26:01] patch as written, modify it to make sure
[00:26:03] that it aderes to the instructions." And
[00:26:05] then up it goes to GitHub. And this sort
[00:26:07] of thing is not going to be obsoleted by
[00:26:10] increases in model capability. It's
[00:26:12] really just about getting that right
[00:26:14] text, that right context to the agent at
[00:26:16] the right time.
[00:26:17] &gt;&gt; Can we talk about an example of a good
[00:26:20] harness? So, a lot of people are asking
[00:26:22] about the codeex model, the codeex
[00:26:24] harness. How does that compare to other
[00:26:26] harnesses? So, cloud code, open code.
[00:26:28] Uh, how do you guys take these decisions
[00:26:30] into play? You don't work directly on
[00:26:32] codec, but if there's you can if there's
[00:26:34] stuff you can speak about about the
[00:26:36] codeex harness, what you guys see as you
[00:26:38] architect it out.
[00:26:40] &gt;&gt; Yeah. So one thing that I think is super
[00:26:43] powerful is this notion that the labs
[00:26:46] are not just post-training the models
[00:26:48] but post-training the models in the
[00:26:49] context of the harness in which they are
[00:26:51] primarily deployed in right like the
[00:26:54] apply patch tool or like the specific
[00:26:56] quoting semantics of how to invoke the
[00:26:58] bash tool are like in the loop for the
[00:27:01] post- training process for the harnesses
[00:27:03] from the labs which means like there is
[00:27:06] leverage to be had by depending on these
[00:27:08] sort of like firstparty harnesses
[00:27:09] directly At least this is what I
[00:27:11] believe. Uh, and as such, kind of being
[00:27:15] able to direct through them via things
[00:27:18] like the SDK or manipulating the Codex
[00:27:20] app server directly means you kind of
[00:27:22] get to ride the wave of all that
[00:27:24] leverage in post- training. Instead,
[00:27:26] focus on the parts that you care about,
[00:27:28] which is like what correct code looks
[00:27:30] like. Um, I kind of have high confidence
[00:27:34] that things like clog code and codecs
[00:27:36] will continue to get better. uh that is
[00:27:38] the responsibility of like the teams
[00:27:40] working on these coding agents. So in my
[00:27:43] role where I don't really want to focus
[00:27:45] on the coding harness at all is figuring
[00:27:48] out ways to plug into them in ways that
[00:27:51] um kind of like steer the agent. That
[00:27:55] means my job can sort of like move up to
[00:27:58] thinking about differences in model
[00:27:59] behavior between releases rather than
[00:28:02] deeply understanding the nuts and bolts
[00:28:03] of the harness. Instead, I can think
[00:28:05] about what it means to, you know, drive
[00:28:08] the behavior that I want vers based on
[00:28:10] the observed behavior rather than like
[00:28:12] the inner mechanics of the thing. It's a
[00:28:15] perfect follow-up to the next question,
[00:28:16] which is, uh, do you have any
[00:28:18] recommendations for collaboration
[00:28:20] platform? So, when you're in the
[00:28:21] software development life cycle, is
[00:28:23] there any platform that you use for
[00:28:25] agents, engineers, developers all to
[00:28:28] collaborate on working on anything? Any
[00:28:30] tips, any tools?
[00:28:32] Yeah. So
[00:28:35] in this world it has largely been just
[00:28:39] markdown files in the repository and
[00:28:41] GitHub that have been the primary sort
[00:28:43] of hub and spoke sort of thing. If you
[00:28:46] think about collaborating on a document
[00:28:49] like you open Google Docs, you write
[00:28:51] something, you ask for feedback, people
[00:28:53] comment, you apply suggestions, these
[00:28:54] sorts of things. This is kind of like a
[00:28:56] little clean room environment just for
[00:28:59] this work artifact that you're
[00:29:00] producing. like a PR kind of has a
[00:29:02] similar purpose. So we kind of treat
[00:29:05] that as a big hub and spoke broadcast
[00:29:07] domain where all of the agents and
[00:29:09] humans collaborate together. Uh and
[00:29:13] because we optimize for throughput, we
[00:29:15] don't block on any sort of like
[00:29:17] contribution to that like folks can
[00:29:18] either review or not. Agents can either
[00:29:20] review or not. The implementation agent
[00:29:23] can acknowledge, defer or reject any
[00:29:26] feedback that it gets. uh really
[00:29:28] allowing each participant in the
[00:29:30] production of diffs to kind of make
[00:29:32] their own judgments around what it means
[00:29:34] to deliver, receive, respond to
[00:29:36] feedback. Uh and this has a nice
[00:29:39] property of like not putting the model
[00:29:41] in a box in a bunch of places. We want
[00:29:44] them to use their good reasoning sort of
[00:29:46] thing. So being super prescriptive
[00:29:48] around like every bit of feedback must
[00:29:50] be addressed can kind of have this like
[00:29:52] catastrophic failure mode of your coding
[00:29:55] agent being bullied by all of the
[00:29:57] reviewers when really we want to bias
[00:29:59] toward code being accepted, not perfect,
[00:30:02] not drowning in minutia and these sorts
[00:30:04] of things.
[00:30:06] &gt;&gt; How should people get started with using
[00:30:08] coding agents? People that have been
[00:30:10] using a lot of doing a lot of manually
[00:30:12] written code, how how do they start to
[00:30:15] transition? What should they offload?
[00:30:17] How do they kind of come over that
[00:30:19] barrier of okay, I'm still checking
[00:30:20] every PR I'm copy pasting from codecs.
[00:30:24] How should like the average engineer
[00:30:26] start to use these tools?
[00:30:28] &gt;&gt; I think there's two ways to approach
[00:30:30] this problem. One is to
[00:30:33] start using the coding agents to improve
[00:30:35] your confidence in the code itself as it
[00:30:38] is written today. Right? I think we
[00:30:40] would all agree that like more tests is
[00:30:42] probably a good thing, right? to assert
[00:30:44] that our programs are well specified and
[00:30:47] behave correctly as our users interact
[00:30:49] with them is a good thing. Uh and the
[00:30:51] agents are super good at looking at the
[00:30:54] existing code with some context around
[00:30:56] how it is meant to be used and writing
[00:30:58] tests that assert that behavior. So kind
[00:31:01] of using this to improve your confidence
[00:31:03] in the quality of the code will also
[00:31:06] increase the agents ability to
[00:31:08] successfully navigate it which means you
[00:31:10] don't have to worry as much around doing
[00:31:13] super detailed review of the agent
[00:31:15] output. The other way to think about
[00:31:17] this is to look at how you are spending
[00:31:20] your time. Is it you know staring at
[00:31:23] your editor writing code? Is it waiting
[00:31:25] for tests to run? Is it waiting for
[00:31:27] human review feedback? is CI slow and
[00:31:31] you're like waiting on that maybe you
[00:31:32] have a ton of flaky tests and using the
[00:31:34] agents to incrementally automate the
[00:31:38] parts where you are spending your time
[00:31:40] because ultimately the high lever parts
[00:31:42] of our jobs is to define the work that
[00:31:45] must be done prioritize and schedule
[00:31:47] that work and then effectively empower
[00:31:49] folks on our team to do that work. uh
[00:31:52] and the more and more we can delegate
[00:31:55] and move into sort of this like
[00:31:56] sequencing and orchestration role even
[00:31:59] if if you just think about like managing
[00:32:01] your teams right the more parallel and
[00:32:03] the more like deeper individual
[00:32:06] executions of those delegations we're
[00:32:07] able to do right if I put primitives in
[00:32:11] place that make it super easy to like
[00:32:13] spin up ways to respond to events on my
[00:32:15] Kafka queue right like I don't really
[00:32:17] need to be in the weeds with every
[00:32:18] engineer making sure they like implement
[00:32:20] a consumer correctly Right. And these
[00:32:23] same sort of like building block style
[00:32:25] techniques apply really well to the
[00:32:27] agents and stack really well too.
[00:32:29] &gt;&gt; A fun one. How do you work with agents
[00:32:31] in your car?
[00:32:34] &gt;&gt; Um so I have not used the new uh voice
[00:32:37] mode that launched in CarPlay uh
[00:32:40] recently. Uh not ready for that. But uh
[00:32:43] usually what I'll do is kick off uh a
[00:32:46] task uh right before I leave the office.
[00:32:49] uh tether my laptop to my phone, buckle
[00:32:52] it into the back seat, and kind of let
[00:32:53] it cook in the 30 minutes it takes me to
[00:32:55] get home. Uh most of the time with the
[00:32:57] skills we invoke that tell the agent,
[00:32:59] you know, you're operating on a task,
[00:33:00] you go until the tests are green. Uh you
[00:33:02] know, I don't have to reach back there
[00:33:04] and poke yes, continue onto the thing.
[00:33:06] Uh and I'm basically able to more fully
[00:33:10] saturate, you know, my day with token
[00:33:13] consumption. Um, the dream here is that
[00:33:16] I actually have 50 agents running 247
[00:33:19] and I don't have to interact with them
[00:33:20] at all. Uh, and the way to do that is to
[00:33:23] define the work well, figure out ways
[00:33:25] for it to automatically be scheduled and
[00:33:27] remove myself from having to click the
[00:33:29] button. Right? Every time I have to type
[00:33:31] continue to the agent is like a failure
[00:33:33] of the harness to provide enough context
[00:33:35] around what it means to continue to
[00:33:37] completion.
[00:33:39] &gt;&gt; Wow, good statement at the end. every
[00:33:41] time you have to interact with the agent
[00:33:43] is a failure. Okay, so the following
[00:33:46] question kind of scales this out, right?
[00:33:47] As your org knowledge map scales, what
[00:33:50] practical steps do you have to like
[00:33:53] enable progressive disclosure? So as you
[00:33:55] have a larger and larger codebase, as
[00:33:57] you have more people, how do you scale
[00:33:59] your agents to work better with this?
[00:34:01] &gt;&gt; Yeah. So
[00:34:03] when I sort of initially started this
[00:34:05] project that I was working on, blank
[00:34:07] repository, create Electron app, right?
[00:34:10] you know, V single package, all this
[00:34:12] sort of stuff. And eventually ended up
[00:34:14] with a mess, right? Because there's no
[00:34:18] package privacy that allows me to
[00:34:19] enforce invariance around what APIs are
[00:34:21] public versus which ones are not. The
[00:34:23] agent didn't have like concrete hooks in
[00:34:26] the file system to determine which
[00:34:29] domains were separate from the other
[00:34:30] ones. So we ended up going like full
[00:34:33] 10,000 engineer organization heavy on
[00:34:35] the architecture
[00:34:37] 750 packages in the PNPM workspace
[00:34:40] isolated by business logic domain or
[00:34:43] layer of the stack individual small util
[00:34:46] packages that encapsulate reusable
[00:34:49] functionality that we lint on being used
[00:34:51] that we can encode leverage in and I do
[00:34:54] think that like in this world even if
[00:34:57] you don't actually have microservices
[00:34:59] structuring your repositories in ways
[00:35:01] that you can actually scope like the
[00:35:03] directory subree you are looking in to
[00:35:06] be able to do most of the change helps
[00:35:09] uh and you know code in the file system
[00:35:13] is also text which means it's
[00:35:15] effectively prompts that you're giving
[00:35:16] to your coding agent. Uh, so making the
[00:35:19] code as much the same as possible kind
[00:35:23] of makes it so that regardless of where
[00:35:25] in the repository your agent is looking,
[00:35:27] it develops a ton of transferable
[00:35:29] context, right? Like you should have one
[00:35:32] way to like do a bounded concurrency
[00:35:35] helper. You should have one way to
[00:35:37] construct a observable and instrumented
[00:35:41] side effectful command. You should have
[00:35:43] one OM, right? Like you should have one
[00:35:45] programming language. You should have
[00:35:46] one way of writing CI scripts. you
[00:35:47] should have one way of adding additional
[00:35:49] lint rules, these sorts of things
[00:35:50] because it means that like the tokens
[00:35:53] that you want the model to produce are
[00:35:54] easier to predict and more consistently
[00:35:56] predicted regardless of where it looks.
[00:35:58] Um, so I would say figure out ways to
[00:36:01] structure the code so it is local to a
[00:36:03] subree in the repository for most of the
[00:36:06] ways you would interact with that system
[00:36:08] and then figure out a way to use these
[00:36:09] agents to completely migrate the
[00:36:11] codebase to be the same. you know,
[00:36:13] empower someone on your team to be a
[00:36:15] dictator to say this is the way it must
[00:36:17] be done, right? Or, you know, figure
[00:36:18] that out together
[00:36:20] and, you know, write it down, evolve the
[00:36:23] code so that it reflects that reality,
[00:36:25] these sorts of things.
[00:36:26] &gt;&gt; We've got a few questions on code
[00:36:28] review. How do you approach code review
[00:36:30] now that you have such high velocity?
[00:36:32] Uh, do you just not read the code? Do
[00:36:34] you just trust trust the test coverage?
[00:36:36] Uh, how do you write good tests? How do
[00:36:38] you offload that stigma of like, you
[00:36:41] know, you have a mental blocker. I need
[00:36:42] to manually check everything before I
[00:36:44] merge pure.
[00:36:46] &gt;&gt; So that same sort of idea where you have
[00:36:49] to look at where you're spending your
[00:36:50] time and figure out ways to spend less
[00:36:53] of it. Uh, you know, when we started,
[00:36:57] right, the first thing to do was figure
[00:36:59] out how to get the agent reliably
[00:37:00] producing code that we would accept. And
[00:37:03] a big challenge we ran into is with each
[00:37:05] engineer producing three to five PRs per
[00:37:08] day, even on a team of three, merge
[00:37:10] conflicts were super miserable, right?
[00:37:13] Because these PRs tended to be pretty
[00:37:14] big. We were working on the same parts
[00:37:17] of the codebase. So that's where we
[00:37:19] moved in two directions. One was to like
[00:37:22] tree out the code a bit more to minimize
[00:37:24] these merge conflicts, but also minimize
[00:37:26] the amount of time PRs were open so that
[00:37:28] we were uh reducing the likelihood of a
[00:37:31] merge conflict actually occurring. And
[00:37:33] the reason PRs were staying open so long
[00:37:36] was because we needed code review uh
[00:37:38] because humans were being the blocker in
[00:37:42] this scenario. So in order to do
[00:37:47] that piece automatically, I essentially
[00:37:49] asked every engineer on the team to take
[00:37:52] one day a week, Fridays, we called it
[00:37:54] garbage collection day, where our entire
[00:37:57] job was to take every bit of slop we had
[00:38:01] observed over the course of the week
[00:38:02] that was making a PR difficult to merge
[00:38:05] and figure out ways to categorically
[00:38:07] eliminate it from ever happening in the
[00:38:09] first place, which is where we kind of
[00:38:11] started closing this loop between the
[00:38:14] feedback that humans were giving on the
[00:38:15] PR indicates some context failure on
[00:38:17] behalf of the agent, getting that into
[00:38:20] the repository and then figuring out
[00:38:22] ways to automatically prompt inject the
[00:38:23] agent so that it would selfheal when it
[00:38:25] produced this bad behavior. And this is
[00:38:27] kind of how you go from synchronous
[00:38:29] human time spent giving feedback as code
[00:38:31] review comments to documentation in the
[00:38:34] repository to automatically surfing this
[00:38:36] documentation either via a failing test
[00:38:39] or a reviewer agent who is primed to
[00:38:41] review the code as written in the
[00:38:43] context of these docs. But all of that
[00:38:46] happens by putting those docs in a
[00:38:47] single place that all these processes
[00:38:49] are able to attach to. Um, you know, we
[00:38:54] kind of asked folks to basically bucket
[00:38:56] the types of review feedback they were
[00:38:58] giving into like um like the persona
[00:39:00] they were operating as like front-end
[00:39:02] architect, you know, reliability
[00:39:04] engineer, scalability sort of thing. And
[00:39:06] then basically for each of those
[00:39:08] personas, we spun up a review agent that
[00:39:10] gets triggered on every push that says,
[00:39:12] is this code good? Surface any P2s or
[00:39:14] above that would block this PR from
[00:39:16] merging based on these documentation
[00:39:18] that says what good looks like. Uh and
[00:39:21] with that and just continuously
[00:39:23] appending to these files, we started to
[00:39:25] see slop reduce reduce reduce.
[00:39:28] &gt;&gt; People have questions about your billion
[00:39:30] tokens. Where do you think those are
[00:39:32] split up? So how much of it is on code
[00:39:34] review? Where where is the majority of
[00:39:37] that usage coming from? And a followup
[00:39:39] for people that are just getting
[00:39:41] started. Say they have they've jumped
[00:39:43] and done a $200 pro plan, right? If you
[00:39:46] had to cut your usage by a fifth, how
[00:39:48] should people maximize their usage?
[00:39:51] Right? You run into usage limits. Um,
[00:39:53] you know, you don't want to just copy
[00:39:54] paste million lines of code every six
[00:39:57] hours. No prompt hit prompt cache hit.
[00:39:59] But how should we how should we think
[00:40:01] about that?
[00:40:02] &gt;&gt; Yeah. So I would say probably
[00:40:07] a it's probably a third a third a third
[00:40:10] between like planning ticket curation
[00:40:15] documentation implementation and stuff
[00:40:17] that runs in CI.
[00:40:18] &gt;&gt; Do you use plan mode?
[00:40:20] &gt;&gt; Uh we uh I've used exec plans which was
[00:40:23] kind of like an early version of this
[00:40:25] that we published which is sort of like
[00:40:26] a proto skill that says this is how you
[00:40:28] should structure a plan with milestones
[00:40:30] and acceptance criteria. um haven't
[00:40:33] really used plan mode as part of the
[00:40:35] harness at all. My my sort of
[00:40:36] expectation here is that I should be
[00:40:38] able to drop a ticket in and have it do
[00:40:40] the job anyway without diverting through
[00:40:42] a plan. Uh because most of the time I'm
[00:40:44] never going to read it anyway. Uh so I
[00:40:47] find that if you do use a plan and you
[00:40:49] approve it without reading it at all,
[00:40:51] you're actually encoding a bunch of
[00:40:52] instructions that you don't necessarily
[00:40:54] want followed. Uh so if you are going to
[00:40:57] use plans, my recommendation is to push
[00:40:59] those up as single PRs with just the
[00:41:01] plan where you actually have human
[00:41:04] review every line of it and like block
[00:41:06] on human approval before they get merged
[00:41:08] and then kicked off. Uh because it's
[00:41:11] you're effectively potentially wasting
[00:41:13] your time on a rollout with instructions
[00:41:16] that like are bad. Uh so you want to
[00:41:18] kind of like minimize the time that
[00:41:19] happens. But I do think that uh kind of
[00:41:23] getting tokens to be spent in CI is a
[00:41:26] necessary part here because writing code
[00:41:29] no longer is the hard part. Like getting
[00:41:31] code accepted and advancing the code and
[00:41:34] product forward is like what it takes to
[00:41:36] make that written code be valuable. And
[00:41:39] you know you kind of have all heard the
[00:41:41] apherism that like you know senior
[00:41:42] engineers give good code reviews like we
[00:41:44] expect our senior engineers as agents to
[00:41:46] do the same.
[00:41:49] Uh someone asked is code a disposable
[00:41:51] build artifact?
[00:41:53] &gt;&gt; Yes.
[00:41:55] &gt;&gt; Uh I think we we touch on this with uh
[00:41:57] symfony which is sort of this agent
[00:41:59] orchestrator that we release. This idea
[00:42:01] that you know we can publish a library
[00:42:05] that's actually a super well-defined
[00:42:07] spec that the code is a compiled
[00:42:10] artifact of. And I think like using LLM
[00:42:14] as fuzzy compiler is like an interesting
[00:42:17] mental model to have, right? Like all of
[00:42:20] the context that we're putting in the
[00:42:21] codebase for harness engineering is
[00:42:24] effectively like constraints and
[00:42:26] optimization passes on which code is
[00:42:29] acceptable to build in the first place.
[00:42:31] Uh and this is pretty similar to like
[00:42:33] the static analysis and optimization
[00:42:36] passes that something like LLVM would do
[00:42:38] in the process of compiling Rust code.
[00:42:41] uh and sort of
[00:42:43] swapping out one model for another is
[00:42:46] sort of like changing your code
[00:42:47] generation backend from you know LLVM to
[00:42:50] crane lift in the Rust compiler and you
[00:42:53] would expect that all of the sort of
[00:42:55] rules around what acceptable Rust code
[00:42:57] looks like produce valid sound machine
[00:43:01] code out the back even if the generation
[00:43:04] process is different and you end up with
[00:43:05] different x86 instructions. So same sort
[00:43:08] of mindset for LLMs swapping out
[00:43:10] different models sort of thing. We want
[00:43:12] the structure around the code to
[00:43:14] basically limit
[00:43:17] how it is written to things that would
[00:43:19] be acceptable to us.
[00:43:21] &gt;&gt; At a high level, can you give us a
[00:43:24] picture of what future you're building
[00:43:25] for? Does context still matter? How do
[00:43:28] people do engineering, harness
[00:43:30] engineering, context engineering? What
[00:43:32] does the future look like?
[00:43:35] sort of the the feature that I want to
[00:43:37] build toward here is where
[00:43:40] I'm able to take a token budget and a
[00:43:45] quarter, a half or a year's worth of
[00:43:48] work,
[00:43:50] take the human input to rank what is
[00:43:52] most important success metrics,
[00:43:55] reliability metrics, give it to the
[00:43:57] machines and have them continually work
[00:43:59] and advance my product forward. uh
[00:44:02] without sort of you know my hands
[00:44:04] explicitly on the wheels at all. We
[00:44:08] as we have gone through like very early
[00:44:10] prototyping to internal alpha internal
[00:44:14] beta external alpha I kind of have felt
[00:44:17] that like new parts of the software
[00:44:19] engineering process have kind of like
[00:44:21] started from zero and we've had to build
[00:44:22] up capability kind of like these like
[00:44:25] you know pentagonal like personality
[00:44:28] charts right where like I spike in this
[00:44:30] direction maybe I'm weak over here and
[00:44:32] you know when we get to deployed
[00:44:35] software for the first time, right? The
[00:44:37] agents ability to do like QA smoke
[00:44:39] testing on our built artifacts before
[00:44:42] they're promoted to distribution was
[00:44:43] weak. We hadn't invested any time in
[00:44:45] this. There were no docs. There were no
[00:44:46] tools that the agents could use to like
[00:44:48] download the built artifact, launch it,
[00:44:51] poke around to make sure that our like
[00:44:53] most critical user journeys were well
[00:44:55] validated and tested. So, because I
[00:44:58] don't want to be touching the computer,
[00:45:00] we needed to figure out like ways for
[00:45:02] the agents to build themselves tools to
[00:45:04] do that part. Uh, and
[00:45:07] there's a whole universe of software
[00:45:09] engineering outside of writing code,
[00:45:11] right? Like I am triaging user feedback.
[00:45:13] I'm triaging pages. I am making sure
[00:45:16] that we don't have any PII leaking in
[00:45:19] the logs in production. I'm making sure
[00:45:21] that like the Twitter vibes are good and
[00:45:23] people are enjoying my software that uh
[00:45:26] our user operations staff are supported
[00:45:29] with well written runbooks that allow
[00:45:31] them to triage and mitigate high volume
[00:45:34] user issues and then moving that into
[00:45:36] the code itself so they don't happen in
[00:45:37] the first place and as I no longer have
[00:45:41] to produce code like my mind can shift
[00:45:43] to these other higher level or more
[00:45:46] squishy activities but the agents are
[00:45:48] good enough to do these things too and
[00:45:49] figuring out how like write down the
[00:45:51] processes and the acceptance criteria
[00:45:53] becomes like the sort of like meta
[00:45:54] programming part of the job using these
[00:45:56] agents.
[00:45:57] &gt;&gt; That's a great way to end it. What an
[00:45:59] exciting future. Give it up for Ryan
[00:46:01] guys.
[00:46:01] &gt;&gt; Thank you folks.
