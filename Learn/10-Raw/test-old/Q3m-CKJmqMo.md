---
# === identity ===
id: Q3m-CKJmqMo
url: "https://www.youtube.com/watch?v=Q3m-CKJmqMo"
title: "DGX Spark Live:  Ask the Experts - Gemma 4 on DGX Spark"
aliases:
  - "DGX Spark Live:  Ask the Experts - Gemma 4 on DGX Spark"

# === creator ===
channel: NVIDIA Developer
channel_url: "https://www.youtube.com/channel/UCBHcMCGaiJhv-ESTcWGJPcw"
channel_follower_count: 211000

# === time ===
duration: 2642
upload_date: 20260424
fetched_at: "2026-05-16T07:57:46+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/Q3m-CKJmqMo/maxresdefault.jpg"

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
view_count: 7002
like_count: 176

# === status ===
availability: public
live_status: was_live

# === lifecycle ===
state: active
---

# DGX Spark Live:  Ask the Experts - Gemma 4 on DGX Spark

## Description

Gemma 4 introduced a powerful new family of native multimodal and multilingual models that scales across the full spectrum of NVIDIA hardware - from Blackwell in the data center to Jetson at the edge. 

In this stream, we’re going hands-on with the DGX Spark to see how it can amplify Gemma 4’s features, including massive 256K token context window and native vision/audio capabilities.

Bring your questions! We’ll have experts from NVIDIA and Google DeepMind.

## Transcript

[snorts] >> Hello everyone, Maitri here [clears throat] with NVIDIA and welcome to another week of DGX Spark Live. Today we have a very special session for you. We have the experts from NVIDIA and DeepMind joining us for an ask the expert sessions on Gemma 4. Thank you for joining us and please type in the chat where you're joining us from. We love to hear what parts of the world we have people joining us here to learn

more about DGX Spark and other cool things. So please go ahead and introduce yourselves in the chat. And without further ado, I'll just pass it on to our guests. We have Anu and Anusha from NVIDIA and we have Ian from DeepMind to introduce themselves and then we can get into the demos. Very cool. I will very quickly introduce myself and then pass it on. Okay, my name's Anu. I am our um developer marketing manager and I I work with all

of our um big open source model launches. Anusha, can I pass it on to you? Uh-oh, Anusha, you're muted. Okay, can you hear me now? Yeah, we can. Okay, perfect. Hi everyone, I'm Anusha. I'm a developer advocate here at NVIDIA. Ian, please introduce yourself, our guest. I can. My name is Ian. I'm a developer relations engineer at Google and I work on the Gemma models and most recently the Gemma 4 launch.

All right, I think we're good to get started with the demo for today. Okay, so I'll quickly take you through what my setup here is. I've pulled the Gemma 426B model. It's running locally on a Spark. And it's being served via vLLM. It's a fairly straightforward setup, very simple to get going. That is it to get the model served locally. As you can see here for my specific use case, which is this just this demo, I've

limited it to 150 images per prompt, one video and zero audio. That's just the scope of this demo though technically it supports all of these modalities and we talk we can talk more about that with Ian right after. So with that, let's get into the actual demo. So we're going to start off with a very simple image prompt. And what we want it to do is take this image. Okay. Okay, so we have this image which is a

menu where all the text is in Hindi. And we're going to ask it to take a look at this image and translate the text. So translate the text in this image to English. So as you can see, I'm not really talking about what the text is, what language it is. And let's see what it does. There you go, pretty much immediately it's able to identify the text, figure out what language it is and then move on to translating it as well.

It is a long menu, so let's give it a few seconds to get through all of this. I always tested this out before, so we do have a good sense of the translation is out. [laughter] You know, I think that's one of the the value props of Gemma, right? Like throughout all of the releases it's been really strong in in multilingual, right? Um Okay, you want to share on that, Ian? Yeah, we I mean with an hour training we

have about 140 languages that we support and then if you if you use one of the audio models, there's a there's a couple more that we kind of target for that specifically. So yeah, I think for us like making it as accessible as possible and having like a good baseline for, you know, also fine-tuning as well. If you if you find there's not a language it supports, you can tune it to customize it for that too. But it has a very good

