---
# === identity ===
id: LnCXoIr0Mw8
url: "https://www.youtube.com/watch?v=LnCXoIr0Mw8"
title: "Build an Agentic GraphRAG System in 1 Hour (MCP + Knowledge Graph) | Databases for AI"
aliases:
  - "Build an Agentic GraphRAG System in 1 Hour (MCP + Knowledge Graph) | Databases for AI"

# === creator ===
channel: AWS Events
channel_url: "https://www.youtube.com/channel/UCdoadna9HFHsxXWhafhNvKw"
channel_follower_count: 176000

# === time ===
duration: 3616
upload_date: 20260515
fetched_at: "2026-05-25T13:06:46+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/LnCXoIr0Mw8/maxresdefault.jpg"

# === content structure ===
chapters: []
chapters_usable: false

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
view_count: 4002
like_count: 114

# === status ===
availability: public
live_status: was_live

# === lifecycle ===
state: active
---

# Build an Agentic GraphRAG System in 1 Hour (MCP + Knowledge Graph) | Databases for AI

## Description

🕵️ Your AI agent shouldn't need a decision tree to decide how to investigate. 

The answers to complex questions often don’t live in a single data source. They span across multiple locations, domains, and vary in structure – tabular, connected, and unstructured, just to name a few.  

Agentic GraphRAG gives your agent a toolkit and lets it choose which source(s) would be best:

🔹 A Neptune MCP server for open-ended knowledge graph exploration 
🔹 Custom domain tools for defined, repeatable, and high-confidence subgraph extraction 
🔹 Auto-generated domain tools to query over unstructured documents  

We demo a fraud detection use case with #AmazonNeptune & #AmazonBedrock, but the architecture works for any domain where your #agenticAI needs to follow leads across structured & unstructured data. 

Stop orchestrating & start letting your agent investigate.

## Transcript

[00:00:00] Heat. Heat. [music]

[00:00:07] [music]

[00:00:14] [music]

[00:00:20] [music]

[00:00:28] >> [music]

[00:00:34] [music]

[00:00:40] >> All right. Hi everyone. Thank you so much for taking the time to join us for another episode in the databases for AI series. Um, so if you are a builder working on building rag applications, maybe you've already started dabbling on the side of graph rag applications or you're just interested in graphs like a lot of us are, then you are in the right place today because we are going to be showing you how to build an

[00:01:12] agentic graph rag system in less than an hour. Uh, so my name is Melissa. I am a Neptune specialist solutions architect and I am going to be your host for today's episode. I am also here with our super special guest Ian. Um if Ian you want to quickly introduce yourself. >> Hello everyone. My name is Ian. Uh I'm a graph architect with the Amazon Neptune service team. >> Awesome. Thank you Ian. Um so yeah as a

[00:01:43] Neptune specialist solutions architect um I get a lot of inquiries from customers uh people using Neptune on everything graph and Neptune related but it feels like lately a lot of the asks and questions that we get are really centered around how do we make our rag applications more accurate? How do we give them more context? How do we kind of capture some of the missing semantics and bits that a pure rag search might

[00:02:14] miss? And so kind of the traditional answer to that has been using graph rag. And just as a little recap, so if you've tuned in to some of our previous episodes on this databases for AI series, you might have seen that we've done some previous episodes covering graph in general. We talked a little bit about graph rag, what is it, why you might need it, when it would be a great fit. Um, and we'll post the links in the

[00:02:44] chat just in case you want to catch up. But just as a really quick recap to kind of set the stage for agentic graph rag, what we're going to be talking to about today, I just wanted to chat a little bit about what graph rag is really quickly. Um so if you're familiar with just your standard rag pipeline um it's actually very similar to how a graph rag architecture would look like. Um so here right we are again still starting with

[00:03:14] our data sources. We're going to load them, chunk them, generate embeddings, stick those embeddings into our vector store, but we're really enriching this process with a graph that will help provide additional context to the flow that helps capture not necessarily similar information, right? It could be dissimilar information, but it can still be relevant to the original question, right? And that's really the value that

[00:03:46] graphreg works. And uh one of my favorite examples that I always like to show of course is our sales prospects in example core. Um and this [clears throat] is a really great simple example that kind of captures the value ad of the graph in the graph rag flow. And as an example here, we might have a repository of articles, about example corp, about the sales, about the distributors that it uses. And right if

[00:04:16] we generate some chunks for it and we're trying to answer this question with the standard vector rag flow right we see that um a chatbot might pull from this do the vector search and we're going to match on the most semantically similar chunks which are going to be these blue ones. Um, and while this is semantically similar and we can derive an answer from this, right, that sales are going to be great, we actually see as a human that

[00:04:43] we're missing some extra context on the bottom. And so these are really the extra bits of information that are crucial and might be missed as part of just a standard vector flow. Um, so I just really wanted to quickly set the stage with that extra context about graph rag because we've been talking a lot about just graph rag as an architecture. We've been talking about more generally how we can connect a

[00:05:08] graph to agents to kind of query graphs with agents, but today we're really going to be putting all of those different components together into what we call agentic graph rag. And so I think that really brings our question to you Ian of on like I feel like graph rag has been such a hot topic lately. Uh we understand kind of generally the gaps that graph rag helps bridge from the standard vector rag but now we're moving

