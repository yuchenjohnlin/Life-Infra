---
# === identity ===
id: 2yi4mAN3CtE
url: "https://www.youtube.com/watch?v=2yi4mAN3CtE"
title: Advanced Context Engineering
aliases:
  - Advanced Context Engineering

# === creator ===
channel: MLOps.community
channel_url: "https://www.youtube.com/channel/UCG6qpjVnBTTT8wLGBygANOQ"
channel_follower_count: 39500

# === time ===
duration: 1722
upload_date: 20250813
fetched_at: "2026-05-17T08:19:38+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/2yi4mAN3CtE/maxresdefault.jpg"

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
view_count: 818
like_count: 28

# === status ===
availability: public
live_status: not_live

# === lifecycle ===
state: active
---

# Advanced Context Engineering

## Description

Huge shoutout to ⁨@Databricks for sponsoring our conference Agents in Production 2025

Abstract // 
Hi, I'm Dex. I've been hacking on AI agents for a while. I've tried every agent framework out there, from the plug-and-play crew/langchains to the "minimalist" smolagents of the world to the "production grade" langraph, griptape, etc. I've talked to a lot of really strong founders who are all building really impressive things with AI. Most of them are rolling the stack themselves. I don't see a lot of frameworks in production customer-facing agents. I've been surprised to find that most of the products out there billing themselves as "AI Agents" are not all that agentic. A lot of them are mostly deterministic code, with LLM steps sprinkled in at just the right points to make the experience truly magical. Agents, at least the good ones, don't follow the "here's your prompt, here's a bag of tools, loop until you hit the goal" pattern. Rather, they are comprised of mostly just software. So, I set out to answer: What are the principles we can use to build LLM-powered software that is actually good enough to put in the hands of production customers?

Bio // 
Hey - I'm Dex, and I'm hacking on safer, more reliable agents at HumanLayer. HumanLayer helps AI builders create agents that feel more like real coworkers - taking them out of ChatGPT-style interfaces and deploying them into Slack, email, or wherever their users already are. Before this, I was working on AI Agents that managed SQL warehouses, and did a long stint at replicated.com helping the world's best software teams deliver Kubernetes apps into customer environments. I've been coding since 17, when I built tools for NASA researchers to navigate the south pole of the moon. Enjoyer of tacos and burpees (not necessarily in that order)

An MLOps Community Production sponsored by Databricks

## Transcript

[00:00:00] [Music] Um, what's up everybody? I'm Dex. Uh, I could talk a little bit about myself, but I'm not going to. Um, this is 12actor agents and we're here because of all of you. Um, so this talk wouldn't have been possible. I'll give a couple shoutouts at the end. Um but this is basically my journey talking to about a hundred founders, AI engineers, CTO's, people building agents um specifically people building agents that are deployed

[00:00:36] in production especially to enterprise and making hundreds of thousands if not uh millions of dollars in revenue. um and my journey in understanding how different it is that the top 1% of builders uh the way they work compared to the bottom 99% and everything I learned. So um if you're here and you're building agents, you are a part of this and I'm really excited to share my learnings and especially excited for the

[00:01:04] questions, discussions. I might even try to wrap a little early um so that we can have a longer discussion. Um what's it like to build agents in 2025? Um, if you're like me, you went on some kind of journey that looked like this where you decided you want to build an agent. You did some product design, some UX, me, you figured out what you wanted to build, and then we're all engineers here. We know how to use libraries. Uh,

[00:01:24] we don't build everything from scratch. So, you pick up a framework and you get to work and you can ship something really good really fast with a lot of off offtheshelf tools. Um, and it's 80% is good enough to get the CEO really excited about the project and double your budget and tell you to go hire a bunch of people. Um, but it's probably not good enough to put something in customer hands. And we'll get into what

[00:01:42] I mean by 80% uh in a minute. Um and you realize that like in order to get past that 80%, you end up nine layers deep in a Python call stack trying to figure out, oh, how does this prompt get built or where do these tool calls get injected? Where's this all coming from? Uh and if you're like me and a lot of people I talk to, um you kind of just start over from scratch and you use the base API calls and you build your own