like swathe of multilingual training data which kind of really helps it in like every component. So you know, you don't necessarily learn concepts in like one language, they can come through lots of different sources. So yeah, for us this is like super important. So this is a great example. Yeah, all right. So with that we're going to move to the next one which is taking it a notch higher. We have this

video from NVIDIA's Groot robotics data set. And it's just a short clip of two robotic arms and a bunch of vegetables and fruits in front of it. And we want it to list out what it sees in this video. So let's list out everything on the table and actually let's just leave it at that. Let's see. And there you go, once again very quickly it's able to identify what objects are on the table. And then it's also split them into

vegetables and fruits versus other equipment {slash} objects. So those are two quick prompts to sort of show us the a tip of the iceberg sort of thing of all the multimodality skills that Gemma 4 has. We're going to also try a a fun prompt which is uh one of my favorite things that I've tested out recently where with under 15 words, technically if you remove stop words it's probably closer to 10.

Immediately it starts building an entire game. All I've said is build me a classic snake game and it's generating HTML. One caveat here is that I have uh in the system prompt specified that every time I ask for a game I want it to be a web browser supported game. That's why it's generating HTML. But even then very short prompt and it's immediately generating this. This of course will also take a few seconds just because

it's a very long HTML file where it's building the games from scratch. But I do have a version of this that I generated right before. And if we go load game, okay, well it started immediately. I I swear I'm better at Okay, no, I am All right, let Let us see. Okay, well I'm terrible at playing the game. But it did a good job building the game for sure. Okay, maybe I'm not that bad. This is [laughter]

I'm very jealous. Because I never got really good at like making front ends cuz I was always doing back end engineering and now it's just like so much easier. >> [laughter] >> It's so easy and the game like for the the short prompt that we gave here, this is an amazing game. So it's really cool to look at. And the last demo that I'm going to take everyone through right now sort of tests out the long context ability of the

model which is something that I think we're highlighting. Uh so I have six PDFs here. They're all long PDFs. They're all Google white papers. And we're going to go ahead and load the documents. So the thought here is the demo you just showed was like doing output, right? With HTML and now we're kind of doing two. Um a completely different demo and you're >> Right. doing a lot of processing, understanding. So very lots of different

use cases that you Right, right. And like I mentioned, this is just like four small things of like the myriad of things Gemma 4 is good at. So we can definitely talk more about that right after. Uh but yeah, now it has six PDFs. They're all loaded. They talk The PDFs talk about agents. There's embedding and vector stores, lots of cool stuff here. Now what we want to try to see is given its long context capabilities um I'll

ask it two types of prompts. The first is more of a needle in the haystack kind of thing where we want it to identify a specific thing from this massive context base that it's gotten. And the second one will be more of a throughout this context summarize something for me and come up with something that sort of synthesizes everything. Uh Okay, so the first one is what specific automotive AI agents are described in

the documents. So this is a very specific question that is probably mentioned in only one of the six documents that I gave it. And there we go, immediately it's listed out the agents as well as what its sources are. It's citing its sources here. And the second one, like I said, something that sort of goes through the entire thing to come up with one answer that summarizes everything is the documents describe multiple reasoning

frameworks across all of these PDFs. We just wanted to create a unified list of specific frameworks that we've mentioned here and then talk about which document discusses which framework and in what context. So this of course requires going through all of the context that we've given the model. And as you can see pretty much immediately, it's able to identify those frameworks, list them out for us, cite its sources again. So

this of course is just six PDFs. You could scale this up up significantly uh with the smaller models as well as the medium-sized model. So yeah, that's that's a quick demo of some of the many things that Gemma 4 is really good at. Cool. Well, we have actually a few questions that have already come in. Um first uh I think we already answered this in the chat, but um asking which model you were using.

Um actually Ian and Anusha, I would love to hear your experience working with like the different small models. Um you're using the 26B1 in this one, but um >> Yes. also the history of you know, I I we've seen mobile-friendly models um in the last few Gemma releases. Like tell us more about that choice and and what you've seen, you know, taking traction in the community. Yeah, absolutely. Yeah, and we're happy

to do that. Yeah, so I mean for us it's about making the models accessible across like a whole range of different devices from like Jetsons, you know, Raspberry Pis, mobile phones, laptops, all the way up to like cloud compute and stuff like that. And like for us the mobile story is kind of super important, you know, we use our phones like every day. Having smart assistants on it was like kind of core to both, you know, uh

