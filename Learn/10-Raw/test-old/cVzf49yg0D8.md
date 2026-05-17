---
# === identity ===
id: cVzf49yg0D8
url: "https://www.youtube.com/watch?v=cVzf49yg0D8"
title: Building Conversational Agents — Thor Schaeff and Philipp Schmid, Google DeepMind
aliases:
  - Building Conversational Agents — Thor Schaeff and Philipp Schmid, Google DeepMind

# === creator ===
channel: AI Engineer
channel_url: "https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA"
channel_follower_count: 471000

# === time ===
duration: 6453
upload_date: 20260430
fetched_at: "2026-05-16T07:57:27+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/cVzf49yg0D8/maxresdefault.jpg"

# === content structure ===
chapters:
  - {start: 0, title: "<Untitled Chapter 1>"}
  - {start: 14, title: Introduction and speaker introductions}
  - {start: 375, title: Audience interaction and project discussions}
  - {start: 518, title: Introduction to building conversational agents}
  - {start: 1697, title: Discussion on Gemini Flash for coding and agentic use}
  - {start: 2188, title: Coding agent implementation and tool calling demonstration}
  - {start: 2575, title: Overview of the Interactions API and state management}
  - {start: 2945, title: Introduction to the Gemini Live API}
  - {start: 3002, title: Live Jukebox demo with music generation}
  - {start: 3289, title: Deep dive into Gemini Flash Live features (multimodality, latency, tools)}
  - {start: 4014, title: Technical setup and implementation of the Live API using WebSockets}
  - {start: 5114, title: Session management and context window compression}
  - {start: 5217, title: Real-world business use cases for conversational agents}
  - {start: 5702, title: Multimodal grounding and handling audio inputs}
  - {start: 6000, title: Discussion on personalization and speaker identification}
chapters_authoritative: false
has_real_chapters: false
has_key_moments: true

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
view_count: 5699
like_count: 131

# === status ===
availability: public
live_status: not_live

# === lifecycle ===
state: active
---

# Building Conversational Agents — Thor Schaeff and Philipp Schmid, Google DeepMind

## Description

Thor Schaeff and Philipp Schmid show how to build conversational agents with Google DeepMind's Gemini APIs, from tool-using coding agents to realtime voice interfaces. The session covers the new Interactions API, agent skills, server-side state, and the Live API workflow for streaming audio, video, and tool calls into multimodal assistants.

Speaker info:
- https://x.com/_philschmid
- https://x.com/thorwebdev

Timestamps
0:14 - Introduction and speaker introductions
6:15 - Audience interaction and project discussions
8:38 - Introduction to building conversational agents
28:17 - Discussion on Gemini Flash for coding and agentic use
36:28 - Coding agent implementation and tool calling demonstration
42:55 - Overview of the Interactions API and state management
49:05 - Introduction to the Gemini Live API
50:02 - Live Jukebox demo with music generation
54:49 - Deep dive into Gemini Flash Live features (multimodality, latency, tools)
1:06:54 - Technical setup and implementation of the Live API using WebSockets
1:25:14 - Session management and context window compression
1:26:57 - Real-world business use cases for conversational agents
1:35:02 - Multimodal grounding and handling audio inputs
1:40:00 - Discussion on personalization and speaker identification

## Transcript

Hello everyone. >> Hello.

>> Perfect. >> It's just that Philip and I were both Germans and we thought it was funny. Maybe we we can do it in German. Actually, looks like there's a there's a German crew there, which is nice. Uh, no, no worries. We'll we'll we'll do it in English. We'll do it in a couple different languages. Maybe we'll find out. Do we have other languages in the room? >> Other nationalities? Yeah. What do we

have? >> Shout it out. >> So, Spanish. >> Any Icelandic? >> No. >> D. Okay. Close. Close. Romanian. >> Romanian. Nice. >> Dutch. Pña. Netherlands. >> Okay. >> Which? >> Hindu. >> Yeah. But Hindu. Okay. Canada. No. Okay. Bangalore. No. >> Uh, >> Farsy. All right. Nice. >> Czech. >> Czech. Yeah. Brilliant. Okay. This is uh fantastic. Well, thanks everyone for making your way over here with with all

your languages. Really appreciate it. we can we can really put the model to the test today which is great. Um yeah, hi I'm Thor or to for the German speakers amongst you. Um >> hi I'm Philip um only Philillip so >> for German and English speakers. Yeah, it's nice. We so we work on the developer experience at Google DeepMind broadly covering kind of Gemini API and also uh working on Google AI studio as a

tool for you know developers to try out the models quickly uh and then also the the API um interfaces to use the API. You do need an API key. Uh actually who has an API key already? Gemini API. Okay, couple folks. Uh, who has used AI Studio before? Google AI Studio. Okay, couple folks. Great. Um, maybe we can quickly Sorry, >> anti-gravity. >> Yeah, that's good. Uh, you actually don't need an API key for anti-gravity,

but um, so if you don't have an API key yet, uh, if you have your machine on you, I hope you do. Uh, it's it's it's a hands-on workshop. I do apologize. They took away your tables. Um, so it's a very laptop situation. Uh, like literally, uh, laptop. Um, I hope you didn't bring your Mac Mini or whatever. Uh, but so yes, if you just go to ai.dev. Um, and I mean there's you can also go to ai.studio. You can go to

aistudio.com, but we paid a lot of money for AI.dev, so please use that. Uh it just it just redirects to AI studio. But um >> let me >> so AI.dev API key. >> Uh yes or on the corner left side there's a get API key and then API- keys is where you >> German. >> Uh yeah it's it's my personal account and we cannot change language. So uh you need only a Google account. So no credit card, no nothing. All of the things we

are going to do is part of the free tier. So if you go to AI studio or AI.dev and there's some like signin form you can like just use your Gmail. No worries we will not charge you. Uh and then on API keys uh you find at the top right corner normally something called API key create or create API key uh and when you do it for the first time you uh might need so similar for me uh I can import my projects or I can create my projects. I

can just click create give it any name. I mean we can call it uh I I workshop uh and then create project I can translate it to English. Okay, takes a few seconds and then you should be able to create key and this key will be used for the demos or the hands-on things we are going to do use later. Wait, it shows the API key. >> Yeah, I will delete it. So don't don't copy it. But you can like >> copy very fast.

>> You can use that key. You can like put it into your bash RC or set HRC file or later you can like directly inline it. Whatever you prefer. If you have one, you can use this one. And since we have a few more minutes time, we really want to make sure everyone who wants to follow along, take your time, create your API key. If there's an error appearing or something else is not working, feel free to raise your hand to

will come to you and we'll help you. And >> and yeah, just a reminder, it is a secret API key. >> So don't do what Philip is doing there. >> This is why I delete my key again. >> Yes. So we do get that a lot that people um leak their API keys. Mostly it's clock code that is like pushing their API keys to to to GitHub. So I recommend you don't do that. No, just just kidding. Just remember it is a secret

API key. Um, so treat it like a secret. Uh, don't share it with your neighbor, you know. >> Um, but yeah, do create that API key now. And we'll give you a couple minutes to do that. And while you do that or, you know, once you finished creating your API key, I'd love for you, you know, to just briefly introduce yourself if you want to and just sort of, you know, let us know what you would like to

get out of the workshop. Maybe there's a specific use case you're working on. Um, yeah, we'd love to kind of get to know you all a little bit as well. So while you create your API keys uh if you want to feel free to just you know shout out uh your name or nickname uh and sort of what you're working on what you would like to get out of the workshop. Yeah, with Raol from the Thursday podcast working for Koreas

and big fan of Gemma. Yeah, Gemma 4 and Gemini. I'm one of the few who are using it for coding and stuff as well by H& um I'm also running it on the classes actually. >> Oh, nice. >> And I want to see more of this, you know. >> Okay. >> And I want Google classes. >> Okay. Yeah. We'll we'll see if we can get to the glasses by the end of the workshop. Sorry. Yeah. If you have a seat to your right, can you jump in so

we can fill up on the side here? Makes it easier to be left. >> And while we are waiting, uh, we launched something cool on Chrome, which I haven't activated it, but when you go on your tap bar, click right, you can now move tabs to the side. And we have vertical tabs now. So, >> yay. So, more screen. That's good. >> Nice. Okay, cool. So glasses are you are you are you running what are you running on the glasses well

technically on the phone right software where you use which calls open clawization for >> two >> and then that's just using Gemini live kind of through the websocket on the phone right yeah nice yeah that's cool yeah vision claw if you haven't heard of that uh pretty pretty fun open source project um and I think you can run it uh sort of on the well now that Meta has opened up the SDK for the the Meta Rayban uh you can