[00:02:04] thing. Or uh one project I went on was I realized that this wasn't even like that good a problem for agents. Um, one of the first agents I built was over a year ago. I had a make file um with a bunch of tasks to build my projects and I created a small agent. I said, "You have a tool to read the make file and you have a tool to run the make tasks. Go build my project." Couldn't figure it out. And again, this is GPT4. This was

[00:02:26] almost like pre40 even. Um, but uh it did things in the wrong order. It skipped steps. I just didn't understand how it worked. And after like two hours of just kind of messing around, tinkering on a Saturday afternoon, I just kept updating the prompt. And I had the prompt very specific of like use this one and then use this one and then take the output from this one and feed it into this one. And by the end of it,

[00:02:47] I got it to call the tools in the right order and it could actually access the file system and it could build the project. Uh, and then I reflected and I said, "Wow, like if I had not tried to build an agent, I could have written the bash script to do all I already knew what the workflow was. I could have written a bash script to do all of that in uh in probably about 90 seconds. So, not every problem needs an agent. Um,

[00:03:11] but I want to talk about performance and what 80% really means. Um, because we talked about this um because AI changes the rules. Can you imagine if your REST API failed on 20% of requests? I'd call that an outage. I tell all my customers the API is down. But, um, and in preAI, you had things like latency, uptime, cost, and security. Um, with AI, we also care about accuracy. And there's this other dimension of performance where

[00:03:34] it's like it's normal for your thing to be factually incorrect to hallucinate. People have a tolerance for that. But your goal is to maximize accuracy. And so 12 factor agents and we're going to talk about context engineering. It's really all about performance in that sense of not speed, not cost, not latency, but how do you actually get the AI to reliably solve problems in a way that people can trust it, in a way that

[00:03:56] it can be trusted to do high stakes work. Um, so I went on this journey. Um I think a lot of you have also been on similar journeys or about to go on such journeys. Um and what I came out of it with was that there are some core things that make agents really really good. Um doing a green field rewrite throw out throw out the old software and we're doing the new software now. We're doing we're doing agents and we got our seven

[00:04:19] agents and here's what we're going to build. It's like please no. uh take small modular concepts from your existing codebase um from sorry from agent building and apply them to your existing codebase. And what's cool about this is I don't think you need an AI background to do it. This is really about um it's a lot less about making models better or training or fine-tuning or all this stuff we've been talking

[00:04:40] about. Um the RL talk was super interesting. This is about how do you take the best model you can get your hands on today and get the most out of it. So just like Heroku published this thing called 12 factor apps which was a system of kind of um conventions for how to build software that would run well in the cloud. We don't even have the term cloud native yet but if you're deploying software in the cloud you are doing

[00:05:01] almost all of these things and you don't think about it. You have version control and you have tests and you have a build pipeline. This didn't need this doesn't need to be said anymore. And I think basically my thought is that we need something similar for agents of just like what are the core building blocks no matter how you're building it, no matter where you're shipping it, no matter what problem you're solving, what

[00:05:19] things hold true for all agent implementations. And again, this is just I can't take credit for coming up with a lot of this. This is me talking to a hundred people who figured this out in a way that let them build really cool products and really cool businesses and then writing it all down. So, um, we put up this GitHub repo in April. Uh, turns out a lot of people felt this. We're on the top page of hacker news for all day.

[00:05:41] Um, bunch of impressions on social. I will just present this slide uh without comment. Um, and is on track to hit 10k stars. Uh, with all of your help, I'll put up a QR code again later. That one was only up for a sec. Um, compared to something that feels super hypy like MCP, um, I think a lot of people identify with what we found and what we were saying here. So, there's already 14 contributors to uh, 12actor agents. Um,

