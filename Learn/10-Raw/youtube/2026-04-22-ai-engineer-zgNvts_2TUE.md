---
source_url: https://www.youtube.com/watch?v=zgNvts_2TUE
source_type: youtube
source_platform: youtube.com
title: "State of the Claw — Peter Steinberger"
author: AI Engineer
video_id: zgNvts_2TUE
captured_at: 2026-04-22
duration_min: 44
status: raw
---

# State of the Claw — Peter Steinberger (AI Engineer)

**Source:** https://www.youtube.com/watch?v=zgNvts_2TUE

## Chapters

- 00:00:00 Project Growth and Statistics
- 00:02:23 Management Challenges and the OpenClaw Foundation
- 00:03:47 Addressing Security Advisories and Vulnerabilities
- 00:10:33 Misinformation and Media Fearmongering
- 00:14:50 The Burden of Open Source Maintenance
- 00:16:12 OpenAI Involvement and Future Independence
- 00:18:57 Audience Q&A Begins
- 00:19:53 OpenClaw's Relationship with OpenAI
- 00:22:28 The Importance of Open and Local Models
- 00:24:57 Coding Workflow and Agent Interactions
- 00:28:28 Defining 'Taste' in AI Development
- 00:30:31 Developing Personality for AI Agents
- 00:33:22 Future Vision: Ubiquitous Agents and Smart Homes
- 00:35:58 Addressing Prompt Injection Risks
- 00:38:33 Future Vision: Implementing 'Dreaming' and Modularity
- 00:40:24 Life as a Maintainer and Future Skills

## Transcript