our offering. So we want to build a model that would kind of work like effectively on both of those. And we have the E2B and the E4B models that kind of do that bit. So they're kind of like the smaller ones. We have one that's kind of uh much quicker. It's like the it's much uh quicker on the infant side and one which is you get a bit more intelligence, but requires a bit more RAM to kind of run and support.

And we even have a architecture called that we call effective, which is where we have uh per-layer embeddings. And the embeddings actually uh they are separate from the rest of the the core architecture of the model. So you can do some clever things where you put the embeddings into like flash memory and stuff. So it means you don't have to load all of it. So you actually have a much smaller initial footprint.

So like I think for us like, you know, those kind of spaces and like, you know, running stuff on consumer hardware is like super important for us. Like, you know, you know, we're we're we're like compute-starved in the world of like everybody wants to run generate more tokens and stuff like that. So hopefully we can make sure that you have something that you can run on your machine, but then also kind of in the cloud, too.

Anusha, anything you want to add? We're getting some questions in the chat about, you know, maximizing tokens per second, which is really important for us. >> [laughter] >> Yeah. Uh you know, what sort of things do you all look at when um trying to maximize inference? Well, I I think I'll circle back to the first question you asked, um which is about my experience setting this up. And I think like I showed early on, the

setup was extremely easy because it's very easy to dump the 26B1 on a Spark, get things running, and it's extremely fast with like the three or four-line command that I shared early on. Um I also experimented with the smaller models. This was the 26B1. Um I also tried out the smaller ones. Extremely fast, also. The The reason I chose the 26B1 here is because I wanted to test out a longer context range. For the demo I only

choose chose like six PDFs. But I also tried it out with way more. And I think with the smaller models, it's 128K tokens. This one was 256. So seeing that in action was really cool, and I'm also really excited to test more things out with Gemma 4. One question that I had for you, Ian, that sort of came in my mind right right as you were talking about the history of Gemma is that obviously the demos I

showed here were like I said before, very tip of the iceberg of everything that Gemma 4 is really good at. In the last couple weeks, I think it's been a little over three weeks since Gemma 4 has been launched, and it's had like a lot of people talking about it, trying it out. Has there been any specific use case that you saw that really excited you or was something that you didn't expect when the model originally came

out? Yeah, that's a good question. Um I mean, so I'll I'll kind of I'll answer that in two parts. Like there's there's things that excite me and that people have built, and there's also things that I was kind of unexpected. So things that excite me uh I love like the the voice agents, like the local uh you know, you know, having your own like like assistant that like runs on your laptop or your phone that you can take around

with you. Uh like lots of people have been building out stuff related to that. Uh we have uh the smaller models, the E2B and the 4B have an audio in as part of it, too. So you don't have to have a separate like speech-to-text. You can use the model and it will understand. And actually that like that additional context makes a massive difference in terms of like the understanding. So like, you know, if you just if you just

get it to transcribe stuff, like it will do a pretty good job of uh you know, I'm creating a shopping list. Like it has a better understanding of the products that we I might actually add to your shopping list, too, because you're able to kind of do that. It's like uh you know, combined with the model's understanding. Um so that's one that I'm I'm actually excited for. I can't wait to see people make more of

those. The surprising bit uh is I'm really surprised how quickly people put these into like agent frameworks. You know, things like Open Claw, like Hermes agent, like uh we've been seeing people just like, you know, just going all in and saying like, you know, I've Oh, now my my whole workflow is now just powered by, you know, Gemma 31B or the 26B depending on like, you know, whether you're going for like intelligence or

speed. Um and like they kind of really ran with that. Like we thought people would do it because we had, you know, function calling capabilities, got reasoning capabilities, like all the things you need to do kind of work around a load of problems, but you know, actually the the examples you showed like the ones that I thought people would be most excited about, but really it's like what they can kind of just set

their agents off doing. So maybe they could just say, "Oh, I've got like these 20 documents. Just like figure something out and, you know, write me a summary of them." And you don't even have to like specify. The agent would go off and do all that stuff. So it's kind of like I think about like the extrapolation of that. So yeah. Well, tell us more about um I know you've added more modalities as future

