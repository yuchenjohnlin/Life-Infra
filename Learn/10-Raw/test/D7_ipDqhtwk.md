---
# === identity ===
id: D7_ipDqhtwk
url: "https://www.youtube.com/watch?v=D7_ipDqhtwk"
title: "How We Build Effective Agents: Barry Zhang, Anthropic"
aliases:
  - "How We Build Effective Agents: Barry Zhang, Anthropic"

# === creator ===
channel: AI Engineer
channel_url: "https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA"
channel_follower_count: 473000

# === time ===
duration: 909
upload_date: 20250404
fetched_at: "2026-05-17T08:19:34+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/D7_ipDqhtwk/maxresdefault.jpg"

# === content structure ===
chapters: []
chapters_authoritative: false
has_real_chapters: false
has_key_moments: false

# === language ===
language: en-US
original_language: en

# === subtitles ===
manual_track_languages: []
auto_track_languages:
  - en
transcript_status: available
transcript_source: auto_en
transcript_target: null
is_translated: false

# === engagement ===
view_count: 459846
like_count: 9791

# === status ===
availability: public
live_status: not_live

# === lifecycle ===
state: active
---

# How We Build Effective Agents: Barry Zhang, Anthropic

## Description

Recorded live at the Agent Engineering Session Day from the AI Engineer Summit 2025 in New York. Learn more at https://ai.engineer and purchase tickets to our next event, the AI Engineer World's Fair, in SF June 3 - 5 here: https://ti.to/software-3/ai-engineer-worlds-fair-2025

About Barry:

Barry is a member of technical staff on Anthropic's Applied AI team, focusing on developing agentic systems with enterprises and startups. Previously, he was a tech lead on the Monetization genAI team at Meta, where he claimed the inaugural 'AI Engineer' title. He holds degrees in Computer Science and Industrial Engineering from Northwestern

## Transcript

[00:00:00] [Music] Wow, it's uh incredible to be on the same stage as uh so many people I've learned so much from. Let's get into it. My name is Barry and today we're going to be talking about how we build effective agents. About two months ago, Eric and I wrote a blog post called Building Effective Agents. In there, we shared some opinionated take on what an agent is and isn't, and we give some practical learnings that we have gained along the

[00:00:41] way. Today, I'd like to go deeper on three core ideas from the blog post and provide you with some personal musings at the end. Here are those ideas. First, don't build agents for everything. Second, keep it simple. And third, think like your agents. Let's first start with a recap of how we got here. Most of us probably started building very simple features. Things like summarization, classification, extraction, just really

[00:01:13] simple things that felt like magic two to three years ago and have now become table stakes. Then as we got more sophisticated and as products mature, we got more creative. One model call often wasn't enough. So we started orchestrating multiple model calls in predefined control flows. This basically gave us a way to trade off cause and latency for better performance and we call these workflows. We believe this is the

[00:01:39] beginning of agentic systems. Now models are even more capable and we are seeing more and more domain domain specific agents start to pop up in production. Unlike workflows, agents can decide their own trajectory and operate almost independently based on environment feedback. This is going to be our focus today. It's probably a little bit too early to name what the next phase of agentic system is going to look like,

[00:02:07] especially in production. Single agents could become a lot more general purpose and more capable or we can start to see collaboration and delegation in multi- aent settings. Regardless, I think the broad trend here is that as we give these systems a lot more agency, they become more useful and more capable. But as a result, the cost, the latency, the consequences of errors also go up. And that brings us to the first

[00:02:31] point. Don't build agents for everything. Well, why not? We think of agents as a way to scale complex and valuable tasks. They shouldn't be a drop in upgrade for every use case. If uh if you have read the blog post, you'll know that we talked a lot about workflows and that's because we really like them and they're a great concrete way to deliver values today. Well, so when should you build an agent? Here's our

[00:02:59] checklist. The first thing to consider is the complexity of your task. Agents really thrive in ambiguous problem spaces. And if you can map out the entire decision tree pretty easily, just build that explicitly and then optimize every node of that decision tree, it's a lot more cost- effective and it's going to give you a lot more control. Next thing to consider is the value of your task. That exploration I

[00:03:23] just mentioned is going to cost you a lot of tokens. So the task really needs to justify the cost. If your budget per task is around 10 cents, for example, you're building a u high volume customer support system, that only affords you 30 to 50,000 tokens. In that case, just use a workflow to solve the most common scenarios and you're able to capture the majority of the values from there. On the other hand, though, if you look at