[00:00:17] next presenter is the creator of Open
[00:00:18] Claw, the world's fastest growing
[00:00:20] open-source AI. He recently joined
[00:00:23] OpenAI to work on bringing agents to
[00:00:26] everyone. Please join me in welcoming to
[00:00:28] the stage Peter Steinberger.
[00:01:00] So, Swiss asked me to do a state of the
[00:01:00] claw. Who here is running open claw?
[00:01:03] Give me some hands.
[00:01:05] Ah, it's like 30 40%. Very good. Um,
[00:01:10] yeah,
[00:01:12] it's been quite a few months. Um, the
[00:01:16] project is now five months old.
[00:01:19] I think it's fair to say by now that we
[00:01:21] are the fastest growing project in
[00:01:24] GitHub's history. Um, if you've seen the
[00:01:26] the graph, usually it's some some
[00:01:29] projects look like a hockey stick, but
[00:01:31] ours was just like a straight line and a
[00:01:33] friend called it stripper pole gross
[00:01:37] and that comes with its own challenges.
[00:01:39] So, we have I think now we are the the
[00:01:43] largest number on GitHub stars. There's
[00:01:45] a few that are bigger but they're
[00:01:47] basically educational target. No other
[00:01:49] software project is that big. It's
[00:01:51] around 30,000 commits. It we're closing
[00:01:55] in 2,000 contributors
[00:01:58] soon to be 30,000 PRs. Um,
[00:02:06] see, and we're not slowing down. So, you
[00:02:06] see that it's a ramp, but you know, it's
[00:02:09] we only have April 9. So, um,
[00:02:15] velocity keeps keeps being good.
[00:02:23] And at the same time,
[00:02:23] it hasn't been easy. You know, I I had
[00:02:26] two roads when I when I decided what I
[00:02:28] want to do and I I did the whole company
[00:02:31] thing. I was like, I don't want to do
[00:02:32] this again. And then I joined OpenI, but
[00:02:35] then we also created the Open Cloud
[00:02:36] Foundation. And now I kind of have two
[00:02:38] jobs.
[00:02:39] And running the foundation is like a
[00:02:42] running a company on hard mode because
[00:02:44] you have like all the all the things
[00:02:46] that you need to take care of but also
[00:02:48] you have a lot of volunteers that you
[00:02:49] can't really direct.
[00:02:52] So
[00:02:54] one of my goals has been working on the
[00:02:56] on the bus factor like who does comets.
[00:02:59] Um and you see that it's slowly
[00:03:02] improving.
[00:03:04] Vincent's actually talking after me but
[00:03:07] we're still not we're still not there.
[00:03:10] Um, in the last months I I talked to a
[00:03:13] lot of companies.
[00:03:16] So we now have people from Nvidia on
[00:03:19] board. We have someone from Microsoft on
[00:03:21] board to like help with MS Teams with
[00:03:23] like a Windows app. Uh, we have someone
[00:03:25] from Red Hat who's really helping us um
[00:03:28] with security and dockerization. We work
[00:03:31] with a lot of Chinese companies. We have
[00:03:33] people from from Tencent and Biteance.
[00:03:35] um they're actually much larger users
[00:03:38] than any other continent
[00:03:42] and yeah people from pretty much around
[00:03:44] the world but like the main thing I I
[00:03:47] want to like talk a little bit about is
[00:03:48] about open claw is so insecure you know
[00:03:51] you've you've seen the
[00:03:54] you've seen the memes like open claw
[00:03:56] invites the bad guys
[00:03:59] and you probably also seen
[00:04:04] companies like Nvidia
[00:04:05] doing Nemo claw and like everyone has
[00:04:09] little lobsters.
[00:04:15] So
[00:04:15] you also notice that like in the last
[00:04:17] two three months there's been a lot of
[00:04:19] releases where things broke.
[00:04:21] I've basically been been dodoed by
[00:04:24] security advisories. So that's what I
[00:04:28] did um and what I focused on. So far we
[00:04:31] got 1,142
[00:04:34] advisories. That's around 16.6 a day. 99
[00:04:39] are critical. Um we published around 469
[00:04:43] and we closed 60% of them. So these
[00:04:47] numbers sound like absolutely
[00:04:48] terrifying.
[00:04:51] If you compare it for example to like
[00:04:52] other large projects like the Linux
[00:04:55] kernel gets like eight or nine a day. we
[00:04:58] get like twice as much and curl so far
[00:05:00] has 600 reports we have like twice as
[00:05:02] much as curl.
[00:05:10] So every time I I get a
[00:05:10] security incident, the rule is the
[00:05:14] higher the higher they screaming how
[00:05:16] critical they are, the more likely it's
[00:05:18] slop. Like we we I mean you've probably
[00:05:22] also seen the news like we we we are
[00:05:24] very fast moving into a world where
[00:05:29] we have to change how we build software
[00:05:31] because all these AI tools are getting
[00:05:33] so good at identifying
[00:05:37] even the most weird multi-chained
[00:05:40] exploits and like we're gonna going to
[00:05:42] break all the software that exists. I
[00:05:44] give you an example like
[00:05:46] uh Nvidia they
[00:05:49] they launched Neimoclaw and Neimoclaw is
[00:05:52] a a plug-in and a security layer for
[00:05:54] open claw. You can put it in a sandbox.
[00:05:57] I the keynote was on Monday. They
[00:05:59] invited me on Sunday to like work with
[00:06:01] them. I hooked it up to Codex security.
[00:06:04] It found like five different ways how to
[00:06:06] break out of the of their secure sandbox
[00:06:08] within half an hour.
[00:06:11] That's because like if you use that
[00:06:12] product, you get access to the unnerved
[00:06:15] model that is quite a bit smarter in
[00:06:18] terms of cyber than what the public has
[00:06:21] access. Exactly. Because it's dangerous.
[00:06:30] But yeah um
[00:06:30] also this whole industry those people
[00:06:33] for them it's like credits right the
[00:06:35] more the more issues they find the more
[00:06:37] they seen so like openclaw was like the
[00:06:40] insecure product that everybody tried to
[00:06:42] break so literally like hundreds of
[00:06:43] people firing up their clankers trying
[00:06:46] to break open claw
[00:06:49] um
[00:06:57] the typical attack surface is like
[00:06:57] remote code execution,
[00:07:00] bypass approval, code injection, pass
[00:07:03] traversal. Uh again sounds all very
[00:07:07] dangerous
[00:07:09] and I give you I give you one one
[00:07:11] concrete example. Um
[00:07:14] Gshjp.
[00:07:16] This is about a this is a CVSS of 10. So
[00:07:20] it's like the scariest thing that you
[00:07:22] can possibly do.
[00:07:25] It is an issue where if you
[00:07:30] uh sync for example the iPhone app that
[00:07:33] we haven't even shipped yet but is in
[00:07:34] progress and you give it only read
[00:07:37] permission then you could like break the
[00:07:40] system to also get write permission.
[00:07:43] So this this one was so critical that
[00:07:46] the I know this one's actually different
[00:07:48] one
[00:07:50] in all in all practical ways
[00:07:54] it is not even an incident because the
[00:07:56] the the typical use cases you install it
[00:07:59] on your machine
[00:08:01] either in a cloud or if you have to on a
[00:08:04] Mac mini I stopped fighting this I'm
[00:08:06] just letting people have fun now
[00:08:10] but in 99% 99% cases you'll either have
[00:08:15] access to your gateway or you have not
[00:08:17] access to the gateway. In in in my
[00:08:19] defense, this was my mistake that I
[00:08:21] tried to create a a more permissive
[00:08:23] model. For example, if you have devices
[00:08:26] that would target speech and then would
[00:08:29] only like read certain things. So
[00:08:31] there's like some use case where you
[00:08:32] could like have a a reduced permission
[00:08:34] system would make sense.
[00:08:36] Um but nobody's even using that. But
[00:08:39] this doesn't matter because the rules of
[00:08:42] the of those how you create the CVSS
[00:08:44] numbers don't contribute to that at all.
[00:08:47] And I try to play by the rules. So it is
[00:08:49] a 10 out of 10. And the world is going
[00:08:52] crazy over incidents that in all
[00:08:54] practical ways will not affect people.
[00:08:58] There's some other stuff that does
[00:08:59] affect people. Uh we have nation states
[00:09:03] trying to like hack people. There was
[00:09:05] like ghost claw which is like from
[00:09:07] likely from North Korea which is
[00:09:10] basically
[00:09:11] confusing people with a different NBN
[00:09:13] package and if you if you go to a wrong
[00:09:15] website and you try to download it you
[00:09:17] get like a a root kit. Um that's outside
[00:09:20] of our control. This happens for other
[00:09:22] people as well. Um,
[00:09:25] also there's the Axios thing which funny
[00:09:28] enough we are not using Axios
[00:09:31] but we are using MS teams or Slack as a
[00:09:36] dependency and they're using XIS and
[00:09:38] they didn't pin us and of course uh
[00:09:41] because that's how supply chain attacks
[00:09:43] work we were also affected.
[00:09:51] Yeah. How do you survive 1,142? I'm sure
[00:09:51] it's 1,150.
[00:09:53] Uh for a while I I I tried to handle a
[00:09:57] loop by myself and which is absolutely
[00:09:59] impossible.
[00:10:01] So So the fastest way to get help was
[00:10:04] like getting getting help from companies
[00:10:08] um and Nvidia has been really amazing to
[00:10:10] like give us some people that basically
[00:10:14] work full-time going through the slop
[00:10:16] and hardening the code base.
[00:10:30] okay.
[00:10:30] That um
[00:10:33] this is one of the anglers. The other
[00:10:35] angle is like there's a lot of companies
[00:10:37] that do fearongering and it's not just
[00:10:40] companies, it's also universities. I
[00:10:43] don't know if you've seen it. There was
[00:10:44] like this um
[00:10:47] paper who made the rounds agents of
[00:10:48] chaos and they say oh it's it's about
[00:10:52] agents in general but then there's four
[00:10:54] pages that explain the open claw
[00:10:56] architecture in utmost detail
[00:10:59] but you know which page they didn't even
[00:11:00] mention
[00:11:02] a security page where we explain how you
[00:11:04] should install it because then it
[00:11:06] wouldn't be fun then it wouldn't be it
[00:11:08] would be hard to make a good story. So
[00:11:11] what they instead did is they ignored
[00:11:15] all of the recommendations we do on
[00:11:17] security. Recommendation is it's your
[00:11:19] personal agent. Don't put it in a group
[00:11:22] chat. If you put it in a group chat,
[00:11:24] turn on sandboxing because if anyone can
[00:11:27] talk to your agent, they can excfiltrate
[00:11:29] anything that the agent can do, right?
[00:11:32] So if it's a team agent, it should only
[00:11:34] know what the team can know and not any
[00:11:36] secret data. And you probably want to
[00:11:37] like have it restricted. If it's your
[00:11:39] personal agent, you should be the only
[00:11:41] one being able to talk to you. But if
[00:11:43] you don't play by these rules, you can
[00:11:45] get some really fun interactions like,
[00:11:47] "Hey, I can talk to your agent and it
[00:11:49] can break your system." And then because
[00:11:51] I I was I was grilling them a little bit
[00:11:53] because I had some questions how to do
[00:11:55] things. They told me, "Oh yeah, no, we
[00:11:56] run it in pseudo mode because we wanted
[00:11:58] the agent to be like maximum powerful."
[00:12:01] So they actually fought the setup. It's
[00:12:04] actually not easy to run it in pudo
[00:12:05] mode. You have to change code. um
[00:12:09] but they didn't mention it in the report
[00:12:11] because again that wouldn't give them
[00:12:13] cloud.
[00:12:21] So yeah um my current frustration is
[00:12:21] like there's like a whole industry that
[00:12:24] try to put the project in negative
[00:12:26] light. It's a nightmare.
[00:12:28] It's insecure by default. It's
[00:12:30] unacceptable.
[00:12:31] Um
[00:12:33] and meanwhile a lot of people love it
[00:12:36] and people who actually
[00:12:38] read the security docs understand it can
[00:12:40] use it just fine. One example that I
[00:12:42] found particularly great is u we had one
[00:12:46] remote one rce that panicked Belgium.
[00:12:50] So the Belgium cyber security did a
[00:12:53] release uh about a remote execution
[00:12:56] environment
[00:13:03] and the whole bug was
[00:13:03] a feature where a malicious website
[00:13:06] could create a link
[00:13:13] that would
[00:13:13] trigger the gateway and then forward
[00:13:15] your gateway token. Now if you use the
[00:13:18] setup that is the default and that is
[00:13:21] recommended the gateway token is local
[00:13:24] only or if you have to it's in your
[00:13:26] private network no external website can
[00:13:29] actually access it. If you
[00:13:33] actively fight the setup and for example
[00:13:35] use cloud code to set it up without
[00:13:37] reading, you might be able to get this
[00:13:39] setup working.
[00:13:41] But again,
[00:13:43] that's not anything what's said on the
[00:13:45] website.
[00:13:52] So to be very honest, yes, there's
[00:13:52] absolutely
[00:13:54] uh risk. the the the big risk is the the
[00:14:03] basically the legal trifecta. You know,
[00:14:03] any any agentic system that has access
[00:14:07] to your data,
[00:14:10] has access to untrusted content and the
[00:14:13] ability to communicate is something
[00:14:16] that's potentially at risk. That's not
[00:14:19] anything special to OpenClaw. It's like
[00:14:21] any any agent any power agent system has
[00:14:24] a problem. The more the more powerful
[00:14:28] you make it, the more it can do for you,
[00:14:31] but the more you also have to understand
[00:14:33] what it does. So this is like the the
[00:14:35] main issue
[00:14:41] >> but people not talk about this. Yeah.
[00:14:42] And then also
[00:14:44] um
[00:14:47] some part about maintaining.
[00:14:50] So
[00:14:53] the problem is like if you get all those
[00:14:54] security advisories,
[00:14:57] you know that most of them are created
[00:14:59] with agents, but you still have to use
[00:15:02] your brain to actually read it because
[00:15:04] we're not at the point where you can
[00:15:06] fully trust or I'm not at the point
[00:15:07] where I I can just fully trust that the
[00:15:10] agent will figure it out. So it is a
[00:15:12] huge burden on on time and you never
[00:15:14] know. I mean sometimes you can you can
[00:15:16] often guess you know anytime the reput
[00:15:19] is too nice or like someone apologizes
[00:15:22] that's very likely AI because usually
[00:15:24] people in security don't apologize. Um
[00:15:29] but it is a huge problem and it's
[00:15:30] something that I see more and more open
[00:15:32] source projects complaining about or
[00:15:34] like breaking. Um,
[00:15:37] some are very public about it like
[00:15:38] ffmpeg.
[00:15:44] Usually you get the report. It's very
[00:15:44] rare that you actually get a report and
[00:15:45] a fix. If you get a report and a fix,
[00:15:48] it's usually a very bad fix. If you rush
[00:15:52] it, as I sometimes did in the beginning
[00:15:53] because I was overload, you will very
[00:15:56] certainly break your product.
[00:16:06] Yeah. So this is something that's just
[00:16:06] very difficult to pull up only with
[00:16:09] volunteers. So we so
[00:16:12] what are we working on?
[00:16:14] Number one is
[00:16:17] I
[00:16:19] people say like open AI bought open claw
[00:16:22] that's not the truth. they might bought
[00:16:24] my soul.md
[00:16:25] um but they very much understand that in
[00:16:28] order for what the world needs is like
[00:16:32] more people that play with AI to like
[00:16:35] understand what AI can do to both
[00:16:37] understand the risk and also the
[00:16:38] possibilities they understand that if
[00:16:41] you or like someone who never played
[00:16:44] with never used AI suddenly is at home
[00:16:47] and uses openclaw they'll come to work
[00:16:50] and they will ask why don't we have AI
[00:16:51] at work so they very much understand
[00:16:53] that like supporting this project is
[00:16:55] very useful and in order for that
[00:16:57] project to be successful cannot be under
[00:16:59] one company. Therefore, I'm kind of
[00:17:01] building Switzerland with the open glove
[00:17:03] foundation and I have Dave was helping
[00:17:05] me with it. Um, it's almost done. The
[00:17:08] last thing that's keeping us going is
[00:17:10] like the American bank system which is a
[00:17:13] little bit slow and very confused when
[00:17:15] you're not American.
[00:17:16] Um, it's inspired by what Ghosti did.
[00:17:20] And this will actually then help us to
[00:17:22] hire full-time people to both keep up
[00:17:26] the pace, improve the quality, and free
[00:17:29] up some of my time that I can work on on
[00:17:31] cool stuff again.
[00:17:40] And that's my little update on State of
[00:17:40] the Claw. I'll be around later for like
[00:17:42] a Q&A. Thank you for listening.
[00:17:46] Okay,
[00:17:48] great. Thank you for the whoop. Love the
[00:17:50] whoop. Um, so excellent. Okay, you've
[00:17:53] chosen the claw uh track to get started
[00:17:57] on for our our breakouts and uh uh it's
[00:18:00] going to be great. I think it's going to
[00:18:01] be it's going to be a good session. Um
[00:18:03] we are going to be hearing about a bunch
[00:18:05] of different things uh related to uh
[00:18:08] openclaw and just personal AI assistance
[00:18:10] in general. There's some open claw
[00:18:12] contributors, openclaw maintainers, uh
[00:18:15] um uh open claw competitors, uh and open
[00:18:18] claw creators, uh going to be here on
[00:18:21] the stage. Um we're actually going to uh
[00:18:23] be taking this through until the lunch
[00:18:25] break. Um oh, there we go. We can see up
[00:18:27] there. So, it's about an hour and a half
[00:18:29] of uh of sessions, slightly shorter
[00:18:32] sessions than uh than earlier, I think.
[00:18:34] Um but we're going to be starting with
[00:18:35] uh an AMA. came in. You saw Peter
[00:18:37] earlier on, but you're going to get a
[00:18:38] chance to ask questions and there's
[00:18:40] going to be a bit of a conversation uh
[00:18:42] with Peter and Swix. So, I think to get
[00:18:44] us started, I will simply invite Swix up
[00:18:47] who will kick things off. So, uh please
[00:18:50] welcome him to the stage. Swix, come on
[00:18:52] up. Swix.
[00:18:57] >> All right.
[00:18:57] >> Actually, you can just go together.
[00:18:59] >> You can come out together. There's no
[00:19:01] secret. Peter, welcome. Everybody there
[00:19:03] is
[00:19:09] Okay, so the deal for this is meant to
[00:19:09] be an AMA. Uh the the main idea is that
[00:19:12] I've run six of these AI engineers and
[00:19:15] whenever we have some big maintainer,
[00:19:17] big VIP, we only give them a talk, but
[00:19:20] actually you guys have questions that
[00:19:21] you want to ask. Uh so uh we wanted to
[00:19:24] sort of create that opportunity. So you
[00:19:25] can you can submit there. I'm going to
[00:19:26] moderate uh and and all that. Uh the
[00:19:29] spicy one I'm just going to start off
[00:19:31] with. Pete just quote uh quote tweeted
[00:19:33] uh me and saying send all your questions
[00:19:36] about closed claw right uh
[00:19:40] I think uh people have a lot of
[00:19:42] questions about um the future of
[00:19:44] openclaw at openai uh and uh I wanted to
[00:19:48] give you the space what what is the what
[00:19:49] are people saying about closed claw and
[00:19:50] then what is your response
[00:19:53] >> I didn't even think about it was like it
[00:19:56] came up when when I decided to go to to
[00:19:59] openi And
[00:20:02] I think I think people have a point that
[00:20:06] open air wasn't always
[00:20:08] amazing with open source. And I I think
[00:20:11] a lot changed like Codex is open source
[00:20:13] now. They released Symfony which is a
[00:20:15] really cool orchestration layer. So like
[00:20:16] like they're really leaning in and
[00:20:18] understanding open source now. They
[00:20:20] understand that open cloud needs to stay
[00:20:23] open work with any model be it be it one
[00:20:27] of the the big companies or being a
[00:20:30] local model um everybody in the industry
[00:20:34] wins if more people spend time with AI
[00:20:38] you know if if I if I think AI is
[00:20:41] something scary and then suddenly I I I
[00:20:43] play with open claw and suddenly it's
[00:20:45] like fun and weird and then I come to
[00:20:47] work and there's no like I don't have AI
[00:20:50] tools at work. I'm going to get to my
[00:20:51] boss and say why the f do we not have AI
[00:20:53] at work and and then like those
[00:20:56] companies would probably not run open
[00:20:59] claw but we want something that's like
[00:21:00] hosted and managed and and then somebody
[00:21:04] can can make a sale. So they they're
[00:21:06] like very much on board. They provide me
[00:21:08] with resources. Um, actually it's me
[00:21:11] like I could get a lot more people from
[00:21:12] OpenAI to help with the project, but
[00:21:15] that would just make a picture that they
[00:21:18] could have taken over the project and I
[00:21:20] don't want that. So I I I brought in
[00:21:22] people from Nvidia, we have someone from
[00:21:24] Microsoft, from Telegram, someone from
[00:21:27] Salesforce of all the companies. So So
[00:21:29] shout out actually there's cool people
[00:21:31] at Slack. So we have someone that
[00:21:33] maintains the Slack plugin. Now I
[00:21:36] brought Tensent on board, Bite Dance. We
[00:21:39] talked to Alibaba, Miniax, Kimi, like
[00:21:41] all the all the model providers. They're
[00:21:43] like very much on board. Um, Nvidia has
[00:21:46] been immensely helpful. They
[00:21:50] I think I one of the coolest companies
[00:21:51] in terms of here's some engineers who
[00:21:53] actually like just hire agency and just
[00:21:55] do things.
[00:21:56] >> Yeah. Uh and now that I have all the
[00:21:58] other companies, I'm also bringing a few
[00:21:59] people in from OpenAI to to help
[00:22:01] maintain the project because it's I mean
[00:22:04] software is just like changing that the
[00:22:06] the pace at which this project operates
[00:22:09] is is insane. You kind of like you need
[00:22:12] an army. Um and I'm working on that.
[00:22:16] >> You have an army. Uh and but but you
[00:22:18] know even the contributor chart that you
[00:22:20] showed uh shows that it's hard to get
[00:22:22] quality contributors to stick around.
[00:22:24] people keep hiring your maintainers and
[00:22:25] then you have to find new ones. Um so
[00:22:28] there's a lot of questions about local
[00:22:30] models and open models. Uh you know like
[00:22:32] not every part of the stack is open.
[00:22:34] There's many models where you don't have
[00:22:36] access to the models and and you know
[00:22:39] there's sort of weird restrictions. Um
[00:22:41] how important is open and local models
[00:22:44] to the future openclaw? I mean part of
[00:22:47] part of what what motivated me to build
[00:22:50] open claw is you see all these large
[00:22:52] companies and then they have connectors
[00:22:55] to my Gmail and then my my email is
[00:22:58] hosted somewhere then this company has
[00:22:59] full access to my email and then I can
[00:23:01] get a little bit down there like it's
[00:23:03] much more exciting to me if I have all
[00:23:05] my data actually under my control and I
[00:23:08] and like a little bit of it goes up
[00:23:10] there if I need the top tier token.
[00:23:13] >> Yeah. and like a second kind of
[00:23:15] hierarchy of uh fallback models.
[00:23:17] >> Yeah, you want to I mean I'm I'm
[00:23:18] European at heart. You want to own your
[00:23:19] data, you know. So so so and nobody
[00:23:22] built it. So for me that was very
[00:23:24] attractive and also the the fact that
[00:23:28] you know if if you're a startup you want
[00:23:30] to connect to Gmail, it takes like half
[00:23:32] a year and it's like a very very
[00:23:34] difficult process. But if I'm a consumer
[00:23:37] my clanker can click on any website and
[00:23:39] it happily clicks on I'm not a bot. If
[00:23:42] you have to give me the data somehow, if
[00:23:44] you can if you give me the data, my my
[00:23:47] agent is able to get the data. So you
[00:23:49] can work around a lot of those those
[00:23:51] silos those big companies are building
[00:23:53] and ultimately you can do much cooler
[00:23:55] automation use cases that large
[00:23:57] companies can never do.
[00:23:58] >> So it's it's like
[00:24:00] it's a little bit the the hacker way.
[00:24:03] >> Yeah. And um any indications from the
[00:24:07] open team on GBTOSS? Is that continu
[00:24:10] continuing to be a stream of work that
[00:24:13] uh will be aligned with open claw or or
[00:24:16] is that like separate?
[00:24:18] >> I'm not I'm not in a position to give
[00:24:20] yeah
[00:24:20] >> give you insights on that just that
[00:24:24] um part of what opencloud triggered is
[00:24:27] that like more people in the company are
[00:24:29] getting excited about open source. Um,
[00:24:33] and I I love that that OpenAI is moving
[00:24:35] more into the open direction. Again, if
[00:24:38] you compare it to some other top tier
[00:24:40] labs that start with an A, uh, that very
[00:24:43] much will sue you if you if you leak any
[00:24:46] of their source um, or block you if you
[00:24:50] are too successful. I I I think Open is
[00:24:53] on a good direction.
[00:24:54] >> Yeah. Okay. I want to highlight this
[00:24:57] question. Um, people love hearing about
[00:24:59] your coding workflow. I think right by
[00:25:02] now your idea of um uh the prompt
[00:25:05] request rather than the pull request is
[00:25:07] is very well socialized and also you've
[00:25:10] been shocking people with just how
[00:25:11] you're spending tokens at OpenAI.
[00:25:14] Uh so basically uh the people want to
[00:25:18] know how you ship and what do you do
[00:25:20] about agent waiting times like why is
[00:25:22] you know you're spinning out so many
[00:25:23] agents. I
[00:25:24] >> I know like I I never imagined that this
[00:25:26] one picture of me would blow up so much.
[00:25:29] >> Yeah. actually
[00:25:30] >> uh give give some numbers just just to
[00:25:32] align people. I I think and there's
[00:25:34] times where I was running almost 10
[00:25:36] sessions at the same time especially
[00:25:39] when I used codeex with 50 51 it was
[00:25:43] quite slow I think now I have to say we
[00:25:47] it's still weird we made improvements
[00:25:51] they both make it faster and then
[00:25:52] there's also fast mode so by now my
[00:25:54] typical workflow is
[00:25:56] maybe half of that maybe five six
[00:25:58] windows instead of double just because
[00:26:00] each loop is faster and like the
[00:26:04] area of work I sync in workers is pretty
[00:26:06] much the same. So I I don't have to use
[00:26:09] split screen so much anymore and I think
[00:26:11] we're going to move into a future where
[00:26:15] um
[00:26:16] token will be will be faster and faster.
[00:26:19] So at some point like this is not
[00:26:21] natural that you work on on six things
[00:26:23] at the same time. Um
[00:26:26] but it's basically a workaround until
[00:26:30] until faster. Yeah. Uh, one of my, uh,
[00:26:35] interesting things of putting you next
[00:26:37] to Ryan was to see how the two of you
[00:26:40] kind of approach uh, token maxing.
[00:26:42] Basically, I'm curious what you think
[00:26:44] about the the complete dark factory
[00:26:45] approach, right? That uh, you don't even
[00:26:48] review code that goes in.
[00:26:57] I think that's more and more doable.
[00:26:57] But also, you know, when I when I
[00:27:00] dark factory in a way also means I come
[00:27:03] up with everything I want to build in
[00:27:04] the beginning and I just don't think you
[00:27:07] can build good software in that way.
[00:27:09] Like
[00:27:11] the way to the mountain is usually never
[00:27:13] a straight line. It is it is it is very
[00:27:16] curved. Sometimes you go a little bit
[00:27:18] off track and then you you see something
[00:27:19] new that inspires you. You find like
[00:27:21] shortcuts. Um
[00:27:24] once you're at the top you you you can
[00:27:25] find the optimal path but you never walk
[00:27:27] like this. So at the same time you will
[00:27:30] the first idea that you have about your
[00:27:32] project is very unlikely going to be the
[00:27:34] final project. But if I if I suddenly
[00:27:37] use the waterfall model again that will
[00:27:39] be the final project. For me that
[00:27:41] doesn't work for me. Like I I build
[00:27:44] steps I play with it. I see how it
[00:27:45] feels. I get new ideas, my prompts
[00:27:48] change. So to me, it's a very iterative
[00:27:51] approach. So I don't see how you could
[00:27:53] fully automate that. You can definitely
[00:27:55] build pipelines for certain things.
[00:27:57] >> Yeah.
[00:27:58] >> But even even for PRs, you don't just
[00:28:00] want to build a pipeline that just
[00:28:01] merges PRs because a lot of them just
[00:28:03] don't make sense, you know, like people
[00:28:05] people will pull your product into all
[00:28:07] kind of directions. But if you automate
[00:28:11] that, the AI will very unlikely know
[00:28:14] what's the right direction. You can
[00:28:15] guide it. I have like a vision document
[00:28:17] that I tried some of that but
[00:28:21] the bottleneck is still sinking and like
[00:28:25] having taste.
[00:28:27] Yeah, taste is very important. Uh how do
[00:28:29] you define taste? This is something that
[00:28:31] in my conversations with people everyone
[00:28:33] understands taste is the moat but nobody
[00:28:35] agrees on what taste good taste is. So
[00:28:38] I'm just curious to hear yours. I think
[00:28:40] in this day and age is like
[00:28:43] the very low level of taste if if it
[00:28:45] doesn't stink like AI and you know
[00:28:47] exactly what I mean you know if if
[00:28:49] something is just so writing style
[00:28:51] personality
[00:28:52] >> also also also UI by now you've seen so
[00:28:55] many so much aentic built UI that you
[00:28:58] immediately know if it's AI
[00:29:00] >> yeah if it has the the color border on
[00:29:02] the left right
[00:29:03] >> yeah I mean for a while it was like the
[00:29:05] purple gradient but much more so I I
[00:29:07] feel It's it's like a feeling the same
[00:29:12] as you can identify AI written slop
[00:29:16] right away.
[00:29:16] >> Yeah.
[00:29:17] >> Um that's why I say it's a smell. Like
[00:29:20] even if you can pinpoint this, you will
[00:29:22] know. So So that's probably the lowest
[00:29:25] the lowest characterization of taste.
[00:29:27] And and then going higher up because now
[00:29:30] so much of software is is automatable.
[00:29:33] There's actually much more time you can
[00:29:34] spend on like the little details. I
[00:29:36] don't know, you know, like like just
[00:29:39] when you when you when you when you run
[00:29:40] open claw, you get like a little message
[00:29:43] uh that sometimes roasts people.
[00:29:46] Those are like the delightful details I
[00:29:48] think that
[00:29:49] >> you'll just not get if you prompt in a
[00:29:51] high level.
[00:29:52] >> Yeah. One one of my favorite tastes of
[00:29:54] yours is how you you uh really put a lot
[00:29:56] of work into your soul soulm and you uh
[00:29:59] you know open source your approach and I
[00:30:02] don't think people worked on enough soul
[00:30:04] until until you came along. So I think
[00:30:06] that's really interesting. Uh my I I I
[00:30:08] have a podcast I haven't done yet. I
[00:30:10] haven't released yet with uh Mikuel
[00:30:12] Parakin, who was the CTO of Shopify now,
[00:30:14] but he was the uh guy leading Bing where
[00:30:17] Sydney was uh the original sort of
[00:30:20] unaligned chatbot that emerged. Uh but I
[00:30:24] think people really have fun when when
[00:30:25] your soul your chatbot has personality.
[00:30:28] Your clanker uh you know has different
[00:30:30] obsessions.
[00:30:31] >> Well, it wasn't because it the world
[00:30:33] changed, right? We had we had chat GBD
[00:30:38] in 2023 and 4 and it was basically
[00:30:43] us having AI without understanding what
[00:30:45] AI can do. So we rebuilt a Google so you
[00:30:48] have like a search field and like you
[00:30:50] get a response and you you don't expect
[00:30:52] Google to have a personality.
[00:30:54] >> Yeah. But now that we moved more towards
[00:30:57] agents, like if if I I didn't think
[00:30:59] about in the beginning WhatsApp relay
[00:31:01] and I just hooked it up to cloud code.
[00:31:05] Um and then I when I was on WhatsApp, I
[00:31:08] noticed that it doesn't feel quite
[00:31:09] right. Like even even though like cloud
[00:31:12] code already has some personality, it
[00:31:14] didn't really fit how people would write
[00:31:16] to you on WhatsApp. So that that's how
[00:31:18] my whole iteration started was like uh
[00:31:20] this again it's about taste, right? It
[00:31:23] doesn't feel quite right. It's like too
[00:31:24] wordy. It uses too many dots. It it it
[00:31:27] my friends text different. And then
[00:31:29] that's how I started working. They say,
[00:31:30] "No, this isn't like try to write more
[00:31:33] like a human."
[00:31:36] >> Uh yeah, I I actually run a writing
[00:31:38] >> like a lobster.
[00:31:39] >> Uh like a lobster. Yes. Um
[00:31:43] uh you know the one of my favorite
[00:31:44] quotes of yours is uh madness with a
[00:31:46] touch of sci science fiction. Yeah.
[00:31:49] Right. Like that this is how you run
[00:31:51] >> um uh AI projects. And I think
[00:31:54] >> not all the art projects, but
[00:31:55] specifically
[00:31:57] something like OpenClaw would have never
[00:32:00] been able, it would not have come out of
[00:32:02] an American company just because it
[00:32:04] would have been killed in legal long
[00:32:07] before it would have been released
[00:32:08] because it just has some problems that
[00:32:11] we haven't really solved as an industry
[00:32:12] yet.
[00:32:13] >> Yeah.
[00:32:13] >> But now we have some mitigations and
[00:32:15] it's getting better. The models are
[00:32:16] getting a lot better. But I don't see
[00:32:21] how any of the big labs could have
[00:32:23] released that. You know, it would be too
[00:32:24] much push back. Oh, and like not enough
[00:32:28] market proof that this is what people
[00:32:30] want.
[00:32:30] >> Yeah.
[00:32:30] >> So like it had to be done by someone
[00:32:35] >> like
[00:32:36] >> outside. Yeah. That that that
[00:32:38] >> sitting
[00:32:38] >> like literally like when I when I built
[00:32:40] it in the very beginning, I was like,
[00:32:41] "Oh, what's the worst that can happen?"
[00:32:43] like it could exfiltrate my token,
[00:32:47] my emails. Yeah, nothing is nothing
[00:32:50] nothing's in there that would like
[00:32:51] completely kill me. You could like
[00:32:53] upload some of my pictures. I was like,
[00:32:55] yeah, I guess the worst are already
[00:32:56] online if you use Grinder. Um,
[00:33:00] so it was like it was like,
[00:33:02] okay, I can live with that risk. It will
[00:33:04] be uncomfortable, but it's like it's
[00:33:06] manageable.
[00:33:07] >> Yeah.
[00:33:07] >> Uh, if your company is a different it
[00:33:10] requires a little different approach.
[00:33:12] >> Yeah. By the way, uh his Instagram
[00:33:14] account, good follow under
[00:33:16] underfollowed.
[00:33:18] It's also it's also has some good stuff.
[00:33:20] Um okay. Uh you were talking about
[00:33:22] WhatsApp, talking about Telegram. A lot
[00:33:24] of these text apps. Um uh text apps are
[00:33:27] good. People are also looking for like
[00:33:28] the next form factor. People want like
[00:33:30] the maybe the the glasses, the earbuds.
[00:33:33] What What is your sort of wish list in
[00:33:36] terms of having agents in your life?
[00:33:44] I started on that actually already, but
[00:33:44] then I was just getting bogged down by
[00:33:48] all the people using it and just like
[00:33:52] the daily grind.
[00:33:55] But if you're at home, I want to be in
[00:33:58] any room and you know at Star Trek when
[00:34:01] you can when you say computer
[00:34:05] I I I want to like talk to my agent
[00:34:07] wherever I am and it should just be able
[00:34:09] to like respond to me. It should know
[00:34:11] where I am. I have like little iPads in
[00:34:14] every room and and my agent can use the
[00:34:16] canvas feature and project stuff on
[00:34:18] those iPads. So like if I ask a question
[00:34:21] that that is like easier to be to be
[00:34:23] answered by also showing me something
[00:34:25] like it could use like the nearest
[00:34:26] display because it's aware of where I
[00:34:28] am. So the phone is just a very
[00:34:32] convenient input point but I kind of
[00:34:34] want to like talk to it from anywhere.
[00:34:36] Yeah.
[00:34:36] >> Like yeah if I'm around and I have
[00:34:37] glasses I should just like be able to
[00:34:39] like listen in and like project
[00:34:40] something on me.
[00:34:42] >> Um
[00:34:43] >> but just ubicular follow you
[00:34:45] >> I think yeah once we have
[00:34:47] >> really smart home. Yeah,
[00:34:49] >> like agents on your phone, but really
[00:34:51] you want ubiquitous agents and then you
[00:34:53] want maybe you will have your your your
[00:34:57] uppercase open claw your private agent
[00:35:01] at work. You might have your I don't
[00:35:03] know lowerase openi claw
[00:35:07] and then
[00:35:13] that claw should be able to like talk to
[00:35:13] your personal claw uh in a way that both
[00:35:18] your company and you are comfortable
[00:35:19] with. So that's kind of like the future
[00:35:20] where we need to work out.
[00:35:22] >> Yeah. Uh one of uh I just did a podcast
[00:35:24] with Maran Dre who's a huge fan uh and
[00:35:27] and also uh have conversations with
[00:35:29] Andre Karpathy. Both of these guys are
[00:35:31] running OpenCloud to run their house.
[00:35:32] And I think OpenClaw for homes is like a
[00:35:35] kind of underrated, but like people are
[00:35:36] really discovering it. And my funniest
[00:35:39] sort of irony is that is it's only
[00:35:41] possible because the internet of
[00:35:43] means that most smart devices are
[00:35:45] terrible in security, which means Open
[00:35:47] Core can run them.
[00:35:49] >> Oh, it's going to be able to work so
[00:35:50] much better in in a few months when the
[00:35:52] models are getting really bad.
[00:35:55] >> Yeah, they're very good. Um, okay. One
[00:35:58] security question. uh about prompt
[00:36:00] injection. How do you want to solve
[00:36:03] prompt injection or what what uh ways in
[00:36:06] which uh have you been thinking about
[00:36:09] the prompt injection problem?
[00:36:12] Probably not enough yet. On the other
[00:36:14] hand, like the the the front end models
[00:36:17] are really quite good at detecting all
[00:36:20] the
[00:36:22] all the cases where like just stuff
[00:36:25] randomly comes in from a website or an
[00:36:27] email is usually not a problem anymore.
[00:36:29] You mark as untrusted content, very hard
[00:36:32] to excfiltrate you from that. If if I
[00:36:36] have unlimited access to your claw and
[00:36:39] can bombard it with stuff, then there's
[00:36:42] still a chance.
[00:36:43] >> Then then there's still a chance. But
[00:36:44] like for one of things,
[00:36:46] >> it's no longer the biggest problem. If
[00:36:48] you use that's also why why you know
[00:36:50] that this is probably the angle where
[00:36:51] like some people say, "Oh, Peter doesn't
[00:36:53] like local models." But then I see like
[00:36:55] people running like a 20 uh billion
[00:36:58] parameter model that just does whatever
[00:37:01] you tell it and and it's not trained to
[00:37:03] have any defenses at all. That's still
[00:37:06] problematic. If you run that and then
[00:37:08] you use a web browser or email um would
[00:37:12] worry me. That's why that's why OpenClow
[00:37:15] warns you if you use a small model. And
[00:37:17] I know people spin the whole thing like
[00:37:18] we hate model. I I love I love I love
[00:37:21] that it we support everything, but like
[00:37:23] you have to
[00:37:26] steer
[00:37:28] the regular user a little bit into a
[00:37:30] direction to make it harder for them to
[00:37:32] shoot themselves in the foot.
[00:37:34] >> Um
[00:37:36] yeah, there there is some ideas for
[00:37:38] problem injection. It's
[00:37:44] >> just a little bit away. I haven't
[00:37:44] announced that.
[00:37:45] >> I think Simon Willis has been working a
[00:37:46] lot on on this. is I mean he coined the
[00:37:48] term prompt injection and the sort of
[00:37:50] dual LLM approach seems smart uh and I'm
[00:37:54] I'm not smart enough to figure out all
[00:37:56] the ways that which it can be attacked
[00:37:58] like at at some point trust just has to
[00:38:00] be a thing right um and uh and I pro
[00:38:04] something interesting I found out from
[00:38:05] talking with Vincent who's speaking next
[00:38:07] is that you guys had to implement the
[00:38:08] same trust system that Toby Luca had to
[00:38:10] implement which is uh you build
[00:38:13] reputation over time and things with
[00:38:15] more trust uh gets more privileged
[00:38:18] access, right? And I think that that
[00:38:20] makes sense.
[00:38:23] >> That's part of the story.
[00:38:24] >> Yeah. Yeah. Yeah. Um okay, so uh some
[00:38:28] more broader questions. What cool
[00:38:30] projects would you like to work on once
[00:38:31] you have more free time?
[00:38:33] >> I mean, I wanted to work on dreaming and
[00:38:35] know like my maintenance worked on
[00:38:36] dreaming while I I'm there like
[00:38:38] >> while you were dreaming.
[00:38:39] >> Uh so shift it, right?
[00:38:41] >> Yes. What what is dreaming? Uh it's like
[00:38:44] a way to reconcile memories and like
[00:38:46] kind of create a little bit like like a
[00:38:48] dream log go through like your session
[00:38:50] logs. Um
[00:38:53] >> we we found out from the enthropic
[00:38:55] source code leak that they also working
[00:38:57] on dreaming, right?
[00:38:58] >> Oh yeah. Yeah. I mean there's
[00:39:00] I'm pretty sure there's like more
[00:39:02] companies working on that. But think a
[00:39:04] little bit like how do we learn as
[00:39:05] humans? You you experience a lot of
[00:39:07] things during the day and then you sleep
[00:39:10] and and in sleep your your brain does
[00:39:12] like a garbage collect
[00:39:14] converts some me some
[00:39:17] local locally stored memories into
[00:39:19] long-term storage and like drops others
[00:39:22] and that that's similar ideas that I
[00:39:24] think could also be very useful for
[00:39:26] agents. Um and then like what we shipped
[00:39:29] on dreaming is like the first little
[00:39:30] step in that direction.
[00:39:31] >> Yeah. It's related to the wiki uh thing
[00:39:34] that Andre has been talking about where
[00:39:37] you sort of collect everything into a
[00:39:38] >> wiki is is more memory but like
[00:39:40] everything kind of blends a little bit
[00:39:41] together. Um that the beauty the beauty
[00:39:44] of open claw is that we can just try
[00:39:46] stuff you know like like everything what
[00:39:49] we worked on for the last months or so
[00:39:51] is that
[00:39:53] in the beginning it was a big spaghetti
[00:39:55] codebased mess and now like everything
[00:39:57] everything is an extension a plug-in. So
[00:39:59] you can replace memory, you can add the
[00:40:01] wicki, you can add dreaming, you can add
[00:40:05] I don't know your your your whatever
[00:40:08] crazy idea you have and just make it
[00:40:09] your own. You don't have to send
[00:40:11] everything to a pull request because
[00:40:13] we're still completely overloaded on
[00:40:14] those. But it's it's more like Linux
[00:40:17] where you just can install your own
[00:40:19] parts.
[00:40:20] >> Yeah. Yeah. And uh you are building what
[00:40:24] a lot of people think uh is the most
[00:40:27] consequential open source since Linux
[00:40:29] which I don't know how do you deal with
[00:40:30] that? How do you deal with the the the
[00:40:32] fame what is a day in your life uh as as
[00:40:36] the BDFL effectively of something like
[00:40:39] this?
[00:40:40] >> What's my Well, there's still a lot of
[00:40:42] coding. There's also a lot of
[00:40:44] >> by the way in in between sessions he was
[00:40:46] coding
[00:40:48] back there.
[00:40:49] >> Yeah. They get tokenized. You have to
[00:40:50] like something has to be right.
[00:40:51] >> You have to push the agents, right?
[00:40:53] >> Yeah. Um
[00:40:56] where it shifted a little bit now it's a
[00:40:58] lot more a lot more talking and
[00:41:02] steering people in the right direction
[00:41:04] like because there's a lot of things
[00:41:06] that we already learned at Open Claw. So
[00:41:08] like part of my role at OpenI is like to
[00:41:10] like help them not make the same
[00:41:12] mistakes again. Um
[00:41:15] and then and then open claw is like try
[00:41:17] out new things that seem exciting and
[00:41:19] some might work and some might not work.
[00:41:21] Enable enable companies to like build
[00:41:25] their own claw without having to fork
[00:41:26] away but like making everything more
[00:41:28] more customizable. Um yeah and sometimes
[00:41:31] I sleep sometimes you sleep. Okay great.
[00:41:34] Uh I think that maybe this is the last
[00:41:36] good closing questions. Uh, what skills
[00:41:38] do you want humans and engineers in
[00:41:40] particular to focus on developing in the
[00:41:42] age of AI?
[00:41:49] >> Taste was a big one, but I already
[00:41:49] mentioned that
[00:41:56] system design is still very important.
[00:41:56] >> Yes, you we talked about this in San
[00:41:58] Francisco. Yeah,
[00:42:00] >> if you don't think about that, you will
[00:42:02] eventually swipe yourself into a corner,
[00:42:05] right? Just by defining the boundaries
[00:42:09] like the funny thing is like everything
[00:42:11] is in the clanker but you still need to
[00:42:13] ask the right questions otherwise
[00:42:16] that makes the difference of like good
[00:42:18] code that comes out or like really bad
[00:42:20] code that comes out and that's still
[00:42:21] where like all the knowledge you have
[00:42:23] like how you build software you can
[00:42:25] apply to steer the agent into into
[00:42:28] something that is not slop.
[00:42:31] >> Yeah. And then I think I think a skill
[00:42:32] that is becoming more and more important
[00:42:35] is saying no.
[00:42:38] And and and that's something I had to
[00:42:40] learn as well because
[00:42:42] even the wildest idea is just just a
[00:42:45] prompt away.
[00:42:47] And usually this one idea is never the
[00:42:49] problem but like this idea and this idea
[00:42:52] and this idea and this idea and then how
[00:42:54] all of that fits together that's the
[00:42:56] problem.
[00:42:57] >> Yes. So like
[00:42:59] I think we're still bottlenecked on
[00:43:01] syncing and about like big picture
[00:43:03] syncing because imagine the world from
[00:43:06] your clanker like you're being thrown
[00:43:08] into a code base. You might have an
[00:43:11] outdated agent.md file, but you
[00:43:13] basically don't know what DF this is and
[00:43:15] you like then like you tell me, hey, add
[00:43:18] user profiles and you like somehow add
[00:43:21] user profiles and connect it to the two
[00:43:23] things you see, but you didn't see the
[00:43:25] whole system, right? And then that's
[00:43:26] where a lot of those localized solutions
[00:43:28] comes where like your project has like
[00:43:30] vS and and it's our job to like help the
[00:43:34] agent do its best work by like providing
[00:43:35] them with like hints. Hey, you want to
[00:43:37] consider this? You want to look there?
[00:43:39] How would this interplay with this? And
[00:43:41] then and then ultimately you get like a
[00:43:42] much a system that actually is
[00:43:45] maintainable.
[00:43:46] >> Yeah. Um well, thank you for maintaining
[00:43:49] one of the most important software of
[00:43:50] all time and thank you for spending time
[00:43:52] with us.
[00:43:52] >> Thanks for having me.
[00:43:54] >> Hopefully you stick around and answer
[00:43:55] questions. Thank you.
[00:43:56] >> All right.