actually hook in something like Gemini Life API uh into the glasses. Well, the glasses connect to your phone and then the phone actually connects to Gemini Life which is cool >> but uh it shows what will be possible. >> Yeah. Nice. Any problems creating API keys? Everyone has an API key. Should we check? >> Okay. Uh, anyone else? Anything specific that Yeah, >> Michael work for Get Your Guide in Zurich. Um, we're building like our

first kind of AI customer support agent. So, >> cool. >> Just interested to think in the general how you guys are doing it, comparing. >> Okay, cool. >> Nice. >> Last chance. Anyone else? >> Okay. >> All right. So we can start before we go into the hands-on session. We I have like 10 15 minutes slides um to give a bit of a background what we are going to use to build the first session which I'm going

to do is more on like the building an agent without any live audio input that's where to take over later and then we are going to building some very nice conversational agents. So um who of you has used the Gemini API to make an API call to Gemini before? That's a few. Have anyone of you used the interactions API? One. Okay. Two. Okay. At least some person. So the interactions API is a new API we launched in December and beta

which hopefully will succeed generate content soon. It's a unified API to use with models uh with agents and is much more aligned with I would say the industry. So much closer to what you are familiar with from open models with the chat completions API or from entropic or from open AI. Um and what we are going to do the slides then we build a coding agent like a small little clot code with reading running uh reading files writing

files running bash commands and then we have some time at the end if you have questions around it and then we do a short break toilet drinks and then tour will continue. We all have an API key. So as I said, we want to build an API which works for both models and agents. And when we launch the interactions API, we also launch deep research. So maybe you have used deep research in chat GPT or in the Gemini app where you basically

start off a query and then you get back a plan and then the model goes on and like does deep research for 10 15 minutes visiting hundreds of sites and um the API um supports both models and agents and it's very simple to switch between those. You basically either define a model which could be Gemini free flash flesh or you define your agents which could be deep research and we are working on it to for you to bring

your own agent or to define your own agent that you can customize all of these behaviors and it's the same surface. So we'll see later, but when you send a request to Nano Banana to generate an image, you can like basically chain those interactions to a flash model to do something else to Lura to have you like generate audio and uh or even to hopefully soon uh vo to generate you u video and the interface

is very similar to what you see from OpenI. So we now have like those uh content blocks basically. So every input you provide and output you provide is the same type. It has a type field which could be a function call, a thought signature, a text, audio, video, image which hopefully makes it for you easier to build with the Gemini API and it is less I would say Google branded, less protospaccific, less gRPC to make it

easier for developers to build. Um, the core primitives of the interactions API in addition to making it easier, we also introduced state on the server which will which we will use for building our agents. So we don't need to manage our loop and always send back the whole history. Very similar to uh responses API, you now have a previous interaction ID you can provide which basically attaches to the existing

history. So you can like just send a new input. Um as mentioned we have an agent with deep research and background true. So you can start your research can pull it or um soon use web hooks to get notified when your research is done. So you don't need to keep the connection open. We have the type blocks and then also we have the same like streaming pattern very typical for web development using SSE which also makes it hopefully

easier for you to build. We all support the built-in tools but we also now have support for remote MCP and I think two weeks ago we launched tool combination so you can now combine Google search with your own custom function which was one of the big features people were asking for years I think and now you can do this. Um and to summarize again the differences between so generate content is what we have today interactions API

is what we will have tomorrow we will have um serverside state management but you don't need to use it so if you say hey I want to manage my turns I want to manage my context I don't trust you or I need to do like context engineering I need to remove certain parts you can do this um you send can it's way easier to send new input basically we have the built-in agents we have also background support. So you will get asynchronous

execution. We all see with agents when you send a prompt that might take 1 2 3 4 minutes to complete and keeping HTTP requests or connections open for I would say more than like 10 seconds is not a very good practice. So you want to like use asynchronous calls to either get notified or like do polling uh when it is done and it is less proto oriented which I really prefer. um it's much closer to what people know from like the

the developer ecosystem and also a side effect of the state management is that the implicit caching for the API is much better. So for the one of you who don't know what is implicit caching. So when you send a request to the model, the model needs to encode all of your input tokens. And you can cach those encodings for a follow-up request to save cost. And cache requests I think are 90% cheaper for the input tokens. And when

you have to manage your state or context yourself, you maybe strip out line breaks, remove um certain parts, this breaks the cache. And using the serverside state, the server keeps the context. So the chances for your cache hit rate is much higher. And we see like two to three times better cache rates from like the the startups using interactions API today. Quick code example on what we mean with

making it simpler. So on the left side you have like the very protospecific oneoff input parts with inline data or text where the the field basically describes the type and on the right side almost looks similar to other APIs. I would say so should be much easier if you decide after the workshop to give it a try. Um then I guess all of you know roughly what an agent is. We have a brain or our model which decides what it

wants to do. Calling a tool generating text doing something else. We have tools which basically gives our brain hands and eyes to interact with the environment where it is in. We have the context. It's basically all of the all the model knows uh what it has to do, what it can do. if there are certain preferences, if there are certain constraints and then we have the loop which basically combines our model with

hands and tools and runs it until the model no longer calls the tools and generates a text. So some quick examples on how to use the API and then we go into like the the nice hands-on part. So basic chat usage with serverside state becomes very easy because we have our interactions create call. So we define our model, we define our input. What's the capital of France, we get back the output and then we can

just continue providing the previous ID and the model behind the scenes or like the server behind the scenes basically has our user input, our model output and then appends the new user input that you don't need to have like a client side history object where you append the user turns, the model turns and then the user turn again. This becomes very helpful when you build agents where you have a loop and always need to append new user

input and um as mentioned before that also works for agents and models. So we really want to build this unified interface where you can continue your conversations no matter what model you use. And in this example, we basically run a deep research request on research AI agents in 2026. And then we take the research output and just continue with the nano banana model to generate a visual for it. And it's like four lines

of code basically without for you to what's the context, how do I provide the input and hopefully makes it a lot easier. But as said, you don't have to do it. So like the input field also accepts the same array with ro user ro model model and all of the inputs. Um for two use it's also hopefully now much easier. We have a type function our name for our function which we want to use describe and then we have the

parameters the model needs to generate and then here's roughly what we are going to build. So we make our API call with the tools and then we check what the the output of the interaction is. Requires action basically means you as a client you need to do something. So the output generated some function call or some object which you need to react to. We iterate over our um output types. Check for the function call. Execute the

function. Append the result. send a new interaction until the model no longer decides it wants to call a function and generates a text or something else. Okay. Um the last time I did a workshop, we were all still coding manually. So that's my first time doing a hands-on workshop where at least I don't code much manually anymore. I'm not sure how you do it. So what we are going to do today is we don't code manually. We are going

to use your preferred IDE agent CLI of choice. I'm not sure how many of you are following, but um to make it easier, we created agent skills for our agents to use. So if you go to the Gemini, you can search for Gemini API Docs coding agents. >> You zoom in. >> Ah yes, sorry. Of course. Um I can also Can you see it? >> Yeah, I think you can also just Google >> I mean I can skills >> Gemini agent skills.

Okay. Um yes this one it should be des set up your coding agent with Gemini MCPN skills. I think that should bring us here >> and very different results >> really. >> Yes. Or if not you can go to the documentation and then on the left side in the getting started section there's a coding agent setup.

Are you are we successful? Okay. Um >> so one question should we install this skill globally or just for the project? >> You can you don't need to install it globally. And that's a good question. So how do you install? So we have multiple skills. We have the Gemini API dev skill. We not going to use this one. That's for the generate content API. If you want to use that API or if you are familiar with it, go for it. But we have

the the Gemini live API. That's what tour is going to use later. So we also don't install this. But then we have the Gemini interactions API. And here you can either pick the the first command or the second command depending on what you want. And then like just copy it uh open your workspace um where you're working in. And then I already did it, but you can like add the command npx install and then you should get a wizard asking you

to install it. There are many pre-selected. Don't get confused by it. This just means that all of those agents are compatible with the agents folder. So you might have agents/kills/gemini interactions API and in there we have our skill. Yep. I let me also uh wait. So I tested with cursor and anti-gravity and also Gemini CLI. So if you are using one of those three, you're good. If you're using cloud code, I