[00:05:39] on to agentic graph rag. So I guess how do you define agentic graph rag and what are the gaps that agentic graph rag covers that graph rag alone might not necessarily address. >> Yeah I think [laughter] agentic graph rag or any agentic solution is is us effectively adding a layer of additional intelligence over the top of our rag solutions. So we're providing some domain expertise. We're actually creating systems that can apply

[00:06:15] some domain expertise to solve really really complex problems. So graph rag out of the box or traditional vector rag there's not a lot of intelligence in there. You know you you said that that graph rag is really really useful in finding some of that super relevant information where we've got to chase down some connections in the data. We can use vector rag to find stuff that's really similar to the question that's

[00:06:38] being asked. We can use the graph to chase down additional connections, find some of that non-obvious content and combine these two sets of information and produce a good answer. So effectively with Rag, we're finding some content and then we're handing it off to an LLM with a prompt and saying, you know, given this evidence, please answer this question. But there's not a lot of intelligence there.

[00:07:03] um we are actually having to build an application or build a set of retrievers that know how to go hunt for that information. Um and then really we're just presenting the LLM with everything that we've found. Well, when we think about how we as experts in the real world solve problems, we tend to adopt a more iterative or incremental approach. We come with a whole bunch of strategies to solve a problem. And so we may start

[00:07:33] solving a specific problem by gathering some information, you know, reviewing what the initial situation looks like and then based out on our understanding of how things stand, we'll pick and choose amongst some other strategies in order then to be able to further develop a solution to the problem. That's how we behave as as real experts. And I think what we're all trying to do today in building uh genai applications

[00:08:01] is incorporate some of those expert behaviors into our systems. And that's where an agentic approach can help where the agent is effectively behaving like an expert. And we're furnishing that agent with a whole set of tools and capabilities and bits of domain knowledge. And then we're saying, "Hey, look, here's a really complex problem that I want you to solve. You work out how you're going to solve it. Take

[00:08:27] advantage of these tools, apply some of this knowledge, this domain knowledge, and come back with the answer." >> And so, in adding Sorry, go on. >> Oh, no. I was just going to say, um, just wanted to jump in quickly with Reginaldo's comments. Um, he brings up a good point about the data freshness. Um I think that is also a common question that we get even in just the regular graph rag flow about how do we keep

[00:08:54] things up to date. So it would be awesome if as we kind of go through this kind of if we could touch on the freshness aspect and then how we keep the graph subsequently up to date as part of this flow as well. >> Yeah. Yeah. I mean that that's that's really important isn't it? Because when we are again as as humans and human experts trying to solve a problem, we want access to the latest information.

[00:09:18] Um and therefore we want to be able to trust that whatever tools or whatever sources of information we have available to us are giving us good honest fresh data. So I think as we go through a few demos we'll we'll talk about ways in which we maintain that data and keep it fresh. Um, but obviously it's it's it's super relevant to be able to produce accurate and timely and comprehensive solutions to problems. We need access to

[00:09:49] that that really relevant information. Yeah. Um, and I think when we talk about agentic graph rag, we're effectively saying as part of an agentic solution, we can add some graph rag capabilities. We can take advantage of an underlying graph and of the ways in which we've represented all the stuff that's of interest to us as a set of connected data. We'll take advantage of that in order to chase down those connections,

[00:10:16] find fresh, relevant, non-obvious information, and allow the agent to take advantage of these capabilities. It's beginning to to work its way iteratively through solving a problem. >> Yeah. >> Awesome. So, this this sounds awesome. Um, I I guess my question would be if I'm starting from kind of ground zero, like I don't I maybe I don't have a graph yet, like what's the easiest way to kind of get this going?

[00:10:47] So I think I'm I'm going to create a very simple distinction between what we might call a knowledge graph and other graph solutions that effectively index textual content. And a knowledge graph on the one hand is uh a very faithful representation of the stuff that's really of interest to us. And what we'll see in a minute is a a demo, a fraud demo where we have a graph data set that represents uh accounts and transactions and bits of

[00:11:23] identity information associated with those accounts. And to get started there, there's actually still quite a bit of effort involved because as a builder, I've got to think, well, what's an ideal representation of my domain? How am I going to model it as a graph? Um, what kinds of questions do I expect to be able to ask and answer out of that graph? There's a bit of upfront information architecture effectively,

[00:11:52] but the end result is I've got a really really powerful data set that rep represents the stuff that I'm really interested in and I can ask some very very complex questions of it. Um, and I think on the Neptune side, we do have some tooling that can help all of our builders get started modeling those domains and creating queries and visualizations of them. But as I say, I'm going to call that a knowledge graph. There's lots of

[00:12:22] different ways of describing knowledge graphs, but that's that's my simple version of it. It's, you know, kind of faithful representation of the stuff in our domain that we're really really interested in. >> Awesome. Separately there is um we'll often have a lot of information in unstructured or semistructured documents in text documents or markdown files or even JSON documents things like that. And one of the easiest ways of getting