[00:03:49] this question and your first thought is, I don't care how many tokens I spend. I just want to get the task done. Please see me after the talk. Our go to market team would love to speak with you. From there, we want to derisk the critical capabilities. This is to make sure that there aren't any significant bottlenecks in the agent's trajectory. If you're doing a coding agent, you want to make sure it's able to write good

[00:04:11] code, it's able to debug, and it's able to recover from its errors. If you do have bottlenecks, that's probably not going to be fatal, but they will multiply your cost and latency. So, in that case, we normally just reduce the scope, simplify the task, and try again. Finally, the the the last important thing to consider is the cost of error and error discovery. If your errors are going to be high stake and very hard to

[00:04:39] discover, it's going to be very difficult for you to trust the agent to take actions on your behalf and to have more autonomy. You can always mitigate this by limiting the scope, right? You can have read only access. You can have more human in the loop, but this will also limit how well you're able to scale your agent in your use case. Let's see this checklist in in action. Why is coding a great agent use case?

[00:05:03] First, to go from design doc to a PR is obviously a very ambiguous and very complex task. And second, um we're a lot of us are developers here, so we know that good code has a lot of value. And third, many of us already use cloud for coding. So we know that it's great at many parts of the coding workflow. And last, coding has this really nice property where the output is easily verifiable through unit test and CI. And

[00:05:31] that's probably why we're seeing so many creative and successful coding agents. Right now, once you find a good use case for agents, this is the second core idea, which is to keep it as simple as possible. Let me show you what I mean. This is what agents look like to us. They're models using tools in a loop. And in this frame, three components define what an agent really looks like. First is the environment.

[00:06:02] This is a system that the agent is operating in. Then we have a set of tools which offer an interface for the agent to take action and get feedback. Then we have the system prompt which defines the goals, the constraints and the ideal behavior for the agent to actually work in this environment. Then the model gets called in a loop and that's agents. We have learned the hard way to keep this simple because any complexity

[00:06:29] up front is really going to kill iteration speed. Iterating on just these three basic components is going to give you by far the highest ROI and optimizations can come later. Here are examples of three agent use cases that we have built for ourselves or or our customers just to make it more concrete. They're going to look very different on the product surface. They're going to look very different in their scope. They're going

[00:06:53] to look different in the capability, but they share almost exactly the same backbone. They they actually share almost the exact same code. The environment largely depends on your use case. So really the only two design decisions is what are the set of tools you want to offer to the agent and what is the prompt that you want to instruct your agent to follow. Um, on this note, if you want to learn more about tools, my friend Mahes is

[00:07:19] going to be giving a workshop on model context protocol MCP tomorrow morning. Um, I've seen that workshop. It's going to be really fun. So, I highly encourage you guys to to check that out. Um, but back to our talk. Once you have figured out these three basic components, you have a lot of optimizations to do from there. Uh, for coding and computer use, uh, you might want to, uh, catch the trajectory to reduce cost. For search

[00:07:41] where you have a lot of tool calls, you can parallelize a lot of those to reduce latency. And for almost all of these, we want to make sure to present the agents progress in such a way that gain user trust. But that's it. Keep it as simple as possible as you're iterating. Build these three components first and then optimize once you have the behaviors down. All right, this is the last idea. Um, is to think like your agents. I've

[00:08:09] seen a lot of builders and myself included who develop agents from our own perspectives and get confused when agents make a mistake. It seems counterintuitive to us. And that's why we always recommend to put yourself in the agents context window. Agents can exhibit some really sophisticated behavior. It could look incredibly complex, but at each step, what the model is doing is still just running inference on a very limited set

[00:08:35] of contexts. Everything that the model knows about the current state of the world is going to be explained in that 10 to 20k tokens. And it's really helpful to limit ourselves in that context and see if it's actually sufficient and coherent. This will give you a much better understanding of how agents see the world and then kind of bridge the gap between our understanding and theirs. Let's imagine for a second that

[00:09:02] we're computer use agents now and then see what that feels like. All we're going to get is a static screenshot and a very poorly written description. This is by yours truly. Let's read through it. You know, you're a computer use agent. You have a set of tools and you have a task. Terrible. Uh we can think and talk and reason all we want, but the only thing that's going to take effect in the environment are our