[00:06:07] and what really shook out of this was this idea that blew up in June called context engineering. So, uh, this is this is a picture. It was slightly I made the text a little bit bigger, but this is a basic picture that was in the original 12 factor agents from April. Um, Swix even even went so far as to put the main text on the AI engineer talk from June as context engineering. And by the way, as we're going through, I am

[00:06:28] going to blast through the center meat of this presentation because if you really want all those details, you can go watch the other talk. Um, and I want to get to kind of like looking back after three or four months and what we've learned since then. Uh, if you want to go watch the talk, you can go watch it. It'll be easy to find. Um, so that was June 3rd. Uh, on June 12th, Walden from, uh, Cognition wrote this

[00:06:49] really cool essay on how they learned and what they learned building multiple agent systems and what they realized doesn't work well. Uh, six days later, Toby uh, from Shopify came out and talked about essentially like how he thinks about context engineering versus prompt engineering. Andre Carpathy jumped on a week later. Um, and so they had this whole thing of like what is context engineering, all this stuff. And

[00:07:13] like the definition of context engineering in my mind, again, it's all about performance. Um, but it's expanded a little bit. When I talk about context engineering, it's really about how do you build a really good agent? How do you build a bunch of software that is powered by LLMs that feels like a cohesive digital person that is helping you do your job or helping you accomplish a task or entertain you? Um,

[00:07:35] context engineering now as it is used today can also be mean like used to mean how do you use an agent? So, you're jumping into deep research or you're jumping into cloud code and you're giving it all the right pieces of information in a single prompt so that it can do its job properly. that is now also, I think, a valid use of the term context engineering. But I'm going to talk less about that. I'm going to talk

[00:07:57] more about building software that is powered by LLMs that uh and you're engineering the context that goes into your individual API calls. So, just to clarify that um you're going to listen to this talk and it's going to sound like I'm here to talk trash on all the frameworks. Uh the things that are out there are incredible. Um the frameworks are really, really good. They moved us forward in a really important and

[00:08:17] powerful way. Um, this is if anything a list of feature requests, a list of design principles. This is the things that frameworks in AI, the next generation of AI frameworks need to enable us to do um in a way that saves us time on this stuff that's tedious but allows us to move fast and have control over what's what's going on. So um, if I'm not here to bash, what am I here to do? I want you all to question

[00:08:41] everything you know about agents. Unless you already watched the other talk, don't question any of that. Uh but uh open the black box and understand agents from scratch and build great agents with sound engineering practices. Sounds good. Uh again, I'm gonna blast through this middle section of the talk. If you wanted more detail, you can go you can go read the repo and you can also go watch the AI engineer talk um which is

[00:09:04] another 17 minutes of your time. Um there will also be QR codes at the end if you want to go read. So um I want to stop on this one though. This is the most important factor. The thing that makes LLMs good, the things that makes agents feel magical is the ability to take a string like this and turn it into JSON that looks like this. Is taking raw unstructured input and turning it into something that a program will use to go

[00:09:29] execute something meaningful in the world. Whether it's fetching data or changing data or pushing data out, doesn't matter what we do with the JSON. That's those are the other factors. But you can start moving towards agentic software just by doing this pattern. Um that's factor one. Um factor four tools are structured outputs. I'm gonna start speeding through. But basically like tools are not that fancy. The idea of

[00:09:52] tool use like I don't say tool use considered harmful in the sense of like it's bad to give AI access to the world. I mean that the framing of the idea that tool use is a some alien entity interacting with the world I think is like counterproductive to building good agents because all that's happening during tool use. I'm sure many of you have seen this under the hood is an LM is outputting JSON. Deterministic code

[00:10:16] is going to do something with it and maybe you'll feed those results back to the LM. So if you can make models like this, you can feed them into a switch statement like this and you can run some code but there's nothing special about it. um the orchestration and control flow stuff. Again, I'm going to go through this pretty quickly. Um but the way we got here is basically we're building software uh which is already a