Gemma releases have come on. Um actually tell us like the the recent history of Gemma and your experience um seeing the the space of all this, especially on the the local agent local uh model execution side. Yeah, absolutely. So I mean, when we started this project, gosh, almost like two and a bit years ago now. Like it's it's we're at we're at the fourth version, and I feel like we've we've it's only been like a couple years.

Um yeah, the we we started off know we know that, you know, building things in the open like is grounds for innovation. It's it's like a very kind of democratized way of like uh creating models. So it was important for us that we had both like the Gemini offerings and like uh the frontier level, but then we also had like the open models that, you know, you could tune, you could adjust, and you could do research on.

And I think the first couple versions of Gemma models uh a lot of the community built um uh things like, you know, translations for different languages. So we had like a version that works with Southeast Asian languages like in Bulgarian. Uh there was lots of kind of research projects that were based on it. So we tried to build like a good foundation for that. But what we find in uh since maybe Gemma

3 up to Gemma 4 is there's been a much more of a shift to using it for a lot of uh like commercial and like personal applications, too. So there's been more of a demand uh for uh [snorts] you know, the model to be able to like think, more of a demand for it to be able to take action. Uh and we kind of build this alongside like obviously, you know, other things we do in Google as well like, you know, in our

operating systems like Android and stuff like that. We want to provide smart models for that. Um but we also want to build a model that would work on iOS as well, and then like, you know, works on your laptop. So uh we kind of saw a shift from like what I would describe as like the traditionally researchy like usage of open models to a much more like, you know, you can go and download like AI Edge Gallery on your phone on

iOS and Android, and now you've got like a pocket version that you can just like point at things. And people will use that to kind of explore like the different modalities to your point like about, you know, taking video or taking pictures or like, you know, like leaving voice notes to the model. So I think for us it's we very much listen to what the community asked us for, and this is, you know, the kind of core bits behind uh

Gemma 4. So a lot of this is like direct feedback from that. You said the magic words. Um we noticed that on this launch it was the first uh I believe the first Gemma launch to use the standard Apache 2.0 license. So you are intending for people to start using this for commercial use cases? Yeah, absolutely. I I can't believe I didn't lead with that. Like that's one of our big pieces. Oh, so you asked you asked what what

were the big one of the big surprises were. I mean we were we were quietly happy that uh you moving to Apache like it would open a lot of doors for people, people who would otherwise you know, have to go through long legal processes to try and like work with the Gemma license could do it much easier cuz, you know, Apache's work very well understood. Um I don't think we were quite ready for how excited people were about that. Almost

as excited about like the models themselves. So uh and obviously, you know, we were on board with that cuz that's what I wanted what we wanted to do, but um yeah, having having the community kind of say, "Yes, this is exactly what we're after." and um we're going to take this and run with it is kind of very exciting. Very cool. Well, we actually have so many questions coming in. So, let's go through the starred questions.

Um Oh, okay. Actually, one that, you know, I I am obligated to ask about is uh there's an NVFP4 version of uh I believe a 31B. Um so, Heisenberg wants to know like when should we consider using quantized models? Oh, yeah, absolutely. Well, I mean, this is the beauty of it. I think we talked a little bit about speed. Uh the the tradeoffs in with most of these models, if you've been using this for a while,

and if you're not, I'll kind of summarize, is like with the quantizations, obviously, we they can fit on smaller and smaller uh like footprints of memory, and then you get performance improvements as well, depending on like the accelerators you're using. But like the challenge has always been retaining the quality of the model between those two things. And for us, I think, you know, working with you

folks at Nvidia and and having NVFP4 specific ones that are targeted for hardware, we get like the combination of that. So, I think actually I was looking at some of the benchmarks that we were getting out, and we're getting like very similar, if not identical, to like some of our bigger models. So, you get something that's like you know, a quarter of the size of the the BF16 model, the 16-bit one, but

still retaining like a lot of its reasoning capabilities, its mathematical capabilities, coding capabilities. So, like my my short answer to that is if if you have it and you can use it, use it, cuz that's like the best route versus uh you know, trying to you know, get a much bigger piece of hardware to to do the same thing, cuz otherwise you'd be running a slower 16-bit version compared to like, you