[00:09:25] tools. So, we attempt a click without really seeing what's happening. And while the inference is happening, while the two execution is happening, this is basically equivalent to us closing our eyes for three to five seconds and using the computer in the dark. Then you open up your eyes and you see another screenshot. Whatever you did could have worked or you could have shut down the computer. You just don't know. This is a

[00:09:48] huge lethal phase and the cycle kind of starts again. I highly recommend just trying doing a full task from the agent's perspective like this. I promise you it's a fascinating and only mildly uncomfortable experience. However, once you go through that mildly uncomfortable experience, uh I think it becomes very clear what the agents would have actually needed. It's clearly very crucial to know uh what the

[00:10:14] screen resolution is so I know how to click. Um it's also good to have recommended actions and limitations just so that you know uh we can uh put some guardrails around uh what we should be exploring and we can avoid unnecessary exploration. These are just some examples and you know do this exercise for your own own agent use case and figure out what kind of context do you actually want to provide for the

[00:10:38] agent. Fortunately though um we are building systems that speak our language. So we could just ask cloud to understand cloud. You can throw in your your system prompt and ask well is any of this instruction ambiguous? Does it make sense to you? Are you able to follow this? You can throw in a two description and see whether the agent knows how to use the tool. You can see if it wants more parameter, fewer

[00:11:00] parameter. And one thing that we do quite frequently is we throw the entire agent's trajectory into cloud and just ask it, hey, why do you think we made this decision right here? And is there anything that we can do to help you make better decisions? This shouldn't replace your own understanding of the context, but you'll help you gain a much closer perspective on how the agent is seeing the world. So

[00:11:22] once again, think like your agent as you're iterating. All right. Uh I've I've spent most of the talk about very practical stuff. Uh I'm going to indulge myself and spend one slide on personal musings. This is going to be my view on how this might evolve and some open questions I think we need to answer together as AI engineers. These are the top three things that are always on my mind. First, I think we

[00:11:47] need to make agents a lot more budget aare. Unlike workflows, we don't really have a great sense of control for the cost and latency for agents. I think figuring this out will enable a lot more use cases as it gives us the necessary control to deploy them in production. The open question is just what's the best way to define and enforce budgets in terms of time, in terms of money, in terms of tokens, the things that we care

[00:12:10] about. Next up is this concept of self-evolving tools. I've I've already hinted at this two slides ago, but uh we are already using models to help iterate on the two description, but this should generalize pretty well into a meta tool where agents can design and improve their own tool ergonomics. This will make agents a lot more general purpose as they can adopt the tools that they need for each use

[00:12:36] case. Finally, um I don't even think this is a hot take anymore. I have a personal conviction that we will see a lot more multi- aent uh collaborations in production by the end of this year. They're well parallelized. They have very nice separation of concerns and having sub agent for example will really protect the main agents context window. Um but I think a big open question here is um how how do these

[00:13:02] agents actually communicate with each other? We're currently in this very rigid frame of having mostly synchronous user assistant terms and I think most of our systems are built around that. So how do we expand from there and build in asynchronous communication and and enable more roles that that afford agents to communicate with each other and recognize each other? I think that's going to be a big open question as we

[00:13:23] explore this more multi- aent future. These are the areas that take up a lot of my mind space. If you're also thinking about this uh please shoot me a text. I would love to chat. Okay, let's uh bring it all together. If you forget everything I said today, these are the three takeaways. First, don't build agents for everything. If you do find a good use case and want to build an agent, keep it as simple for as long as possible. And

[00:13:51] finally, as you iterate, try to think like your agent, gain their perspective, and help them do their job. I would love to keep in touch with everyone of you. If you want to chat about agents, especially those open questions that I talked about, uh you'll be incredibly lovely. You can just, you know, uh jam on some of these ideas. Uh these are my socials if you want to get connected. And I'm going to end the

[00:14:15] presentation on a personal anecdote. So back in 2023, I was building AI product at Meta and we had this funny thing where we could change our job description to anything we want. Um, after reading that blog post from Swix, I decided I was going to be the first AI engineer. Uh, I I really love the focus on practicality and just making AI actually useful to the world. And I think that aspiration brought me here

[00:14:39] today. So, I hope you enjoy the rest of the AI engineer summit. And in the meantime, let's keep building. Thank you. [Music]