[00:12:52] started building firstly a graph rag solution and then an agentic graph rag solution based off this kind of content is to take advantage of either things such as the Neptune bedrock integration that will allow you to automatically ingest all of this data and create a kind of graph rag capability. That's a fully managed uh capability that we offer through Bedrock through Bedrock knowledge bases or and again in one of the demos we'll

[00:13:21] be seeing uh this in a little more detail. We have an opensource graph rag toolkit that will actually allow you to ingest all of those unstructured and semistructured documents. And the toolkit will automatically build for you a graph. It's not a knowledge graph. It's a it's a graph that provides a very powerful index over all of that textual content. Um, and then the toolkit actually provides you then with a query engine

[00:13:49] that allows you to begin to ask questions of your data. And what we'll see a bit later on is how that toolkit also includes some features that will automatically create a set of tools that you can use in an Aentic solution. So if you've got unstructured or semi-structured data, the easiest way to get started is either through Bedrock knowledge bases or via the graph rack toolkit. Um if you're wanting to build

[00:14:17] one of these more highfidelity knowledge like graphs, um there are perhaps some other tools that we can talk about or we can link to at the end of the show that can help you with some of that modeling um and application and information architecture. >> Awesome. And just to kind of jump in on this, um, thank you Reginaldo for your question talking a little bit about how Neptune ties into the architecture that

[00:14:41] Ian was just discussing. So does Neptune have any similarity search capabilities or do you have to map those nodes in an external vector database? So depending on the architecture that you want to build, I think there's a couple options here, right Ian? >> There that there are. Yes. Yeah. [snorts] So um firstly you know for for people watching who aren't necessarily hugely familiar with Neptune just say that

[00:15:09] Neptune is Amazon's managed graph database but actually has two different engines. There's the Neptune database engine which you can think of as uh kind of SQL for it's an online transactional graph database for storing very very large data sets. Um and then separately we have another engine called Neptune Analytics which is a memory optimized graph engine. Neptune Analytics also allows you to store vector

[00:15:40] embeddings as part of the graph. So if you're building a solution that uses Neptune Analytics, you can model all and model everything as a graph, store it in Neptune Analytics. You can also generate embeddings. You have to do that externally perhaps via bedrock, but you can then store those embeddings within the graph. And you can use the graph query languages that we supply with Neptune Analytics to conduct a vector

[00:16:06] similarity search and use that as the starting point for a graph query that then chases down all of those connections in the graph. uh or you can begin a normal graph traversal and then when you find stuff in the graph that you're really interested in, if they have embeddings associated with them or attached to them, you can use that to drive similarity search. So that's one approach. Neptune Analytics allows you

[00:16:30] to combine graph and vector similarity search in the same underlying technology. um a separate approach and this is the the the approach that we've adopted in that open-source toolkit is to create a logical distinction between a graph store and a vector store and then have put APIs over the two of them so that I could query the vector store find stuff that's of interest by way of similarity search and then use those results to

[00:17:02] drive a graph search in the graph And again in the toolkit the toolkit actually supports multiple backends. It supports Neptune database, Neptune Analytics, S3 vectors, open search, uh Postgress with the PG vector extension. Depending upon which of those backends you choose, it may be, you know, if you're using Neptune Analytics, the graph store and the vector store will actually be pointed at the same

[00:17:31] underlying instance. Does that help answer the question? >> Yeah, I think you covered that perfectly. Yeah. So, uh just to summarize, Bedrock knowledge bases graph rag. If I wanted to go that route, I can use that with Neptune Analytics and that would be an all-in-one package. And then if I wanted to mix and match my stores, the graph toolkit would be a good option for that. and it would handle it would

[00:17:59] handle for me the kind of mapping between the nodes in the graph to the corresponding vectors in the open search. So uh yeah it would be handled for me so I don't have to think about that too much >> actually and I think that's a really important point. So you know we we've talked about the Neptune Bedrock integration and the toolkit and in both cases these service on the one hand open source library on the other are doing that

[00:18:26] mapping on your behalf. But if you're building your own graph rag solutions um and you're wanting to combine vector search with graph search you do have to think about how you're going to map backwards and forwards between the two. So the results that returned from a top case similarity search should ideally have some reference to nodes in the graph that you can use to then begin a graph traversal or a graph query.

[00:18:55] >> So I guess when we think about how the graph rag toolkit fits in with a gentic graph rag I I guess I'm mentally trying to figure out like what's the connection if we want to do a gentic graph rag. uh how does that work if we're choosing to use the graph toolkit to build this out? >> So [snorts] um let's let's think about the the the kind of the overall architecture of an agentic solution. As I say, what we're wanting to do here is

[00:19:27] is what you're wanting is to build a system or an application where we've incorporated some domain knowledge, some expertise. we're actually having the system behave like an expert. The way we've done that for decades is to hardcode all of that kind of decision-making logic into the application. But then we find that that's a rather fragile way of solving the problem. It works today really really well as long as we're prepared to

[00:19:57] to to follow those steps. but something out there in your the business changes, some new requirements emerge, and we've got to go and revise and update that all over again. With an agentic solution, we're effectively saying, "Look, here's a an LLM based agent that we're going to furnish or give um some instructions, some domain expertise that describe how it ought to behave. And we're also going to give it some tools that it can use to