think it should work as well. I'm not sure if they follow agents best practice. If not, I mean I'm sure you can. >> They invent invented it, right? Like the skills. >> Yeah, the skills, but I think they only look at claude. Uh I think >> look at agent >> but I think it installs into skills. >> I don't know. Okay. So >> yeah. >> Okay. Yeah. Question. >> Uh you show two different commands. One skills and the other one context 7 or

>> Yeah, they both both work the same. >> What but what's what is context 7? >> Uh so context 7 is I think a product based out of upstach. So context 7 is has an MCP server and now a skills CLI which you can use to get access to like skills. It's like a public repository. So and skills.sh is the same from the versel team. >> Okay. >> So it's like and it it works both works on GitHub. So the Google-gemini-gemini

skills is a GitHub repository and the GitHub repository includes all of the skills we we documented. So you can also go there and find it there. There are also the the deal in instance commands and it makes it much easier than cloning it and making sure you have it in the right directory. And then what we can do is um to make sure our skill works we can just like ask our agent uh what skills can you

use and then it should if it if you have installed it correctly you should see yes we have our specialized interactions API skill. So anti-gravity here picked up our skill in the agents/skill folder. Okay. How are we doing? >> Can you zoom in just a bit? >> Zoom in more. >> Okay. >> Better. >> Yeah. >> Um I was using telegram with my result of this being run on the system. So >> would I have to have it run?

>> No, you can like you should be able to do it on like your open claw kind of stuff if you tell it install the interactions API and then >> just the final product of the workshop. Will it run? >> Yeah, it should run. It's a Python script. We are going to execute it later. >> So because I'm only running should work. >> Okay. Any any difficulties installing the skill? Any questions what a skill is? Everyone familiar with skills? Okay.

What we can do maybe uh to give you some uh insights on what skill we created or what it contains. Right? The importance when creating skills is it should be either something the model cannot do reliably or if you have some personal preferences on like how to do a certain workflow or I don't know you always need to run tests using bun or something like this and what we did with our skill is we made sure that the agent is aware of

which Gemini models are available. A common issue we saw before that is like Gemini always used Gemini 1.5 which is no longer the latest model. Um we also included the agents here. uh we have some like very high level information on how it works but we did not include like all of the documentation. What we did instead is you should see yes uh a link to our documentation which is available as markdown. So instead of the need to

always update our skill with like for example we added a new feature to interactions API to combine tools we would have needed to update our skill and then every one of you also need to update your skill to be able to use it and then we are not making a lot of progress in terms of like knowledge cutoff. Instead we provide the the information as part of the skill. So all of the agents now have like web fetch

tools. So they can query the information based on the skill and then like we only need to maintain like the documentation which is mostly up to date. Yeah. >> How do you find that work like efficiency? >> Sorry. >> How do you find that works with like tooling efficiency and all that sort of thing? Do you find it like it having to go and fetch the page to >> I mean it it normally you would provide

it as a reference on your local file, right? So it either needs to do a read file call or a web f call which is the same I would say in terms of like cost and it works very well. Okay. So what we are going to do as a first example since we are not wipe coding uh we want to build something more substantial we not just say build an agent we want to be more specific. So we want to build um create an agent class with a

constructor and a run method. The constructor creates uh Gen AI client. So the Gen AI client is what we are going to use to call our model. We also need uh defines model and we also need uh global previous interaction ID and then add the main method to run an example. uh do all of that in uh workshop pie. Okay. So, and as we can see the model in this case or the agent as a first step read our skill,

analyzed our main file is implementing the skill. Okay, it checks. It should probably fail. Yes, because I'm using UV, so I stop and I tell it use UV uh from the workspace and and then we let it generate. We Okay, it checks if we have installed the library. We have. So maybe in your case, the agent still tries to install Google Chenai. If not, you can do it yourself with like pip install or uei pip install

um google- geni and then make sure to okay so we have our starting agent class. We have our genai client. We have our model ID. It defaults to Gemini free flash. It would never have defaulted to Gemini free flash if it would it hadn't read the skill, right? because then we were stuck with Gemini 1.5. We have our run method which calls uh makes our interactions.create uh call. We have the input text. We have our um previous

interaction ID. We set our new previous interaction ID and then we return the text and then nice as a main example um which we will run in a bit. We create our agent. We have turn one. So my name is Phil and then the agent uh runs it and then what is my name to then we can check if our Gemini created Gemini agent uh works with uh multi-turn and our interactions API. You might see a warning similar to

the one I got here. Uh interaction usage is experimental. That's as we are still in beta. We really work hard to get the API out of beta to make sure you can use it in production. And our call was successful. Hi Phil, nice to meet you. Okay, maybe we weren't successful. I don't actually have a name. So what is my name? Maybe we should check. Did we do it correctly? I mean, my name is maybe a Okay, that's still

the call. Sorry, I asked it. What's your name? I mean it's a language model for trained by Google. It makes sense. And what is my name? Your name is Philip. How can I help you? So yeah 3 flash as a coding model. >> Yes. >> I mean it it it works really well if you are providing good instructions with good skills and good context and don't expect it to I don't know like cure cancer. Like if you have a very good

understanding of what you are trying to build Gemini free flash is like very fast. I mean it didn't take much long. It didn't consumes credits, right? Every one of us is somewhat token constraints at the moment and it it works really well. Okay. >> Use it for agendic use. Yes. But for planning and coding. >> Yeah. No, it works. I mean we will going to use free well. I mean like it also asks like if it wants to run. So we are

closing the loop even like with Gemini free flash. It tries to run our script to make sure it works. And then we will continue in a bit. How are we doing? Anyone making successful calls? Yes. >> Okay. Perfect. >> Background. >> Okay. Any any issues? Any errors? Any questions? >> Yeah. >> I'm using TypeScript. >> Okay. >> It it works. >> Yeah. >> Nice. Great. >> Works for me too. >> Mhm. Awesome. Even coding on a phone.

So, okay. So, normally the next step for our agent, right? We now have our like very basic run. We can chat with the model. Now we need to add tools to it and we want to build some kind of a coding agent. So first tools uh we are going to add is a read and write file tool and we just continue in our uh main agent thread. It's like okay uh next we need to add a read file and write file tool. create

the create a basic Python implementation and also the JSON schema definition. So when you use function calling or tool use right we need to create a JSON schema which we provide to the model so the model understands what it needs to generate. Once it generates that schema, we also need to have some kind of a code implementation which we can then run on the client. So we ask it to create the Python implementation and also the JSON

schema uh and a map to for the key and key function schema. Okay, let's see what it will come up with. Okay,

it's cheating a little bit. So, I have like a solution folder and it looked up the implementation implement. Yeah, I mean that's why it's still important to like check your wait I can like it it it found like the solution and then it was like oh I got this solid Python example in solution.h agent to guide me. The task is implement read file and write file. >> Yes. So what we got back is we have two

new like very basic very very basic file implementation. So we have a read file tool with a file path which uses um Python syntax to open it to read it and we have a write file tool with file path and the content and writes it. And then we have our read file schema. Um, reads a file and returns the content. Write file, writes the file and returns the content. And it made some updates to our agent. So what did it change? Okay, our

input is now a text uh string and a list. Makes sense since we now need to return a function call. We check what do we do? Okay, we create a tool definition for our model which is the T schema. So that's our tools map schema. And then we have our loop which you might be familiar with from the slide I showed. So after we run our request, we check the interactions output. So the interactions outputs include all of the

events generated by the model. And since Gemini is a reasoning model, it also includes for example the thoughts and the thought signatures which we need to return since we are using the previous interaction ID and the server side state that's done by us and we only need to check okay do we have a function call we have a nice debug so we can check it and for our outputs or function call we check our tools do we have our tool or

not I mean maybe the model wants to edit a file but we don't have edit a file tool we would catch it here it calls our model and then it creates the tool results. So for function call we have a function result that's also part of the change. We really want to make it easy. Um we will see later when we use Google search there will be a Google search call and a Google search result to have very the same schema and then we use

recursion. So if we have two results we basically call ourself the selfrun method again. If we don't have two results, we returned the interaction text and it also updated our example. Write hello from the agent to a file named hello text and return it back. So we I mean the changes roughly look good to me. We can try and run it. So u run python workshop main. What do we get? We get our tool call

with write file. We get our two result. We get a read file call again and then the final agent response. The file hello agent text was successfully created with the content. Agents are not only like singleton, right? Maybe we wanted to respond. So next step is basically very ambitious telling it I want to have a continuous I don't know stood in implementation to test. Let's see it. So let's see where it will continue.