[00:10:38] graph. We got these DAG orchestrators like Airflow, Prefect, all these sorts of things. Really good technology that gives you a lot of affordances. Um but the promise of agents is you don't have to write the DAG yourself. You give the event the LLM a event and a goal and it will traverse through the graph uh in its own way and try to figure out exactly um what needs to happen next. Uh, and we model this as a loop. And if

[00:10:59] you were going to um kind of animate what happens, you have your event that goes into the LM. It's going to pick tools over and over and over again. Um, and at each iteration, you're taking the updated context window and feeding it into the prompt. And as a whole, this whole thing is your agent. But this is a simple software construct. And so if we can separate out the core pieces of this architecture that let you do this kind

[00:11:23] of dynamic graph building in real time as the data is being processed, then you can get a lot more flexible and powerful applications. So again, it turns out the bigger that loop gets, it doesn't really work. We'll get back into that. Long context windows are really, really hard. Um even as models get smarter, you'll always get better results with like a really small focused prompt and context. Um but we can build on this. Um, and so

[00:11:45] if you say what's an agent really, you've got your prompt, uh, which is going to turn something, usually a context window, um, but could be an initial event into JSON. And I don't know about you all, but I'm I'm a software engineer. I've written a switch statement before. Uh, I've written a for loop, uh, and I know how to turn data into strings and strings back into data. So, um, a lot of these pieces are not

[00:12:07] that complicated and you can build them yourself. And so, that's what we're going to talk about today. Um, and you can do all kinds of fun stuff like breaking and switching and summarizing and judging and all these things you've read about really cool papers on what agents do. I would say like implement that stuff yourself because it's not that complex. Um, five and six are similar. I'm not going to go a lot here,

[00:12:24] but this is about launching and pausing and resuming agents. Um, basically the idea that if you have your agent loop built like this and uh let's say it gets triggered by a rest or an MCP call, we build some context and we push that into the model then um we call a longunning tool. We can take that context with the longrunning tool selection, put it in the database, interrupt it and then go launch that longunning job. When the job

[00:12:49] is finished, it will post a web hook back to us with the state ID and the result. We can use the state ID to fetch the context out of the database and then we can append the result and then we push it right back in. The core of this thing is all stateless. So agents are just software I think is the big takeaway there and you should maintain flexibility. So that's five and six. Um owning your prompts again there are

[00:13:12] frameworks that can template you out a pretty good prompt. As you get to that 80 and push through the boundary you probably want to own every token of the prompt. Um because LM are pure functions. The only thing that affects the quality of your agent is how good are the tokens coming out. Is it selecting the right next step? Is it selecting the right parameters? The only thing that influences other than getting

[00:13:31] a better model or changing the model parameters. The only thing that in influences the performance of your agent is which tokens are you putting in. Um so I think Nimrod had a good talk about like you could pick from three different models and five different prompts and a couple other things and you have this explosion. So really focused on like if you're not changing the model and the and the temperature and the settings,

[00:13:51] how can you get the best results by messing with the actual tokens you put in the prompt. Um, and I don't know what's better. I don't know what the right approach is. Um, the prompts off the shelf from the templating frameworks may be the best, but I know the more things you can try, the more likely you are to stumble onto something that is really, really powerful and differentiated. Um, similar though on your context

[00:14:11] building. Not going to talk too much about this, but the way you pass information in, you can have a string of tool calls or you can just pass everything that happened in in a single user message. As long as you're conveying to the model what happened and you're asking it, hey, choose the next step. You can do a lot of things that are not the like standard recommended uh context window management. Um, and so

[00:14:30] you can do this in Python really easily by stringifying stuff. We do a lot of traces in this XML stuff and just put the whole thing in the user message. I'll show you a real example later. Um, and like yeah, look at your if you wonder why all the like pros use XML instead of JSON when they stuff data into an LLM, there's a lot more token efficiency. There's a lot this is more meaning dense. The LM has to read less

[00:14:52] stuff to get the same meaning out. Um, and if you don't own your context window, you can't do these kinds of inspections. So that's that's owning your context window. Again, tokens in, tokens out. And everything everything in building great agents is context engineering. the prompt, the memory, the rag, the agentic history, structured output. It's all part of this idea of how do I get the right tokens out of the