[00:20:29] solve the problem. So we're giving it some knowledge and the tools that it can use based on that knowledge and then we're going to let it solve the problem. It's going to work out its own stepby-step approach to solving the problem and it may make a couple of steps forward and come back and solve. The way in which the graph rag toolkit can help here is it can automatically create what I'm calling domainspecific

[00:20:58] tools I tools that are intimately related to the underlying data set and it can expose those tools to the agent. Now many agentic solutions are not only going to have a graph as part of the underlying tool set. They may very well have many other tools that are pointed to other different backends. But where we've introduced the toolkit in order to provide some graph capabilities to the agent, the toolkit

[00:21:30] is making it really really easy to automatically generate tools that are descriptive or representative of our domain. they kind of naturally incorporate lots of knowledge about our domain because the toolkit is automatically introspecting the underlying data and saying hey I think this underlying data set represents a set of uh runbooks or a set of policy documents so hey look I've got a knowledge base or I've got a tool here

[00:22:03] that knows all about runbooks to solve problems x y and zed and we're advertising that to the agent and then the agent given a problem if it thinks it's appropriate to take advantage of that tool those runbooks or those policy documents it will automatically invoke it. So that's how the toolkit is making this stuff really really easy. It's automatically creating tools that you can incorporate into an

[00:22:28] agentic solution. >> Awesome. Cool. So should we check this out in action? I'm super excited to see how this all works. Um, I've worked with the Graphrack toolkit before, but not from the custom domain tool perspective. So, >> right be interested to see how it all comes together. >> Yeah. And so I I think you know when when Melissa and I were discussing how we'd like to to tackle some of these issues previously, we kind of identified

[00:23:02] three different ways in which you can incorporate a graph and graph capabilities into your agentic solutions today. Um so we're going to go through those three different approaches. Um it's not necessarily either or you know that each approach is relevant for a specific set of problems but the great thing about agentic solutions is we can always add more tools. We can always present the agent with more tools. So

[00:23:30] you can actually combine or mix and match the three different approaches that we're going to look at today. So, what we're going to look at first of all are um two examples of building tools that we give to an agent um that are pointed at one of those knowledge graphs. One of those things I was talking about earlier where we've got a really highfidelity representation of a specific domain. somebody has

[00:23:59] actually invested the time to create a good information architecture and have built and populated and kept fresh a data set around a specific domain. And this is going to be a a fraud demo and I think in previous live live streams we've actually used some of the the fraud demo example uh previously. Um, so we'll look at that first. And then the third example is this example where we've got this unstructured and

[00:24:27] semi-structured textual content that we've ingested into the toolkit. And we're going to show how the toolkit just automatically infers, oh, these are the kind of tools that I can create and hand off to an agent. All right. So, I'm going to >> and for those that are interested in following along, uh, we do have all of the examples and some of the fraud examples that Ian is mentioning from the past episodes. Uh, we'll post those

[00:25:00] links into the chat as well, so you will have access to kind of run through all of these on your own as well. So, >> cool. So let's let's start with this uh this this fraud example. Um so here I've just got a simple diagram that illustrates the underlying graph data model for this fraud data set. So I said this is this is somebody's applied some careful information architecture here in order to design a graph model that's

[00:25:32] really really useful for helping identify things like fraud rings. So you can see that in our underlying graph data, we're going to have lots of different accounts um and many transactions where those accounts have transacted with merchants. And each account is associated with one or more bits of identity information. So as we onboard accounts, we'll capture things like a physical address, person's

[00:25:58] date of birth, an email address, and so on. And for the purposes of a fraud demo application, we typically take those bits of identity information and pull them out and represent them as separate nodes because that allows us to find accounts that are sharing multiple bits of identity information. And that's often a key clue that we're looking at people who are or groups of people who are behaving in a

[00:26:28] fraudulent manner. Okay, so that's the underlying data.

[00:26:37] Um, this diagram or this this visualization here um is just showing some small subset of the data that's in our underlying graph. So you can see all of the things that are red here. These are different accounts. Different bits of identity information are in blue. So, we've got things like uh email address, date of birth, telephone number, um and then we've got all the different transactions where those accounts have

[00:27:05] bought services or products from different merchants. So, that's just to give you a sense of the underlying data that we're working with. Okay. Now, the first approach that we can take if we're wanting to incorporate some fraud detection capabilities into our agentic solution or we're building an agentic solution that is responsible for identifying and uh assessing potentially fraudulent behavior. The

[00:27:33] first way we can do that is to create an agent and give it some knowledge. Say, hey, look, you're an agent. you're responsible for detecting fraud and you've got access to a graph database and a graph data set that represents all this information. So, we're being very explicit. We're actually telling the agent something about the underlying data. We're saying when you're given a problem to solve,

[00:28:01] you're free to write whatever query you want against this underlying data in order to solve that problem or to answer a specific question. So we're effectively allowing the agent to act like uh a good data engineer or uh a database specialist. Okay. So that's the first approach we're going to take. Um and to to do that we're going to use uh another piece of software called the Amazon Neptune MCP server.