know, an INT4 version or a quantized version. Yeah, I guess actually we should kind of quickly define what quantization is, right? So, the the models come out, right? We have a lot of the the data in floating point. Um and we want to reduce the amount of storage that it takes. This is what we're talking about the bits, right? Um but it's almost like an art and science where while we're doing the quantization, it could be done by the

community, it could be done by um who built the model. Like you can quantize it down to many different types of precision. Um that's what you're talking about, right? Like mean making sure that we still maintain accuracy. Um we kind of have like an internal joke like you could quantize down a model to you know, one bit. It's still technically a model. It's just not going to give you anything uh useful out.

Yeah, absolutely. And I think like part of this is like, you know, you find through the use of the models like what size like quantization is like suitable for your task, right? You know, on the on the mobile phones and you know, the small devices where RAM is RAM is really at a premium, I think in some cases we sometimes have like mixtures in the models. So, it's not all, you know, like four bit. Some of some layers are eight

bit, and that kind of allows us to, you know, kind of retain more of the quality, but not kind of sacrificing everything. So, there's there's so many different quantization strategies, and like I I see some people in the chat are talking about some of the stuff from like uh people like Onslaught, and uh there's loads of uh uh teams in the community that have like different approaches. So, it's very much kind of

try the different models, uh and, you know, see what kind of works for you and works for your use case. And there's like we see a consensus building that around like FP8, like, you know, the models pretty much don't lose any kind of there's no degradation pretty much. Um so, having like a scheme that is specifically tailored to that and being able to retain that like uh NVFP4 is like a good example of like where

we've kind of done the quantization steps right, but there's uh yeah, I've seen there's like Q6. I see a few few people using Q3. Like if you really got constrained hardware, you can go like to three bit. Uh so, yeah, there's um yeah, explore is the is the short answer. Very cool. >> we have a question from Charlie Laws. He says, "Do you have any tips or insights on how to fine-tune these models?"

Yeah, good question. I I say for what we've been finding a lot of the time uh is using uh like techniques like Laura and QLoRA uh are kind of the good places to start, right? When we um the obviously the bigger the models get, the the more expensive they become to like fine-tune and optimize. So, if you've got uh like some techniques to be able to do a smaller model, but then on like a fixed like amount of hardware,

you can uh you can get a lot of optimization techniques out of uh of using tools like that. Actually, Onslaught is a good example of like one of our partners that we work with to that are very good at like the fine-tuning route, cuz they have a good balance of like uh using compressed models, but then also doing it such a way that it can fit on like smaller hardware. So, like a T4, like an L4, uh

versus needing, you know, like a much bigger piece of hardware. So, I think for the the main tip I usually have is like start with using uh the the the general prompting strategy, because all of the models in the family are actually very good at instruction following. So, you might even find that before you even need to tune, there is it's actually has quite good capability at particular task. But say you've got a particular

data set that you need to optimize for or like maybe you've got like different multimodal data, then uh you can probably start by trying to use uh an appropriate size model for the like the target hardware. So, start with like a smaller one, which is a little bit cheaper to manage and to like evaluate, and then, you know, move up to like the, you know, the the 26B or the 31B. >> [snorts] >> I think it also depends a little bit on

like expertise, because when you get to the 31B level, uh uh or the 26B level, uh doing things like mixture of experts tuning is very different from from tuning a dense model. So, sometimes it's easier to stick with the bigger dense model to just kind of understand the capabilities rather than it is to try and tune experts within the MoE. So, I think like yeah, start small and kind of build up is the is the major

recommendation here. On the theme of fine-tuning, our next question actually has to deal with what we very briefly touched on earlier is Open Claw. Um So, it Let me check the name. Oh, okay. LinkedIn user wants to know, "Do you have any tips for specifically fine-tuning for the certain types of tasks that Open Claw has been used for?" And you have to answer this, yeah. >> Very good question. I think the tricky bit about this is

that because it's so open-ended as to what, you know, these agentic harnesses can do, uh it's for us, we didn't build a model for a specific harness. We built a model to be like a generalist, that it could understand and reason about a problem and then use the tools that it has in order to do that. So, obviously with like specific agent traces or specific tasks, you can optimize it to do certain sequences. But even now we're