[00:15:15] model, and I don't know what's better, but I know you want to try everything. Um, so that's on your context building. The error stuff is pretty fun, but I'm going to skip over it. But basically, by telling a model it did something wrong. Okay, it doesn't want to advance past this video. Yeah, there we go. So, if you have an error, you can catch the exception, put on your thread, and try again. Obviously, this can spin out. You

[00:15:34] have issues with the model making the same error over and over again. I'm sure lots of you have experienced that. Um, the answer is own your context window. Don't put the whole error in. Clean out errors once you get a valid tool call. All kinds of things you can do here to make this better. Um, contacting humans with tools. This is another one I'm going to kind of gloss over, but you should go watch the other

[00:15:52] talk. um is basically like a lot of people I've talked to are using tool calling for everything and having a specific call or multiple different types of functions that allow the model to declare its intent to respond to the user uh in various ways whether it's request clarification or final answer we're done or etc etc lots of different options. So, um, this is what some of our traces look like that enable the

[00:16:15] model to request human input as a tool call. Um, let you do these outer loop agent things. All kinds of fun stuff. And again, I don't know what's better. If you get good results by using that final like stop token that is like, hey, we're outputting plain text now instead of JSON, you should do that. Um, but I know you should try everything. So, that's contact humans with tools. If you are going to contact humans with tools,

[00:16:36] you might as well give the model the ability to talk to the human where they already are. Instead of forcing everyone who's using agents to have like six different browser tabs for every agent, put it in their Slack, put it in their email. Um, your adoption will go up. Um, and this is this is hard to do because human communication over email and Slack is genuinely asynchronous. So without the control flow stuff, you uh lose a

[00:16:56] lot of the flexibility you need to make these stateful asynchronous workflows work well for your problem space. Um the last one is this small focus agents thing. We talked about this loop and why it doesn't really work. What people are doing that works um is using agents in specific parts of the pipeline. This is really like use LLMs for the things that LLMs are really good at. Don't try to have an LLM do your whole workflow. Find

[00:17:20] the parts where there is natural language or there's human in the loop or there are things where it is valuable to take plain text and compact it into an existing problem to output a better result. whether that's a content review um or lots of other use cases. Um we do this at human layer. We have an agent that does our deployments. Most of the workflow is deterministic. Um so let's say a PR gets merged. We will pull that

[00:17:44] in and uh run it, test it, and actually um we're running a little short on time. I'm going to skip this part. Um but basically it's about using agents. Go watch the other talk if you want to. Um, small focus agents, less than 100 tools, less than 20 steps. You'll get really, really good results that way. Um, what if LLMs keep getting smarter? We talked about this a little bit, but basically what's going to happen is, um, as they

[00:18:10] get smarter, there will always be a thing they're not good at. Yesterday, there was a thing that was really hard. Now, it's easy. Um, and there's a new thing that's really, really hard. And these engineering principles in 12 factor agents are going to help you push the boundaries and find that thing that the LLM can't always get right all the time and tune it up so that you're the only one who can get that right all the

[00:18:31] time. This was why notebook LM was so magical. No one had ever seen something that would do things of this high quality this reliably before. So that's kind of the one of the big takeaways there. Um stateless reducer, stateless transducer, call it what you want. Um manage the state outside the LLM. um and you'll have a better time. Um and really quickly, a lot of people ask about evals and why eval isn't in here. I think the

[00:18:53] idea is like if you embrace this LM are pure functions and tokens in tokens out, then you get this like and that everything is context engineering then like you get this um really clean just input output pair of like a trace of everything that happened. Here's what the next tool is and you can eval on that really easily. I'm going to show you some code from a open source agent that we built that manages issues in

[00:19:17] linear for us. So here's our prompt. You can see at the top the list of um the list of different structured outputs we give it. Again, this is about 10 tools or so including three different ways to contact a human. Um and then our testing and our evals. This is using something called boundary ML BAML which I highly recommend. Very cool product, very cool team. Um, but you can pass in, okay, here's the email and you can make make