[00:28:38] So, the Amazon Neptune MCP server available on GitHub Labs. It's really easy to set up and you'll see that that's exactly what I'm doing in this cell here. I'm creating a local instance that's up and running on this notebook instance of the Amazon Neptune MCP server. And I've told that server where my graph database resides. I've given it the graph endpoint of that data set. And so this MCP server can now be offered by way of

[00:29:09] a client to an agent. So very simple code to create a client that will allow an agent to interact with that MCP server. And that MCP server in turn will forward queries to the underlying graph database. The next thing I have here is a prompt. So this is that that prompt that I'm going to give my agent. And you can see we're telling it this is how I want you to behave. You're a fraud investigation

[00:29:42] agent. So we're telling it a little bit about its role. And then we're providing it with some additional guidance. And the interesting thing here is we've got two different kinds of guidance. We've got some guidance about it behaving like a uh a database specialist. We're telling it how to write good graph queries. But the second part of the prompt, we're also giving it a bit of domain expertise around

[00:30:11] the fraud investigation domain. So we're saying when you're asked questions, you should be doing things such as identifying shared resources, things like shared devices, shared IP addresses. You should try and trace transa transaction flows and money movement patterns. So we're we're actually telling in the prompt we're we're giving the agent some domain expertise and we're also giving it some expertise

[00:30:38] about how to behave like a good database specialist. All right. In this cell here, we're then going to create the agent itself. So we create an agent. We give it the tools that are made available by way of that MCP client. And in this case, that Amazon Neptune MCP server exposes a couple of tools. One is a tool that allows you to get the underlying graph schema. And another is a tool that allows you or the agent to

[00:31:12] actually run graph queries. So let's run. Okay. So Oh. Ah, yeah. Didn't can create my prompt, right?

[00:31:36] Let's restart and do this again. >> I love [snorts] Jupyter Notebooks. [laughter] If you all haven't worked with Jupyter Notebooks before, they're a lot of fun. Um if you're curious about the interface that Ian is showing and uh I guess we saw a little bit of a visualization earlier um we actually have this opensource package called graph notebook that's on our GitHub that actually extends the Jupyter notebooks uh with

[00:32:05] some Neptune specific magics that just make it a lot easier to like generate some of the visuals that we saw earlier. Um, so ever since we introduced that, I feel like all of us tend to lean on the notebooks for doing everything Neptune graph related. >> Yeah, it's it's [snorts] pros and cons, but it's a nice interactive environment for experimenting both in terms of writing queries um and taking advantage of a lot

[00:32:30] of that uh software and the SDKs that we make available. Okay, so I've got it running now. So we've created an agent. I've given it the tools that were made available by way of that MCP server. I've given it the prompt with all of that domain expertise in it. And then I've also given it a question. Find accounts linked by shared contact details or devices that indicate a single fraudulent actor. Um, and now this print out here towards

[00:32:59] the top, we can actually see the agent beginning to run. As I say, we want to build agents that behave like experts that iteratively and incrementally begin to solve a problem based on their current understanding of the state of the world. So, it's going to make an initial query, get back some results, interpret those results, decide what to do next, and then potentially run some additional graph queries.

[00:33:24] So, you can see the agent saying, I can help you find those accounts. It initially gets the graph schema just to confirm that the graph looks exactly how we've promised it's going to look and then it begins to run a number of graph queries against the underlying data. And what's happening here is the agent knows enough about the query language that we use against Neptune query language called Open Cipher. it knows enough to

[00:33:51] be able to actually author queries on the fly that it can then run against that underlying data. So you can see how many we've got five queries here I think that it's run one after another gets the results back makes some decisions advances its problem solving a little further runs another query and so on and then finally it presents us with some results. So in the end this is a rag like solution but

[00:34:20] the agent has more interactively sourced all of that evidence and then finally created a response based upon that evidence. So it said here's the the high-risk fraud cluster lots and lots of details even recommended actions that we should take next. Okay. So quite a comprehensive answer and all we had to do was give it the prompt that told it a little bit about the database or the data schema and a little bit of

[00:34:50] knowledge about the the fraud domain. Yeah, I see this as super helpful especially for if I was a fraud investigator from the business side and I don't want to know how to write any graph queries myself then I can just ask natural language questions and get something back which is super cool but also that kind of brings me to the question of how do I prevent malicious people from let's say deleting certain

[00:35:20] data or augmenting the data writing in bad data, things like that, >> right? Um, so I think firstly we have to ensure that uh the tools that we're running and the environments in which they're running have sufficient permissions to be able to get the job done but no more. And one of the things that we'd be really careful of in this kind of context is ensuring that our notebook environment can read the graph but it can't write or

[00:35:53] delete data. Okay. If we're wanting to create an investigative tool where we don't necessarily want to use the tool to create data and we want to pro definitely prevent anybody from deleting data, then we would use IM permissions to ensure that this environment only has the read data permission against the underlying graph. And then those permissions will flow all the way through that MCP server and any query that the agent may come up

[00:36:27] with. And we all know that agents can be quite creative. We know that LLMs can be quite creative and can often try and do things that exceed their responsibilities. But if the agent here were to invent a query that thought perhaps I do need to delete some data and issues a delete request. As long as we've provisioned the environment such that it can only read data that will be refused. >> Okay. So one of the ways here is firstly