No, I hope at least it should update our main function where we have an input a while loop basically waiting for the input using our agent. So, yep. So, we have our user input uh and then we have we always continue with our agent.r run method which then inside the agent runs it in a loops until there are no tool calls anymore. And if there's a result, we basically get back our response. Okay, let's quickly wait. Is it too fast

or are we still on track? Roughly >> it's fast. >> Okay. I mean we will share the code later. Um also very happy to answer questions. Uh we have many like blog post and examples of that online. So you can if you are interested in like rebuilding it later with less fast um but I I try to be a little bit slower but I also want to give to enough time to have you speak. So what we can do now since we or like our agent implemented

our like while loop to um to to provide input we can say something like hello right normally we should now not do any tool calls because hello is like yeah our agent correctly kind of understood or Geminina in this case understood hey hello is nothing I need to solve with a read or write file to write. So I can say hello, how can I help you? Can you write or maybe can you create uh CSV with a thumbs up

might take a while a bit. So, it does the thinking and it does the function call and okay um certainly here's a CSV file blah blah blah. Um okay, can you write it to disk?

Uh yes, I can if you wait maybe our model is not having our tools. Let's check. There's the tools map. It does. Why is it not using our tools? What tools can you use?

>> Okay. It has a read file. Yes. Maybe we are we're not explicit enough. And what we can do to improve this in one second is we can add a system instruction to tell the model hey you are a coding agent. You can use tools to write and interact with the okay there we got our tool call write file with our CSV. Cool. Since we saw our mistake, we can now tell the model, hey, add system instructions for the interactions API call and add an

example prompt for a coding agent. Okay. And what's really nice now since we uh loaded the interactions API skill in the beginning, the model still has the awareness of okay, how do I add a system instructions to the interactions API and what I can guarantee you is that the Gemini free flesh has never seen any code of the interactions API because the model was trained be before we even released the API. So all of the work we

were doing so far is based on like the skills and like the the coding infrastructure and hasn't been part of the the training. Okay. So what did we get? Um okay we can provide it on the run command or we have one when we create it. That's good. And okay coding persona you are an expert software engineer and helpful coding assistant. You have access to the local file system. Okay let's accept it. Let's start our agent

again. Let's say hello.

Okay. Hello. How can I help you with your software engineering and coding tasks? I mean, definitely better than what we had so far. And what did we send before? We said, can you create a SVG with a thumbs up? So, can you create an SVC with a thumbs up? And now let's see if it calls. Yes. And now at this time we got our write file tool call. And then also we got a hey, I have created a thumbs up SVG file with a simple line

art thumbs icon. So um can I >> I think it should. Yes, there we go. >> We got a thumbs up icon. Cool. Um, and of course, what's missing for a coding agent right? We need to get some bash tools. That's now not part of the solutions folder. So, let's see how we will get our bash tool. Now add a similar run command tool that allows the model to execute bash commands. Okay. Creates an implementation blend.

You're asking >> Phil I think there's a question can you >> I say like I was just testing it does a little bit like try to do like >> even with >> okay so we have our run command which uses a subprocess which in this case I guess is okay we don't care too much about security for this example and then our output is a stood out. Um, works. Edit. We have our run command tool. Yeah, it even updated our system prompt.

And now let's stop that. Let's clear that. Let's run it again. Um, any suggestion on what we should test? >> Use a banana to create an image. I'm not sure that will work because we don't have any skills or any information for it. >> Time. >> Oh, >> get the time. Tool call. Run command date Wednesday, April 8th. >> It looks good. >> Um, yeah. Cool. That's our small little coding agent. >> Delete all files. No, I mean let's not

do this. >> Any more questions? Any more ideas? We have like roughly five to seven minutes. Yes. >> General question. So because the state is kept in the cyber. Yeah. Is it possible to like for the history? >> Yes. >> Yes. So that >> um what you always can do so what we are doing here is right we always use the previous interaction ID from the previous term. So we basically stack it and you can always go back to

any index in the stack and branch from there. So if you would keep the interaction ids on your client side, you can always use those to I don't know branch out and like I don't know have like a first um prompt on like do basic web search and then like use this as like a base for like five parallel requests doing some other work and you can always get the context. So we have an interactions.get method

which you can use to retrieve the interaction and then also get the previous interaction ID. So you can basically go back until the beginning and get all of your state if you want to save it for later. And the default for those interactions being stored on the server for free tier is one day for paid usage is 55 days at the moment. >> Yeah, you had the question. >> Sorry, >> you answer. >> Okay, perfect. more questions. Yeah.

>> Does it mean then it can have infinitely long context window? >> Uh no. So once so Gemini models have a million tokens context what would happen now if you reach that you will get an error but we are working on context compaction techniques but it's easier said as done and um it's still something you currently need to maintain on on your client side. So when you say that it will retain the server will retain

for one day. So that means every day it resets to zero and then >> no no so when you send a request you get an ID the interaction ID uh and the interaction ID stores your input and the output of the model in the free tier the input and output and the ID is stored for one day. So meaning if you send a request now and you continue 8 hour later from that point the state or like the context is still available. If you

would send a request tomorrow, it would basically say cannot find um requests with the old interaction ID because it basically is pruned after a day. But if you use the paid API key, it's stored for 55 days. And um the interactions API is also coming to Vert.Ex. And I think there might be a little bit more flexibility in terms of um how long you want to store or customize it. Yes. Is there a specific API to reward context

if you want to do context on client side? >> We don't have one yet, but hopefully soon. >> Yes, >> give an idea. You could have the API joke being spoken out with the especi >> the especi tool to actually speak the joke about APIs mentioned in >> and we can also use Gemini which has a TTS model which can speak to but speaking and listening I mean to will show many many cool things. Any questions regarding the interactions API

and the small little agent? No. Okay. Then you get 8 minutes. >> I do five minutes. >> Okay. Five minutes. >> Break and then we'll be back here >> with >> to make your agent talk. >> Yes. Cool. >> Cool. Thanks.

>> That worked really well. >> Nice. Yeah. I used the old one and super happy that now there's a new one version was 2.5 before. Yes. Yeah, it's it's been a while. >> How much better? >> Yeah, much better. >> Much we didn't even pay him for it. >> Big upgrades. >> Big upgrades. Yes. Um >> yeah, maybe uh I know there's a couple more minutes, but >> can I ask a question while Caching. >> Caching. >> Yeah.

>> Yes. Input tokens. >> Yeah. >> Is that those conting?

>> That's a good question. We probably need to find Philillip to answer that. I actually I actually don't know. >> Phillip caching question. Uh the input tokens >> y >> what was it?

>> It is not on an interaction level. It's more on an like object level. So, >> for example, when you provide an input like no interaction ID, first input PDF 4,000 tokens and the text input with 10 tokens and you do an follow-up interaction call, maybe only the PDF will be cached and not the other like the short text and then if you do another one, maybe the PDF and like the follow-up turns will be cached. So, it's

like more on like an object level. But since you I mean, how is it? It's very easy to make a mistake in caching if you like even the slightest change in your prompt removing whites space line breaks will break it. So like having this rely on the server to keep it. It's more guaranteed that it's secure and it could be as easy as hey my user says there's an empty line break at the end. Okay, I remove it and then I use that history

again and then it falls apart. >> You do it right. Ideally, every conversation, this previous part of the conversation is captured. >> Yes. Uh, optimally. But I mean, it depends on where your request kind of hits it and like how fast you follow up, but the cache rate should be pretty high. >> Cool. Maybe uh to kick things off, we can sort of look at one of the examples that that we can build uh with the the

live API, the new model. So this is now uh Gemini 3.1 Flash life which came out two weeks ago I think. Um very exciting. It's been a while. I think the previous 2.5 native audio model was December. So it's been a while. The reason being we did kind of major underlying architecture. we work to, you know, ideally lower latency, you know, better scalability in the in the future as this REMs up. So, uh, that's very exciting.

And then, you know, in parallel, we're working on bringing, uh, the life API to the interactions API as well. Um, so that's something that Philip and I are working on at the moment. Not there yet. So, we still have to use the, uh, live API for now, but let's do a little demo. And so this demo uses the life API in combination with LIA 3. Uh so on the Gemini API have have people played with LIA? So the new LIIA model is actually a

music generation model. And so LIA 3 can now generate songs uh you know including songs with lyrics. Uh so this is the clip model which is kind of a 30-second uh clip generation. Uh but then also we have a full song model now where you can generate kind of full full songs. So the idea is that we have our conversational agent which is kind of the DJ that you're interacting with and then that DJ has a tool call to generate music,