[00:19:40] assertions about the intent of the output issue. So you can do these deterministic guesses on on what's going to happen and you can make sure if I change my prompt, I don't change the decision-making. So this is a longer thread where it got an error about team ID must be a UYU ID and we can assert that the next intent is to list the teams because it picked a hallucinated a team ID. And here's a full the point is

[00:20:02] not to read this. You can go read the code, it's open source. Um, but this is a full trace of kind of like once all of this is done, we want to assert that it decides that it's done and we get our final answer. So, in summary, we're still finding the right abstractions. Um, there's a couple links like why libraries versus frameworks is a like a way to think about this. Um, whether you should prefer duplication over the wrong

[00:20:22] abstraction. This is from Ruby Comps in like 2014. Um, if you want to make a 12-actor agent, this is coming soon. I know I said this a month ago, it is still coming soon. Thank you for everyone who reached out. Um we are looking for some collaborators on this as well. So I'm excited to share more there. Um basically this is shad CN for agents. I won't go into what that means. Uh but if you've been in this long

[00:20:42] enough you will uh you will know what I'm saying there. Um so in summary agents are software. You can write a for loop. You can write a switch statement. You can serialize a string. So write the dang software. LM are stateless functions. Everything is context engineering. Own your state and control flow. Find the bleeding edge. Be like the notebook LM team. find the thing that the LM can't do and write a bunch

[00:21:02] of code to make it do that thing. Um, agents are better with people. There are hard things in building agents, but you should probably do them anyway. You should most of them. And one of the things we work on a human layer is uh this especially factor 11 making it easy to connect your agents to humans asynchronously. Uh, because wrangling APIs and web hooks isn't the fun part of this problem. So, um, most of what we do

[00:21:23] is open source because we think this is important to solve together. We do the boring stuff and we sell that. This is the agent to human protocol which is in draft right now. Um, but it's just a really simple like four endpoint spec for how to connect agents to humans asynchronously. Um, that's all the pitching I'm going to do today. I mostly just love automating everything and I had a great time learning from the

[00:21:44] community and writing it all down and sharing it with everybody. So, thank you all for being here. Let's go build something. Um, one shout out is to um I do do uh webinars with Fib who was one of the kind of like original architects of the 12 factor agents methodology. Um we kind of came up with this model together at a hackathon back in November. So if you want to learn more and do hands-on workshops, there's a

[00:22:07] link for that on the last slide. Um thank you so much. There's the GitHub. There's the link to the workshops. Uh if you want to chat more, find me on X. Uh I'm Dexory. Um you can find me on LinkedIn. I'm much more active on X though, so please hit me up. Would love to chat more. We'd love to see what y'all are working on. Uh I think that's it. That's 12actor agents. Awesome. Awesome. Again, another another

[00:22:31] information dense talk. Loved it. Um some folks were asking in the chat uh about the other talk that you were mentioning. So those of you who were asking, I put the link in the chat. So go ahead and uh pull that. Um, and so just like maybe rip ripping through some questions here while we have some time. Um, first thing you you mentioned that for the uh uh looks like you're building some kind of tool to like build 12

[00:22:58] factor agents and say you're looking for collaborators. Where do people go if they're interested? >> That is a great question. Um, I would say ping me on Twitter or open an issue on the GitHub repo. Um and uh I there the discussion will probably happen there. >> Cool. Perfect. Awesome. And folks again if you have questions feel free to drop them in the chat and I will uh transmit them back over to Dex. But maybe while

[00:23:26] we're waiting a few other questions maybe they'll lead into some hot takes. So uh you know one of the things that uh you know caught my eyes talking about uh tool calling in in this and I'm just curious you know given your experience of like talking to a lot of people developing this 12 factor framework >> what is your take on JSON tool calling versus like code execution like generating code instead of like