[00:36:57] securing the environment in which we're running the agent in order to to prevent it doing anything malicious against the the underlying data. >> Awesome. Also just wanted to jump in here with a couple quick questions from the chat. So Lauren is asking if this is available for us to try out ourselves. So yes, we do have a GitHub repo where we post a lot of samples around Neptune and generative AI which we just posted

[00:37:26] in the link into the chat. So check that repo later this week and we'll have that updated with these examples for you to play around with. Also wanted to bring up a question from Reginaldo which I think is a good transition point as to what we've been talking about around you know once we start moving this flow to production you know can we write the queries ourselves or can we really rely on the

[00:37:53] agent and the LLM to make sure that it comes up with like the logically correct version of someone's natural language question. >> Right. Yeah. I think that that I mean that naturally does lead into the the second demo here where we're going to impose a little more control over the kinds of tools that we expose to the agent. Um but just to emphasize I mean this this MCP client and the the uh the Amazon Neptune MCP server are available

[00:38:22] uh via GitHub and you can install them exactly as I've installed them here. And so you could use these today against your own wellformed graph. If you've got an existing graph database, an existing Neptune graph, you can use this today um in order to have the agent write queries. Um the downside is as we saw the agent was running several different queries. Um I actually have some logging where we

[00:38:50] actually see the underlying queries. And what I sometimes see is that the agent might first author a query where the syntax isn't quite correct >> and it runs it against the database and then it gets a response back and says, "Oh, I'm going to try again and I'm going to modify the query." So, it can be quite hesitant in moving forwards and solving the problem. Um, it's a great way of getting up and running very very

[00:39:13] quickly. But it may be that as we begin to move some of our solutions into production, we want as builders to take a little more control over the kinds of tools that were exposed to the agent and the ways in which those tools behave. So the second example I've got here and this again is running against that underlying fraud data set. But here as an application developer, I've created a couple of very domain specific

[00:39:45] tools. So you can see I've got one here, the tool called find fraud ring candidates and a second one called calculate fraud ring exposure. So these are these look just like normal Python methods and you can and you can see that each method encapsulates a graph query. In this first one, we're running actually a graph algorithm, the Louain graph algorithm in order to find uh potentially fraudulent groups of

[00:40:23] fraudulent actors. and we're returning those results. And this second query, again, it's using the open cipher query language, but given a list of account IDs, it's traversing the graph, finding all of those different transactions, and summing the results. So, this allows us to control exactly the kind of behaviors and the kinds of queries that the agent can run against our underlying data set. So, we've moved some of that knowledge

[00:40:52] from the prompt, which we saw in the first example, back into the code, but we're we're then exposing these methods or these functions as tools to the agent. And again, the key thing about an agentic solution is we're not being overly prescriptive about the order in which the agent performs a process. We're just saying, look, you're this kind of expert. Here's a set of tools that you can use. You think about

[00:41:20] the order in which you want to apply them, which tools you want to use. You pick and choose. You go ahead solve the problem the best way you think appropriate. >> And I also see this um we've got another comment from Assan about if we wanted to integrate to an app like a web app um how can we secure it so queries are synthesized and only valid questions are answered. So this looks like it would be

[00:41:46] a great approach for that because you can have a lot more controls over like what exact queries are being run. It looks like with this. >> Yes. Yeah. I I as a an application developer or a a data engineer um have a lot more control over the kinds of query capabilities that I want to expose to the agent. So I'm definitely not going to include queries here that will change or corrupt the data. I'm not going to

[00:42:13] include any queries that delete data. What it does mean is that I need that graph database expertise though I need to understand the domain, the the graph data model and I also need to know how to author good queries that can effectively implement these kinds of capabilities. With that first solution, we were just letting the agent write the best queries it could come up with in order to solve the problem. Now we've

[00:42:42] moved that responsibility back to me, but I've now created a couple of domain meaningful tools that we can give to the agent and just say, you know, you go ahead solve the problem the way you you see fit. So again, we're going to create a little uh local MCP server. We're going to give it these two tools. >> So the setup is slightly different, >> but we're still creating a client. Go on. Oh, sorry. Uh, Ian, I thought it was

[00:43:12] going to take longer to run some of these steps because we got a couple questions in the chat. I just wanted to pop up really quickly. Um, one was just about the query language. So, um, we're using Open Cipher today, but the Neptune MCP server also supports Gremlin, um, as Neptune database supports both query languages today. So, that >> Yeah, that's that's that that's correct. So if you're using Netune database as

[00:43:38] your underlying graph store, then you have access to both Open Cipher and Gremlin query languages for these kind of property graphs. If you're using Neptune Analytics today, Neptune Analytics supports Open Cipher for querying the uh the property graph data model. So yeah, all the examples that we're using today have been written using Open Cipher. >> Yes. And then one more question from Siobhan Shu asking if we could do this

[00:44:06] agentic graph ragra flow with agent core. So um at the moment I believe we're just showing it running locally. Is that right Ian? >> Yes. Yeah. And again notebooks great place to to experiment. Um give you a very nice interactive environment where I can just build out or or flesh out the skeleton of a an overall solution. But putting this into production, um, I I'd use things like agent core in order to