right? Um and so you know I so I'm originally German but you know growing up I learned kind of English through Harry Potter and BB BBC radio one. Uh, and if you remember back in the day, you could like phone in and like wish for a song. And so that's sort of the the the idea of the experience here, right? Then you're on live jukebox. What absolute banger are we cooking up today? Tell me, what genre are we leaning into?

And what sort of vibe are you going for? That's >> Can we get some sort of high energy German um technos schlaga about the AI scene in the UK? >> German technoslagger about UK AI. That's absolutely brilliant, mate. Proper Radio One style. Any specific lyrics or themes you want crammed in there? >> Just surprise me. Let's go. >> Right, you beauty. Let's get those speakers rattling. Prepare for a burst

of machine mayhem. Here comes German technoslagger about the UK AI scene. Let's go. >> In London town, the future's bright and keen. The cleverest robots that you've ever seen. The computers wear a proper bowler hat. And the androids all enjoy a lovely chat. They're drinking builder's tea with digital grace. A happy British smile on every metal face. OH, VUNDERAR, THE AI IS SUPER GORGEOUS. YEAH, SUPER

GORGEOUS.

YEAH. Um the the TPUs enjoy when you clap for them. So, um appreciate that. Uh any anyone have any idea for another one? We can we can do one more. Just shout it out. Any languages, any genres? >> We have a nursing >> aur nursing song >> in Swahili. >> Swahili. Okay. >> Right then. Welcome to the live jukebox. You're on air with me. >> Can we get a nursing song in Swahili, please? A nursing song in Swahili. Brilliant.

That's something we don't hear every day. To make it an absolute banger, what sort of vibe are we going for? Upbeat and celebratory or something more relaxing and gentle? And what specific bits about nursing should we squeeze in? Let me know and I'll get this track buzzing. >> Yeah, techno hardcore about

>> techno hardcore and swuah about nursing. Wicked. Prepare to blast those speakers. I'm dialing that in now. Get ready for a total banger, mate.

I never know. Well, we can feed it in Gemini to uh you know get the audio out. Okay, that is the live jukebox. DJ uh DJ you uh if you want to it's it's on so this was built fully with Google AI studio uh so it's it's kind of a little vipodus um demo I've published it in AI studio as well so you can try it out uh you will need a paid API key for this one because the music generation actually requires a

billing account um so if you have you know an account with credits you can use that uh for example uh cool yeah Gemini uh 3.1 flash life. You know, benchmarks, obviously, benchmarks don't really tell you the truth uh as much. They are great for benchmarking things. Uh the real world, especially in kind of live audio, does often look a bit different. So, um you know, ideally, we just try it out ourselves. So, Gemini

3.1 Flash Life, it's the model that is now in Gemini Life in your phone. So if you're using Gemini app uh on your phone um you're talking to that model as well as I think search life has it now in there as well. So if you're talking to Google search uh I think that's the same model and then you can build applications using this model on the life API. So the life API is a stateful kind of websocket API. um you

are able to send real time text, audio, video feeds uh to the model. So audio you're sending in kind of you know buffer chunks so of the the real-time audio you're streaming that in uh video you can stream in uh at a maximum frame rate of one frame per second. So this can be you know a camera feed, this can be uh a canvas. So uh it could be like your your your screen share, right? So you could share the screen with the

model. So for example, uh Shopify is using this for uh Shopify site kick um where it's actually kind of like a tech support walking you through, you know, if you're like, "Oh, how do I set up a custom domain for like my Shopify store?" It would basically like talk you through how to do that and it can see kind of where you are on the screen by sort of ingesting the frames of the screen. And then in return uh the

websocket gives you kind of real-time events back. And so these are basically streaming back audio buffers. Uh and then also you can get the audio transcription. So that's kind of the text um of it. And then we have um tool calling built in. So Google search grounding is built in by default. So if you need kind of real-time weather information, you can access that as well. Um yeah, some key features. So

what's really cool about this model again it's it's kind of native audio model. So what that means is we're not going through text. So it's kind of not a cascading pipeline where um you're transcribing the text running the text through an LLM and then generating speech. Uh but rather the model itself um is you know going sound token to sound token and the intelligence is kind of baked into this audio model. Um so

it's based on you know Gemini 3.1 so decently intelligent. Uh you have different kind of thinking levels that you can enable. Um and so the great thing with that is kind of the multilingual support. So it's I think 97 languages that are kind of supported in preview uh at the moment which uh and the great thing is because it is kind of a you know native audio model it can actually it has sort of the audio

understanding of of Gemini built into it. So um it can understand a mix of different languages. It can you know sort of denlish for example which is like a mix of German, Deutsch and and English, right? So it would be able to sort of naturally switch between kind of different languages as well which is really great. Um yeah, barge, you know, obviously there's kind of automatic um voice activity detection sort of built

into the model so you can interrupt it. you saw it earlier the DJ you kind of trying to have a conversation but we're trying to get it to to you know use the tool tool use is the other big thing um so major improvements in kind of tool use and instruction following here with that model um and so you can build some some really cool things with that um so obviously we currently only give you uh a websocket API so that is kind of a

downside if you use something like GPC real time before you know you get a direct web RTC um kind of infrastructure which which can be helpful. So we have partnered with you know a lot of uh sort of integration partners like lifekit, pipecat uh software mentioners uh in Poland. They they built a great service called fish gem uh vision agents vox implant. So these partners have integrated kind of the life API directly

and then give you sort of easy web RTC integrations if you if you um you know want that or need that kind of for your system. Um yeah let's let's try it out. So you can try it out yourself. Uh, and it's going to be interesting if we all try it out in this room at the same time. So, uh, we'll see how that works. But, uh, again, AI.studio or AI.dev and then slife. Uh, you can try out the model and so you

can, you know, ingest your webcam here as well. Uh, so we we can give it our webcam feed. Um, allow this time. Uh, and then, you know, we can send text as well. So, we could send like, uh, how is my outfit? Uh, so in this case, you know, I'm not ingesting any. >> You're wearing a green jacket over a blue t-shirt paired with a black cap. The combination looks casual and comfortable. Is there a specific

occasion you have in mind? >> Yeah. Okay. So, um, you know, that obviously is a bit further away from our upbeat sort of British, Australish, Australian, uh, live DJ. So, what we can do is we can, um, you kind of adjust our our voice. So through the system instructions. Um now in terms of the bass voices, we don't have that many. There's kind of 30 different bass voices. >> Got a project in mind >> and they are you know fairly generic

sort of but because you know Gemini has very deep audio understanding. What we can do is actually we can modify the voice through prompts through system instructions. So what we can do is actually we can give it um kind of a system instruction here for example and we can just say okay speak in a friendly Irish accent, right? Um and so now we have that bass voice puck and uh speak in a friendly Irish accent.

Hey, can you hear me? Well, hello there. Loud and clear so I can. What can I do for you on this fine day? What do you think of my outfit? Well, now you're looking very smart, so you are. That green jacket suits you well, I must say. A grand's casual look. Were you thinking of heading out somewhere? Uh, no. I'm just here at the AI engineer. Okay. Anyway, so I I realized I didn't put on So, what I wanted to

show you as well is um there's grounding with Google search. So what we can do is um you know obviously the the model itself is trained to a certain knowledge cutoff date and so um you know if we need kind of real-time information like this gorgeous weather that you know no one would actually believe us the model wouldn't believe us you know if it if it didn't have um Google search grounding but now you know we can we can have

Google search grounding we can have different thinking levels as well so um no thinking is actually very minimal thinking. Um but it means you know the model will respond faster. It's kind of lower latency because the more thinking we have obviously the more thinking steps are kind of involved and um it'll you know increase the latency. So you can see in the benchmarks as well there's kind of thinking high uh

thinking low uh sort of different thinking levels. Um, but so now if we turn on kind of the the Google search here. Oh, hello there. What range of shenanigans can I help you with today? Anything at all? Just give a shout. >> Uh, yeah. What's the weather right now in London, actually? Well, now it looks like it's about 9° and mostly cloudy in London right now. Might be a bit chilly, so you'd be wanting a jacket for sure. Anything else

you need to know about the goings on over there? >> What? What are you talking about? Can you check again? What date is today? >> Ah, apologies there. I seem to have gotten ahead of myself. Today is Wednesday, April 8th, 2026. Is there anything specific you needed to know about today? >> Yeah. And now look up today's actual weather. >> Right. for Wednesday, April 8th, 2026 in London. You're looking at temperatures