[00:23:52] actual JSON tool calls. >> Okay. Okay, so just having like instead of like wiring up let's say the resend.comm MCP server just have the model write JavaScript that calls the API and then execute that code in a sandbox. >> Yeah. or you know some something that I often see is like people defining util functions which are like the tools you can call and then you know just generating code and you know there's a

[00:24:16] lot of >> there's a lot of people that like point out that JSON tool calling like models are pretty bad at outputting JSON >> and also like it's hard to do like composition with that. So just curious like whether how you see this juxtapose with 12 factor agents. Yeah, I mean I think it all comes down to like thinking at the like thinking at the level of abstraction inside the agent loop because you don't just have to blindly

[00:24:41] call tools in a loop. And so you can get the agent to output code. You can then pass that to another agent that reviews the code and asks a human for the right secrets and you can kind of like delegate all these responsibilities out in a way that is deterministic where you're not depending on the agent to call code. As far as like agents calling tools with JSON, um there's a bunch of different ways to do that. I know that

[00:25:01] the quality goes down when you do constrain generation. Um one of the examples we talk about on the uh on the AI that works show is this idea of like when you do code generation and you're writing Python and it's output in a JSON object and you force constraint generation, when you get to the end of that new line, the model's really going to want the next loit is going to be like 99% to pick the new line character.

[00:25:24] But because it's in JSON and that's not valid JSON, it will be for you're going to zero out that thing and then you're going to be stuck with like one% for the backslash and then 1% for the N and like basically like it becomes way harder to get the model to and backslash and N in almost every tokenizer are two separate tokens by the way. There is no single token for the backslash. I think that would be like if you had a code code

[00:25:50] optimized model, maybe that would be the case. But um so that's another thing to think about. If you can if you can have the model write code in the way that it wants to write code, which is the way code is written in the training set, uh that's better. Uh and I think most models are much better writing code that way. So that's like why the JSON tool calling is off. A lot of people have written like custom prompts that tell it

[00:26:10] to output XML and custom XML parsers that handle the output. It's it's tricky. Again, the Boundary ML folks have a really crazy like Rustbased parser that can take busted JSON and turn it back into real JSON. Um, which is kind of a really interesting approach to the problem. There's one other thing I wanted to say, but I forgot. So, um, there's so much here. >> Yeah. >> Yeah. Awesome. I think we got some

[00:26:33] other, uh, questions in the chat, and we might have a couple of minutes. Maybe we'll take one more question. So somebody asked thoughts on safety prompt injection jailbreak and MCP with root permissions is an unsolved problem but increasingly there's edge cases solved by the frontier models. So what's your mental model for working in this space safely but still quickly? I mean again it comes down to like get

[00:26:58] your get your hands in the logic of the loop. Um, MCP I think is really good for adding AI functionality or adding new functionality to AI for people who are not technical. Um, so like someone or like just technical enough to be dangerous, right? If I'm not super technical, I can paste a pile of MCPJSON into cloud desktop and like suddenly connect it to all my stuff. I think if you're building agents um and you're

[00:27:24] controlling the loop and it's not just a blind call tools call tools call tools until some token comes out that says we're done then um you have a lot more control and you can say cool we're going to call this tool but before the output comes out we're going to use a really small dumb model that's not going to follow instructions and use that to like as a guard rail. So like the answer is like if you build in this way and you

[00:27:46] control every every like token of the prompt and everything that goes in and everything that comes out then you get a lot more flexibility control and the answer is like it's going to be different for every use case. There's no like magic just like with memory there's no magic abstraction that solves the memory program problem and the people I know who are building agents that have really good memory. These like um AI

[00:28:05] tutors that help kids learn math and stuff and they like have really good like memory over weeks and months. All of that is built from scratch. >> Awesome. I think that's all the time we have left. We have our next speaker getting ready, but thanks so much for sharing so much. So remember, hit up that GitHub repo, find Dex on Twitter, and uh you know, uh let's make better agents. >> Super dope. Thanks, Skyler. Thanks,

[00:28:34] everybody. Have a great day. Enjoy the rest of the show.