[00:44:33] to properly host and manage and monitor a lot of the the agentic components within my solution. Um, okay. So, we've created those tools. Um, stood up a server that exposes those tools. Um, this code should look very familiar [snorts] because we're creating an agent. Uh, we're telling it which model we want it to use for its own intelligence. And this is going to be Claude Sonet 4. Uh we're giving it those

[00:45:01] tools. Um we're giving it a very very simple system prompt. You're a helpful assistant. Answer the user question based on the evidence in the search results. This is a very very generic system prompt. But then the problem we're asking it to to solve is please can you identify the largest potential fraud ring and then list its members and calculate its exposure. So we'll create that agent. Oh yeah,

[00:45:27] here we go. So, I'll help you identify the largest potential fraud ring. So, it uses the first tool, tool number one, f find fraud ring candidates. Comes back with some results. Now, let me calculate the exposure for this fraud ring. Okay, so you can see again the agent, it knows the tools that it has at its disposal. It's been given a problem to solve and it chooses the most appropriate tools to help solve that

[00:45:58] problem. Really gave it two tools and it used both tools. But it could be that there are much wider array of fraud detection and fraud analysis tools that we were making available to the server. Okay, so that's the first two demos and that's been running against this fraud data set. And as I mentioned earlier, this is a very well-modeled fraud data set that's pretty representative of a set of accounts and merchants and

[00:46:28] transactions and so on. And we've had two different approaches to being able to build an agentic solution that takes advantage of being able to find all of those connections in the the underlying data. >> Yeah. first approach. >> Oh, sorry, Ian. I I've got a little bit of lag, but um just before we move on from the two examples, I just wanted to kind of quickly tie it back to Reginaldo's comment earlier on the data

[00:46:53] freshness. So, because both of these examples, we are reading from kind of that well structured knowledge graph. In this case, we could have like a separate pipeline that just updates the graph in real time if we wanted to, right? So we don't really have to uh at least from the agent perspective, it doesn't have to care too much about the data freshness because we are just constantly updating the graph.

[00:47:17] >> Yes. Yeah, that that [snorts] that's a really really good point here that um we're building an agent that's pointed at this fraud data set. What's building the fraud data set? Well, there are probably some other parts of an application, other pipelines, other systems that as the organization onboards new accounts begins to add new nodes into the graph, add those bits of identity information and as we learn

[00:47:43] about transactions, as transactions flow um through the organization, again, there'll be some other pipeline or application that's populating and updating the graph. So that's what's you know some other process is ensuring that the graph is constantly up to date. The agent can then do its job knowing that the data it has access to is as fresh as possible. Um okay so we're now going to turn to our third example and this is an example

[00:48:16] that uses the graph rag toolkit something I mentioned earlier. The graph toolkit is an open-source library for building graph enabled Genai applications. The graph toolkit allows you to ingest unstructured and semistructured textual content. So things like PDFs, text files, markdown files, and also some semistructured content. It may be JSON documents, things like that. It allows you to ingest all of this and

[00:48:48] it will automatically build for you a graph that effectively indexes all of this textual content. So we're not building what I called earlier a knowledge graph. We're building a graph what I call a lexical graph which is effectively a fancy graph index over all of that textual content. But the toolkit also exposes a query engine API that allows you to ask natural language questions and then it has some retrieval

[00:49:22] strategies that have been prepopulated with very well-written graph queries to go find all of that relevant textual content. And again, the benefit of using the graph here is we can always use vector search to find the semantically similar information. And that's usually core to answering any good question. But the graph will also help us find some of that non-obvious connected information that lies elsewhere in other documents.

[00:49:51] We can combine all that information to get a very comprehensive answer. All right. So that's what the graph rag toolkit allows you to do. It allows you to build the kind of graph rag application that Melissa was showing at the outset of the the live stream. Now there are a couple of other things in the toolkit that are super useful for us here when we're building agentic solutions. The first is it supports out

[00:50:15] of the box this concept of multi-tenency. So I can create separate lexical graphs completely and wholly distinct from one another in the same underlying graph database. Now you could use that because you've got your own different tenants, different users and they all want their own separate graphs. But another way in which you can use it is to ingest specific kinds of documents or specific domain information into a particular

[00:50:42] tenant. So you're applying a kind of divide and conquer approach so that you have different lexical graphs representing different bodies of textual content. Okay. So multi-tenency allows us to ingest into different lexical graphs in the same underlying instance. So we can divide and conquer based on different uh different kind of bodies of knowledge. The second important feature here is as we're ingesting all of this information,

[00:51:12] we're effectively building to the side a kind of inferred schema for the underlying domain semantics for that data. Right? combined together. This means that we can take that inferred schema. We can sample some of the data and we can automatically generate a description of that graph that we could formulate as a tool description. All right. So the example I've got here is two different data sets in two

[00:51:45] different lexical graphs residing in the same database instance. One of those data sets is information about it's kind of aircraft information. It's information about different light aircraft models, the manufacturers, the history of those different aircraft and so on. That's information that was sourced from Wikipedia. The second data set that I have is a set of air aircraft incident reports from the National Transportation Safety