between 5 and 13 degrees with a decent chance of rain, so don't forget that umbrella. Anything else on your mind? All right. Uh here we are. It looks like I didn't pray to the the demo gods. Okay, there seems to be something going on. I wonder if we messed up the UI there. Uh it should it should work a lot better than that. Um I think the Google search grounding for some reason isn't isn't working. So but what we can do now

is we can obviously try it out ourselves in an application. So the easiest way we could do that is you know like the live jukebox life jukebox DJ um we could use Google AI studio to kind of v code our integration. Um so we have this pill here which is called uh add you know voice conversation real time voice with you know Gemini life API uh and then we could say um build kind of a multilingual interview assistant that

allows me to you know train for interviews in different languages uh like German and English and Spanish and you know what have you uh And so we can now kind of fire this off. So this uses Gemini 3 flash preview. Um it is limited to uh kind of JavaScript full stack um environments at the moment. So I think you can choose between kind of next.js Angular. Um there's like XR building blocks as well if you're building for for kind of

glasses um sort of web VR experiences. Um, so you know, feel free to kind of fire one of these off uh right now or you can also clone uh the live jukebox DJ that I shared with you earlier and you can try that out. Um, it'll it'll take a little time uh and you'll hear like a little chime once it is uh ready. So in the meantime, what we can do is uh so if you go to the Gemini Life API docs, Gemini Life API,

uh there we are. So, you know, we've done this. We tried out kind of the life API in Google AI Studio. Um, we also can use the coding agent skills. So, uh, Phil showed you this earlier. Um, we have dedicated coding agent skills also for the the Gemini Life API. So, you can install that. It'll help, you know, your coding agent integrate the life API um more easily, more quickly. Uh but then also you know

we have good old example apps on on GitHub which can be very very helpful. So what you can do is um you can clone these example apps. Uh so in GitHub you know you can uh like you do in GitHub right uh you can clone this. So, we'll open kind of new terminal. And yes, feel free to follow along. Do that a bit bigger. Uh we'll make a new directory. We'll call it AIG uh Europe. I like that they call it Europe, right?

But it's uh I mean, I guess, yeah, the UK is still part of Europe, just not the EU. Fair enough. Um, and so we'll we'll go in there. Uh, and then we'll just do a git clone um of our app. Uh, and so now we have our app in here. Um, so there's actually a couple different examples that we can use in here. Uh, so if you're using anti-gravity, there's a handy agy command to uh open your examples in anti-gravity.

Uh and so we can you know look at our different examples here and how we kind of need to set that up. So we have you know two different scenarios. So the Gemini Life Genai Python example uses the Gemini Life API on the server. So it creates a websocket connection from your server to uh you know Gemini life API and then on your front end you basically set up a proxy um to proxy the websocket connection to

your client side right because your your browser window is kind of your client and so that is what is capturing um your your uh audio feed your video feed and so in this example we're just using fast API Okay. Uh, and we're basically, uh, just setting up kind of a web socket here, uh, that our client can connect to, uh, and then we're basically just receiving sort of our, um, you know, audio cues, our video cues from the

client site. Uh, or, you know, our text input queue as well. Uh, and so we're receiving that. We then setting up um, a live session. So um we're using our Gemini client. So we kind of abstracted sort of all the life API stuff into this Gemini life file here. Uh and you can see like starting the session we're basically setting up kind of our life connect config. Maybe I close this for now. Uh so you can see that um we're

setting up some system instructions. So that was you know earlier kind of said a helpful assistant. We also said kind of speak in a friendly Irish accent for example. Um, you know, this is where we put our uh sort of system instructions, our guardrails. We can, you know, make that pretty long in terms of covering sort of what we what we want. Uh, and then we can define kind of our tools here. Um, and then we're basically

setting up our um, you know, session and uh, our session sort of is, you know, the websocket session. Uh, and then we're just receiving our audio and video cues from the client side. uh and proxying that through. So that is kind of one approach. That's sort of the server to server approach. Um and you know we're just using kind of UV here. Um so if we're setting this up for the first time, uh we can go into So this is

our Gemini live um Genai Python uh example here. So we can set up uh our virtual environment. We can then um activate our source here. Uh we can install our dependencies. Uh okay, I might have this is a a fun part of uh uh a Google laptop security. Come on. All right. Just look away. Don't look. Don't look at that. Um and then yeah, install our requirements. And so we'll need uh an API key. Uh so

the API key, you can see kind of here uh how the config configuration is. So we basically just need our Gemini API key. Uh and we need to set up uh an environment variable for that. So you can see we have an example file here. Not a lot in there because it's basically just that. So we can copy our env.example into ourv uh file here. And then do you remember how to get your API key? Where do you get your API key?

>> Yes. AI.dev. There we are. Fantastic. Love it. Um, okay. AI.dev. Uh, so that is where you get your API key. Uh, I think I have a couple API keys. So, it takes a little while to um load them here. Uh which one is maybe we'll we'll use this one. So once you've created your API key uh you can copy the API key from here. Well actually maybe I should create a new one because later I'll need to delete it. Uh so we'll say

AIG Europe. Uh we'll we have a couple projects here. We'll just use we'll just uh which one which one we using? Too many projects. Okay. We'll just use this one. Uh, and so now I really don't like us actually returning the clear API key here. I think we learned something today. Um, okay, we save that. Uh, and so now we have sort of our API key set up. And now what we can do is, uh, we can run our demo. And that was just the

main.py. And so now our demo will be up and running. on localhost 8000 here. And so we can see um it's just kind of a basic sort of demo. Uh and when we connect top of the morning to you, I'm Gemini live. A little demo of what this API can do. Why not try out some fun features like hearing me speak and different apps? Can >> you cancel me saying? >> Ah, I can see you. All right. You're sitting there with your handsome face

looking straight at me.

Oh, that was that was this uh I was asking. >> Sorry. >> Oh, yeah. Yeah. Yeah. but it didn't transcribe it. >> Um, all right. Uh, we're finding out a lot of things here, uh, to improve, which is nice. Um, but yeah, so what we can see is, um, so this is, you could actually notice that the latency is a bit worse because we're actually having that jump from our client to our server. Um I would love to blame the Wi-Fi but uh so

with the serverto-s server setup you just have that additional latency of sort of going through um your client. So what we can do as well is we can go directly from our client to the server. Uh and so this is the other example that we have um which is this one here using ephirmal tokens. So uh for effirmal tokens we can just kind of look into uh the setup here. Uh very similar. We'll just go uh back uh

actually let me get a new terminal up here. So we'll say uh effirmal tokens. So our effirmal tokens are basically shortlift tokens uh that we generate with our API key on the server side and then we send that effirmal token to our client. So you know our phone, our browser uh to then initiate the websocket connection directly from the client to the life API. Uh again similar setup here. We want uh a virtual

environment. Uh we then uh activate our virtual environment and we install our dependencies. Uh we also need our uh API key uh again. So I think what we can do is just use the same one. So we'll copy maybe just copy this one here and then paste uh paste that in. Is it big enough? I don't know. Can people see that? Maybe we'll zoom in a little bit more. So now we have our key here um as well. Uh and so

now that we have our dependencies installed, uh we can run our server. Uh and so our server here, um we can look at the server real quick. So this server is basically just uh a very you know slim sort of back end that just has our Gemini API key uh and then it generates an effirmal token for us. So sort of um ephirmal token is currently on the v1 alpha API. So you'll need to use actually a different API uh at the moment for this.

And then you would pass in kind of this expiration time. Uh because ideally, you know, the token should be shortlived. Uh so should the token ever leak, you know, uh it shouldn't be too costly because it'll expire um pretty soon. So there we are. That's our token. And then we return our token back to our client. So on our front end, we then have our Gemini Life kind of integration here. And so this is an example of just

a pure websocket integration without sort of any SDK. Um so you know if you you can use kind any sort of websocket framework um here and you can see sort of you know how all the the different sort of raw websocket events um are handled. Uh and so you can see here we have um you know this is kind of our websocket uh API. So here we need to use kind of the v1 alpha. Um and then this is the by so birectional. Um you know we're

streaming in both directions. Uh and here we we pass our access token which is our shortlift token. Uh great. So what we can do now is now our server is up and running. Uh so we can see um this beautiful interface here which was uh handcrafted. um you know, no agent involved in the creation of this one um back in the day. And so we can just see kind of all the different um knobs here that we have. So we'll try