finding that like the 26B or the 31B can do pretty good at skills uh like just, you know, again written kind of in prompt form. So, uh I'm sure there's going to be a an Open Claw optimized version of Gemma. I Not that I have seen yet, but I'm sure the community is like working on it. But again, it depends like with what tooling it's using and like, you know, what kind of work place you need it to be able to

do, because uh because it's so open and so configurable, the I think, you know, trying to trying to tune the model to do this at this point is uh is going to be much trickier to kind of you don't want to lose capability in other areas by over-indexing on like one type of activity, unless it's the only activity you do. So, I think the way I think about it is like figure out what your workflows are and figure out what it

kind of fails on. And if you can adjust that in like skills, and you can adjust that in like configuration or like access tools, do that bit first. And then if you really need to get like reliability out of it, that's when you can start going down like the fine-tuning route for, you know, specific traces. Um but yeah, for instance, like if you have lots of multi-turn conversational stuff that you

need to be able to do, uh you can tune the model to understand what it should how it should answer each stage of that communication or chat as well. And that would probably work quite well for like typical agentic scenarios. Let's actually flip this around to um another question. So, Antonio um wants to know how does the work of fine scientific literature or in a clinical disease target? So, this is

very much not general. Um and I know that >> Very specific. >> [laughter] >> Um Gemma has also has done a lot of work with like Med-Gemini. Um is there anything you want to share about um that area? Yeah, definitely. I mean, so for us, it's important to make a a generalized very intelligent model. Um so, we talk about, you know, how we we've got a lot of learnings from, you know, building Gemini models, which are kind of very

good in like deep reasoning and uh uh like, you know, scientific and mathematical like approaches. And there's the same thing for kind of Gemma stuff. Uh the the difference obviously with, you know, tuning like Med-Gemini, and for those who don't know Med-Gemini, Med-Gemini is a a variant of Gemma models built by the DeepMind team uh working with clinicians that can do um things like medical triaging and

image uh analysis of like medical imaging. So, it's it has data set specifically for that. Um for us, we want to kind of build like the foundation for you to be able to do on top of that, cuz Med-Gemini does a certain type of uh um medical uh information and capabilities, but it's not every type. Like there's all sorts of different uh uh types you could uh you could do. So, all the different domains uh are

applicable kind of on top of that. So, I think for us, we we see that as like we have a very specific use case that we want to help people with with Med-Gemini, but if you have something different, you could use the Gemini 4 model to do it and see how well it reasons and thinks about out of the box. You know, you can get it to explain I was just using it in a demo the other day just explaining string theory to me.

Like just I asked the 31B like if like and and it kind of actually began with like where do I start? Right, I'm going to first explain quantum mechanics and then like so yeah. I will save you the hassle. It was a very long output. Um but the fact that the model has an understanding of this and to me it's even more mad is that I wasn't connected to the internet when I was asking it. Like I could ask it like these very

in-depth questions and it's and it understands that through its training data. So having like a foundation for doing this I think helps when you apply it to another domain because what it can do is it can use its inherent trained understanding to draw conclusions from the data that you pass at the additional data that either tune with or that you you provide it through tools and document access and stuff like that.

Well, speaking of complex output um in this use case did you actually end up using like the the reasoning capabilities? Roger uh wants to know well Roger wants to know how are the thinking capabilities? Yeah, so I mean for us I think the best way to describe it is like thinking as a general pattern adds to the model's ability to get correct answers like within short amount of time. You're trading you're trading

basically token output generated for a more thought through like solution. What we what we found at least with like thinking capabilities generally in Gemini is that you maybe it has strange effects in the terms of like let's say you've got it to generate you an SVG, right? So like like the example we just saw it can just generate pages of like HTML JavaScript other programming languages as well.

So if you got it to generate an SVG, it would you know okay I need to put lines here and I need to put shapes here and whatever. If you turn on thinking it will reason about how it's going to do that do the SVG image before it then generates it. And that extra like process actually can give you much more accurate results at the end. So we find like we have a brilliant demo. I think we posted it a couple of days ago where we have a

version of the 26B that spins up 10 different terminal windows and each one is generating an SVG and it's like running on a laptop. So it's like they're they're all in parallel making like these little logos. Um and if you turn on thinking for those you get like better output for the logos than if you didn't turn it on. Um because it will think oh okay I'm going to do some space themed SVGs. I'm going to do a black hole. What does