[00:52:16] Board. So these are kind of semistructured documents that describe aviation incidents that have occurred over the last few years. So you can see these two bodies of information are related but they're somewhat distinct. One is all about the history of the aircraft and the manufacturers and the other is very specific information about specific incidents. So I've previously ingested all of that information using the toolkit into two

[00:52:42] different tenants. Um, what I'm going to show here is that inferred schema for just one of those data sets. So I said as we're ingesting the data, we're actually building to the side this kind of inferred schema for the data. So we can see that what we have are things like aircrafts and facilities and manufacturers and then different kinds of relationships that connect instances of these things. So in the underlying

[00:53:15] data set we will have information about specific aircraft and about specific manufacturers and they'll be connected by way of lots and lots of different relationships. Okay.

[00:53:31] So what I'm going to do here is start an MCP server. And the toolkit has some methods that will automatically create for you an MCP server. When it creates that MCP server, the toolkit introspects all those different lexical graphs, takes the schemas for each graph, samples the data for each graph, and uses that to generate a description of the contents of the graph. So that's just taken place here.

[00:54:09] Let's just grow the screen a bit. I'm going to create a client again that can point to my MCP server. And look, these are the tools that were automatically created on my behalf by the toolkit based on its understanding of the contents of those different graphs. So the first tool is called aircraft and its domain is general aviation and aircraft knowledge base. So it's quite wordy but it gives a kind of

[00:54:45] a detailed description of this is the kind of information that you'll find in this specific knowledge base. And notice it doesn't even describe it as a graph. It just says hey I'm a tool that knows all about aviation and aircraft. And you could use it for doing things such as tracing aircraft lineage and you could use it for ex answering these kinds of questions. So it's just providing some examples to help the

[00:55:12] agent understand when it might be appropriate to use this specific tool. The second tool is called NTSB and this is about again this is a tool that says hey I'm a knowledge base that knows all about aviation safety and accident investigations. So if you want to know about specific incidents, I'm the tool to use. So familiar piece of code again, we're going to create an agent. We're going to give it those tools, the aircraft

[00:55:45] knowledge base and the air aviation incident knowledge base. A very simple system prompt, but quite a complex question that we wanted to answer. What safety issues and accident patterns do Kit Fox series experimental aircraft demonstrate? And how do these compare to the design features and manufacturing specifications provided by Denny Aircraft? I mean, that to me sounds like quite a complex question

[00:56:12] that might require us to delve into both of those data sets and pick and choose and mix and match and marry up lots and lots of bits of information. All right. So what we'll see here, we don't see a lot of details of what's going on behind the scenes, but effectively the agent to answer this particular question is going backwards and forwards taking advantage of both of those tools, asking a question, getting back the

[00:56:45] results, interpreting the results, deciding what it wants to do next, what it needs to learn next, and so on until it feels as though it's satisfactory accumulated enough information to properly answer the question. So it goes backwards and forwards and behind the scenes it's actually asking natural language questions. The agent is posing natural language questions to those knowledge bases because it doesn't

[00:57:06] know that there's a graph behind the scenes. There's no graph query language that it knows of. It's just asking natural language questions. And then we can see here that it's finally accumulated enough information to create a pretty comprehensive answer about the origins and the design and so on. >> Awesome. Yeah, thanks so much Ian for taking us through this demo. I think this really ties together all the

[00:57:34] different pieces. So, uh, the previous two examples we saw with the Neptune MCP server being able to connect that up to more of a structured, uh, knowledge graph. And then here, you know, we could layer on to those previous two examples, another MCP server and set of tools that would expose what the graph toolkit provides for the graph side of things, which I think is super cool. Um, one last question I wanted to put up on the

[00:58:03] screen. um before we start to close out is from William. Uh he's asking what AWS service do we use for the rag vector database. Uh also no worries being late to the party. We'll have all the recordings posted to YouTube and all of our samples are going to be on the GitHub links that we posted uh by this Friday. Um but as far as the vector store here, graph toolkit supports both Neptune analytics which has its own

[00:58:34] vector index or you can also use other vector stores in conjunction with it. Um I'm sorry Ian for your example were you using Neptune database plus something else? >> Uh this is using Neptune Analytics. So Neptune Analytics is both the graph store and the vector store. The toolkit also supports as you say uh other backend vector stores that includes open search postgress with the PG vector extension and S3 vectors. Um and we

[00:59:00] always welcome contributions to add new connectors. >> Awesome. Perfect. >> Thank you. Well, thank you so much Ian for taking the time to show us all of this today. Um before we close out, are there any like last thoughts or closing thoughts you wanted to share with the audience? Um, well, I I liked your term layer. I mean, the point is we're giving you lots of different options for creating tools

[00:59:29] that you can hand over to your agents. You can keep on adding new tools to your agents, not just graphback tools, but others, and those agents become more powerful, more specialized, behave more like experts over time. >> Awesome. Well, with that, um, everyone again, thank you so much for joining us and yeah, thank you Ian for sharing all your knowledge with us and yeah, hope to see you all on next week's episode of

[00:59:58] Databases for AI. Thank you. >> Wonderful. Thank you. Thanks, Melissa. Thanks, everyone.

[01:00:11] >> [music]