this kind of Google grounding as well. And hopefully it was uh just a thing we need to fix in the UI. Um here's our flash life uh preview model. So that's 3.1 flash life. Uh and then we can uh connect here. And so we see kind of the the server events. Uh actually let me maybe uh do that again. So we say enable Google search grounding connect. So what we can see is kind of our websocket uh setup. So if we look into the

network, we now see we have kind of this um websocket connection here. So we see we have our access token. So our token request to the back end. Actually, let me see that. Okay, so you can see we're just getting our token. So, um the response was just our O token and when it expires, uh what we sent in terms of the payload, where's our payload? Okay, actually that was no payload. Uh yeah, we're we're just getting a token

back. So once we have our token, we then set up our um websocket and so we can see our messages here. So basically the first message in our websocket um we're sending our setup uh configuration. So you see we're you know sending our model as like Gemini 3.1 flash preview. We have some real time uh input there. We have the tools. So hopefully now the Google search uh should work. And so now what we can do is we can um start our

audio. Hey, can you hear me? >> Yep, I can hear you loud and clear. How can I help you today? >> Um I'm in London right now and I'm wondering, do I need an umbrella? What's the weather today? >> I'm not getting the current weather for London right now. Sorry about that. Your best bet is probably to quickly check a weather app on your phone or search online. That'll give you the latest on rain. >> Oh, you're killing me. Just use Google

search. >> My apologies. I seem to be having some trouble pulling that up right now. I know that's frustrating. You can get the forecast easily by just asking your phone or searching online. I'll try to get this sorted on my end. >> Gemini, why are you doing this to me? That's just sad. I understand your frustration. Sometimes technology gives us hiccups and I'm sorry I couldn't get that weather for

you right now. I'm always learning. So hopefully next time will be smoother. Was there anything else I could help you with? All right, that was painful. Uh I do apologize for that. Okay, so something is definitely going on. That is um not good. Not not nice. Um, let's see if we have more uh luck with the custom tools. So, we're also passing in Do we pass in some custom tools or is there actually some issue with our

uh

Hey, can you show me a hello world alert? There you go. A hello world alert has been displayed. Anything else I can help you with? >> Yeah. Can you change the background uh of the page to green, please? >> You got it. The background color should now be green. Let me know if you need anything else. >> Yeah. Can you tell me what's the weather right now in London? I understand you're asking about the

weather in London, but unfortunately the Google grounding, but for some reason it's Yeah. So, with the Google grounding, it should work. So, I I wonder if I messed up something. >> No worries at all. The weather information isn't something I can grab right now, but if you have any other questions or need help with different functions, feel free to ask. Let's try this again. Hey, can you hear me? Ah, yeah. We need some audio. Hey, can

you change the the background back to white, please? >> I wish I could, but I don't actually have control over your display settings. You might need to look in your devices settings menu to change that. >> Anything else I can help with instead? Oh, no. Sorry. Off the page. The the background of the page. Back to white. >> Oh, I see. Sadly, I still can't change that for you. Those appearance settings

are part of the website or app you're using. >> Oh, yeah. You're right. Um, no, but I thought Okay. Well, disabled custom tools. That shouldn't be the case anymore. All right. Um lots of work to do but uh so yeah this is sort of how you can um get up and running. Uh did anyone manage to get it running on their machine? Yeah. Is it is Google search grounding working? >> No. >> Okay. That's uh that's a shame.

All right. Um, what else did we have? So, we need to fix uh lots of takes away from this. Um, yeah, if you didn't get the link, so this is the link to the live API examples. So, um, they also link from the docs. So, if you go to kind of the Gemini life, uh, API docs, you can find them there. Um is that the end of my slides? I do think we have yeah the agent skills as well. So, I mean, if you just go to the Gemini

Life, uh, docs, uh, Gemini Life API, uh, and in the on the main docs, uh, we've actually linked it from, uh, the top there, uh, try the live API, Google AI studio, uh, the GI up examples or use the coding skills. Um, so that is, yeah, that is how you can get started. Cool. That was, uh, not how I was hoping this would go. Um, yeah, we'll we'll figure out what what went wrong there, but um, yeah, I appreciate you all

joining and yeah, we we'll take questions. >> Yeah.

>> Yeah. So, you can look at kind of the session management. So um there's actually sort of so the live API has kind of this context window compression. Um so without compression kind of audio only sessions are limited to 15 minutes. Um audio video sessions are limited to 2 minutes. Um so what that means is that sort of you will the session will kind of terminate. it will give you sort of this go away pane. Um, and what you can do is

sort of enabling context window compression. So context window compression is kind of like a you know sliding window where you basically say you know like I want to keep that much context sort of in my window and sort of as the conversation progresses it will then actually like forget kind of the previous context before that window. Um so yeah so context window compression is something that you can uh enable kind of

you know to have that sliding window to uh make the sessions longer but then you know there's only so much context depending on um the frame rate that you're feeding in in terms of images depending um yeah mostly mostly it's images audio is sort of uh audio only sessions there's more kind of context you can keep in the window but And as you're adding kind of video frames to it, uh it does yeah compress it.

>> Uh yeah. Oh yeah. Yeah. >> Um is there any real life use cases that this is being used for that's very creative from a like a business context? very >> see what you've done today is a lot of fun, but like applying it to business. Is there any businesses that are actually doing this really well right now? >> Yeah. Um I mean so Shopify has it in production with Shopify sidekick. Um there is uh a bunch of so like uh

actually one that I really enjoy if you Gemini life API blog uh we had kind of a a case study which is um this startup. Yeah. So I mean stitch is using it as well. You can like vibe code vibe design with your voice and stitch but then you know stitch is built by Google. So um you know you probably got to discount that. Um Whimo is also integrating it. So um you know we first we got rid of the drivers

in the cars and then you know you do want to talk to someone in the car you can then uh talk to Gemini uh in the future. So they they are working on that. Um I like this one. So this is uh Hey Ado. Um it's a it's a great startup from Argentina. Uh so they are building these um voice sort of companions for the elderly uh in combination with uh kind of an app uh for sort of the caretakers or you know the the the the

children of the elderly where you know they can get notifications you know should the elderly mumble about something that no but so it's it's a really nice interaction where like the multilinguality um really shines, you know, because like in Argentina, uh you know, a lot of it would be Spanish. Um but there's a nice example you can kind of look at. Um which is really sweet. >> I came to visit my grandma Maria. I want

you to say hi to >> you you can you can look at it in your in your own time. Uh and then I think there was another one. So, um, yes, it is somewhat more of a future music use case, just kind of looking at, you know, some of the rough edges and limitations. And I think for now, if you're, you know, like in in a real business use case, you might be, you know, better off with kind of the cascading pipeline

because it gives you sort of the observability at each step of the pipeline. um which kind of with the the real- time you know native audio um you don't really have that fine grain control and observability in terms of you know plugging into say like rewriting the response before it's being said. Um you know obviously there are certain benefits with that in terms of the natural flow of the conversation but for

certain business use cases it might might just not be there yet. So it is somewhat you know a bet in the future of like what uh kind of real-time conversational interactions will look like in the future. Um but yeah depending on your business use case today it might not be the best fit just yet. >> Are the transcripts allable? >> Uh no. So you in the session you can't uh retrieve them. So you would have to

store them on your on your end. Um again so that is sort of where the um integration partners come in. So if uh yeah so lifekit pipe cat they all have like really good offerings to you know store the entire audio as well as the entire transcript and sort of give you additional observability tooling on top of that as well. Um, so it's not something that is kind of all available sort of, you know, from just the Google

site. Uh, so that's something where currently we're relying on kind of the partner integrations to to sort of give you that additional functionality. >> Yeah. >> Oh, sorry. Uh, behind you. Yeah. >> Do you want to go first? >> No. >> Okay. Um so you said that this is not you know like super business ready for more more complex use cases but what are your thoughts for example in um replacing interview interviews for

recruitment using this? Yeah, I mean I'm not sure I would, you know, replace your entire interview pipeline with that, but I think it is a great scenario, you know, for certain steps in the interview process or, you know, being able to screen more candidates, for example. Um, yeah. >> Do you think is that ready? >> Do I think that's ready? um >> because there's a lot of like um context that you also want to give it, right?

Especially even if it's like a first screen or the quick screens that you're mentioning, you still want to put some criteria that would guide and guard rails on how to guide the the conversation. And then the second part to this is also can it work for example with if my company is in a a Google environment Google meets right now we have auto transcript. So can you put these tools together? >> Um yeah so it is uh a preview. So it is