a black hole look like? Okay, well it's going to need you know this shape here is going to need an event horizon and then it thinks more about how it constructs it and then you find that the output ends up being a better looking black hole. Uh but also I guess for for thinking and reasoning like obviously this is kind of critical for agentic and agentic stuff. Like if you're doing coding or you're getting it

to do tasks and it runs into problems, the thinking helps it reason about like the responses. So like the general pattern of like a like a react style agent loop where you know the model does something sees its response and then like makes a decision and then does another another action. By giving it thinking enabled you end up getting pretty good responses to errors. It think like oh why did I run into this

error? Or if it for instance it finds it's it's trying to do like a particular function call that's not working, it can think about why that function call might not be working and it gives it a better like other path. So what we find is like with both the the 26B and the 31B and I mean even the smaller models too that it just it helps them better navigate some of those like workflows. It gets stuck

less because it you know every time it does run into an actual problem it can like figure its way out basically. That was a very long-winded way to say thinking helps. >> Yeah, [laughter] well that leads to one of the next questions from Edward. So I think you already answered this is it capable of handling multi-agent workflows with multiple tools and I think there's lots of different ways that you can demo that. Um so even

though like reasoning does help step through these like multi-step react loops what are the what are the limitations that you're still seeing and and how does this affect you know the way that you're going to be looking at and training and future Geminis? Yeah, this is a good question. I mean so one thing I think is going to illustrate this point cuz people they might look at the different models and then say well why have you

got a 26 and a 31? So the 26 is a mixture of experts but it has 4 billion activated parameters. So actually to do inference on it you need to activate way less than you would for the 31B. So it's kind of it's it's got like a shared intelligence across the experts but it runs closer to the speed of like the 4 billion parameter model. Um so in those cases like you get a very good a good reasoner that that can respond

quite quickly and can react quite quickly. Um but the 31B model is a it's like much slower in its output but it does a little bit more thinking or it has kind of like better results in how it may you know go through a certain agent workflow or how it might like reason over a code base or something like that. And I think one of the major limitations at this point which is kind of an architectural thing or like fundamentally about this

type of model is um when you have very very long context and it's trying to retain everything within this context. Like obviously as the context gets bigger and bigger and bigger like a longer chat history or like you know it's pulled in more files from a repository or it's got more sources of data. It takes the models longer to generate the output because they have even once they've processed all of it even if you

cache it, they have to kind of it kind of starts to ballooning. So I think one of the challenges is that the longer the agents work and run the the harder it is to get them to run efficiently and to be more reliable in like their output. So yeah, I think you you touched on it earlier like the we the smaller models the the 8B and the 4B 128k token context and the biggest are 256. And we've seen people kind of push it

beyond that as well. Like it's this is kind of like what we would say is like our recommended space. But even then when you have yeah, when you have like 256k tokens, you know that might be like you know like a code base or something but it's not going to be like your end your whole enterprise's software. So there's there's still kind of room in that space to kind of like build and extend and train the models to do more

even further context as well. But I think this is like a sweet spot for us in terms of like the trade-off between you know making the model like efficient and reasonable at particular length but then also like big enough that it can consume large documents or like you know multiple video frames or you know like whole libraries of books and stuff like that. Yeah, cool. And you Sharan Metri anything you want to add? I know we've

seen some questions um about clustering two sparks together. And I know we have some playbooks on that that we can share but um any experience running running that configuration? No, I don't have any experience running that configuration but I've been reading the comments and it's giving me ideas for things to try out. So I'm super excited. Yeah, I haven't I haven't run it either but I know there's a lot of playbooks

that we have and we have playbooks in the pipeline as well that users can refer to on how to actually run these large models or even you know multi-agents on a cluster of sparks. So uh our production team is definitely putting out all of the resources that you guys can access and learn how to cluster your sparks and kind of get started from there. Yeah, we'll post the playbook that's clustering two sparks. I know I've seen

people on like local llama claiming that they they clustered many more sparks together. So I'm I'm curious to see what those those results are. Yeah, and we actually have a really interesting blog out as well where now we support over with our software release people can actually build clusters of four and kind of build like a small inference engine for themselves and load up models and you have like 128