something you can use in production. Um depending on your use case I think you need to evaluate like you know do you need like sock 2 sort of there's potentially a bunch of things that you need to build around it for it to actually fit your business use case. Um, so yeah, it is ready for experimentation. >> Does that help? >> I mean, I think that's what we're doing a lot in. >> Yeah. Uh, oh yes. >> Um, an issue I always have is when I'm

demonstrating voice agents, a lot of people are talking and it's it can't differentiate the speakers. between each other. So is there a solution for this already? >> It on a voice sample or something in >> terms of like identifying the different speakers. >> Yeah. And so it only listens to you if it's your agent for instance. >> Oh, interesting. Um it only listens to you. >> Imagine you have a coding agent and

somebody makes a prank and says delete the file or stuff like that. You don't want that. >> Yeah. No, that's that's interesting. No, I don't think there's any specific ability to sort of like say just listen to me. Um, so there is sort of kind of this proactive audio where you can tell it to kind of only respond in certain, you know, to certain context. So like ignore things that aren't relevant to

the conversation. Um, so to some extent that works. Um, but I don't think it's super reliable at the moment where you'd say like only listen to me, ignore anyone else. >> I've done that with parakeet from Nvidia where you can train a little 10 seconds and it can differentiates the speaker that way. But it would be nice to have something like you talk to it and then it recognizes your voice and ignores the

other voices for the rest of the >> That's cool. That's a great great idea. Yeah. Thanks. >> Uh yeah, I think in in the Yeah. >> What does thinking look like? Uh is it does it think in text or is also thinking in speech? >> Yeah. So you get the thinking uh only in in text. So there's uh text events uh on the websocket channel that um so you can you can opt into getting the thinking um as text. Yeah. it wouldn't speak out the

thinking. Yeah. >> Uh thanks for the demo and uh for being brave to go up against the demo gods. Um I had a sort of question around the multimodality side of things. Uh one of the areas that I really want uh good text to no speechtoext models is having them be grounded in what I'm looking at. like when I'm coding I want to just you know word vomit into cursor sorry anti-gravity uh and have it understand

the context and you know when I say something that is a specific class name it should just actually use that um how does that work inside of this framework like would would this be a way to actually do do that grounding or would you recommend some other API for that >> um and this is for so so general Gemini models are really good at audio understanding. So, um if your use case doesn't require like fully real

time transcription, I would actually recommend using like Gemini 3 Flash um to basically transcribe but also get, you know, like ingest context and sort of basically get contextually aware transcription. >> Um at the same time.

And provide mult

awareness.

Yeah, there's uh so I mean depending on your use case if you need it to like be fully real-time conversational um then yeah so you can kind of use text to sort of ingest additional input or you know imagery if it makes sense but then again that you know reduces the context um window size um or you know if you don't need kind of the fully real time um then like using Gemini you know, just flash to, you know,

transcribe is actually pretty good. >> Frame per second means I'm talkingual awareness and your visual doesn't change, you can send input, then speak for 5 seconds and not send an additional image. then you are not using so much context. I think like one image is around 1,200 thou 1,200 tokens. So not too much. Um so if you are like in your editor you want real time you basically can use the API.

First input is send real time image and then send real-time audio and then you stop basically and the model has the image input and the audio input and can respond to it. So you there's no need to stream the image consistently if you don't if it doesn't change or if you don't need like it to react to it. Yeah. >> Cool. Yeah. Uh I think we have a bit more time uh there in the back. Yeah. How do we get you the microphone or do

you just want to shout it out? Oh yeah, we'll do it. Thank you for your interesting presentation. Uh I have a question about the personalization or adaptation. Can it uh recognize the speaker's level or the knowledge during the interaction and then based on the speaker's knowledge produce the results or not? >> Sorry, can you repeat? Can it >> can it recognize the speaker's knowledge or the background during the interaction

to produce the response based on the speaker's knowledge or something like that to personalize itself? So you you want to ingest kind of initial context. Is that what you're saying? >> Not context. For example, suppose I'm talking to that about the civil engineering and candidate recognize I'm a civil engineer and based on my knowledge produce the result use the advanced keyword in civil engineerings

or not >> based on my knowledge. So you would you would have to if it's like special specialized knowledge you would have to give it away to access that. Oh, that mean doesn't have any memory to recognize the human's background or to find the main context of the information of the interaction and based on that produce the next result. >> So you have to somehow feed in that knowledge. So you could either do that

sort of before you you know like as you set up the session you can ingest kind of the the knowledge as initial context for example and then it has that in context to talk about or you would give it kind of function calls to access knowledge sort of during the session as you as you converse. >> Yeah I see. Thank you. that >> yeah know I was to find that uh look out the GPT for example during the some

turns it can find speakers or the users knowledge or the main concept of the information and based on that the GPD can produce some results that means a step by step gradually it personalize to the main context of the conversation so my question is can it a step by step personalize itself to the main context of the uh of the interaction and then produce a result to point to the uh >> so like as long as the the context stays

within the context window during that conversation. >> Yeah. It it would it can like it can identify different speakers and sort of remember what was said in the conversation and like if they introduce themselves with their name as well it can remember kind of that person's name and so like yeah that's kind of the the the audio understanding sort of within Gemini. >> Thank you. >> Okay cool. Uh yeah do you just want to pass it

forward there? Yeah. >> Uh thanks for the nice presentation. Uh could you share maybe some um of your experience on how to evaluate these um live uh voice apps because I can imagine that this becomes a lot more complicated than typical apps. Um yeah I've so it definitely depends on your use case in terms of like uh you know like what are your requirements in terms of you know do you have HIPPA do you have sock 2 like what

is the amount of function calls the amount of guardrails so there's definitely a lot you know >> these demos are nice and and fun but like to bring that in a b business context there are definitely a lot more um steps involved and so that is kind of where the partner integrations come in. So uh you know lifekit has built kind of their entire business around sort of giving you all the batteries around sort

of voice agents and so I would recommend if you know sort of looking at the partner integrations for the sort of real business use cases potentially. Thanks. >> Cool. >> Yeah. >> I hope you don't mind if I just ask a simple question about the interactions API. Going back to the previous talk. >> Yes, please. >> When's that going to be available on Vertex? >> Um, hopefully soon. I mean, if you speak

to some Google Cloud person, some Vertex person, the more you tell them, I need it on Google Cloud, the the easier it gets. We'll do. >> Yeah, it's certainly not in our control. >> Okay. Yeah, that's bad. That's bad. That's cool. I mean it the API will be the same. So you can start today on Gemini API uh start testing. If you need higher rate limits, anything else you can like always reach out. If you need

vertex enterprise specific features, then you might need to wait a little bit. Can I ask like in terms of like PII in any like conversation history, do you know how that's like stored in terms of like like data sovereignty? Can you specify your own data sources or is that all handled like back end um with with like within the API? >> So you can always disable storing anything. So we have a store equals

false flag. So we would not store anything but not storing means no serverside state. So if you would like to use this that's a bit difficult for other vortex features in terms of data soy where you call the model I would expect them to be like similar to generate content so if they have it today they will have it there in the future as well. Okay, cool. That's great. Thanks. Appreciate it. >> Cool. Uh, one last one.

>> No. Okay. Ah, >> sorry. >> No, please. >> Thank you. So, I have a question about u hallucinations. So, we >> Sorry, the what? >> Hallucinations. Yes. So you've have shown some examples uh with the weather that didn't work so well. Uh but uh how do your clients actually deal with that stuff on production? Because I can imagine that for like some examples that we've seen here this is fine but uh in

real life this is a different story. So can you give some best practices or how to deal with that? >> Yeah definitely. Um, so I mean on for the demos the there's definitely a lack of best practices in terms of like system instructions and you know there's a lot that you can do sort of with uh the you know better system instructions to uh have the agent actually follow um the system instructions and not you know go

off and like hallucinate the weather for example. Um, so yeah, I think we we have like there's some best practices do talks. Um, so I'd recommend kind of going through through those. We have an example as well sort of, you know, how to sort of structure um your your system prompt and sort of put you know your guardrails in there, guidelines and um kind of the tool definitions as well. And so once you build that up, uh, the

agent gets a lot better, you know, at following the system instructions and kind of staying within those those parameters.

>> Cool. Cool. Um, yes, thanks so much everyone. I I do apologize for the hiccups, but we we learned something and we'll we'll improve upon it. Uh, but yeah, would love for you all to test it out and um, you know, let me know over the next couple days. I'll be around what you find and let me know your feedback. Thank you. Cheers.