into four memory with this with an external switch. So it's pretty cool what you can do as you keep on clustering these sparks. Cool, we only have a few more minutes. So what closing thoughts do does everyone have? What do you want to What do you want to What do you want to add for our audience before we sign off? I think the one thing that Ian touched upon briefly is something that that's super exciting that I've also seen in

the past couple weeks is just how good the the combination of Gemini 4 on a spark and building a call locally is. It's something that we've tried out. I'm also super excited to try it out more. But yeah, I just think that's worth noting that that is a very cool use case that we're seeing a lot of adoption for. Yeah, I'd I'd second that. Like this is the bit that excites me a lot too. You talk about having like multiple sparks

and like I mean even having one would be incredible for a lot of people like cuz you know 128 gigabytes is a lot of RAM. So I think this is like you know it's not even just a case of you we talk about you know these models take up a certain amount of size but when you have enough memory to do it, you can have long context too. You can have long running things. You can solve serve like multiple users. So like all of my

experience at the moment are about, you know, can we have like multiple user systems or multiple, you know, claws or agents running simultaneously but being hosted locally, which is kind of the exciting bit. We made like a step change in model capability, you know, what we've got this year out of like the big 31B models is what was a cloud model last year. So I think this is the the kind of exciting bit like, you know, how

much of it can you actually, you know, run a lot of this stuff like on your, you know, different ecosystems and stuff like that. And it gives you like this additional like layer of stability like if you, you know, you can take it with you or you can, you know, you can use it to do certain jobs and use your important tokens for you know, building stuff in the cloud that like really matters that really requires a lot of

thought versus like your like simple workflows that, you know, a smaller model can kind of handle. So I think for me it's like this as we move to a world where you know, we've got like these GPUs that are literally not using cycles. You know, you could be having, you know, you know, you know, solving your taxes or like, you know, helping you with video production or like this is like this is my goal. I want to just

have, you know, like agents working for me doing all sorts of other things and and then save the really big hard tasks for like, you know, the big cloud computes where we can, you know, be running like H100s and like, you know, thinking of really complex problems. So uh yeah.

Very cool. Well, our very last question before we we do actually do have a quick question about asking if there's SP line support, which which there is. Um so we'll quickly answer that. Earlier we saw vLLM but again we try to support [snorts] whatever inference engine you are using. So there was day zero support for llama, llama.cpp. Um you know, trying to make sure you have the the most performant and functional

experience using these different engines. Um and I know Gemma worked closely with these inference providers over several releases. Anything you want to say to that, Ian? Yeah, I mean for us just, you know, tell us what you're using too. Like, you know, as you mentioned like we try and, you know, work with all these teams and then video like together. It's not even like a like a bidirectional communication, it's like a three-way

communication. So you know, how do we make it run on this inference engine but also how do we make it run fast on the video hardware? So it's like, you know, that's super important too cuz it's, you know, no good having one or other or both. Uh so yeah, like if you're, you know, you mentioned like, you know, vLLM, SGLang, llama, LM Studio. If there's others that you use, let us know. We'd love to like have feedback on, you know,

what's important to you and what you need to run on your hardware and, yeah, we'll we'll do our best to make sure that future Gemma versions support it. Very cool. Okay, well, I think I think we're going to call it a day. I'll pass it back to to Matrix. Yeah. And thank you Anu. Thank you Anusha. And thank you so much Ian for joining us and kind of sharing your expertise and your insights with our

community here. Our goal with these live streams is to get information and access to everything that we've been working with or working on to all of the people who make this brilliant community. So a big thank you to all of you for joining and everyone on the comments, everyone on the live stream. If we weren't able to answer your questions live, we'll make sure that we can get to them offline. Thank you for joining us once

again and we have a couple of slides that will kind of point you to the right resources you need. I know there were a lot of questions about how to kind of cluster two of the sparks or three of the sparks. And we have all of this info on our build.nvidia.com/spark, on our GitHub, we have a bunch of playbooks where you can get started on how to cluster and how to, you know, start running these models on your

cluster. So definitely go check them out. And with that we come to the end today. I want to thank the background crew, Zach, Jamil, and Barry for helping us run the stream very smoothly. And see you all next week. Thank you. Bye.
