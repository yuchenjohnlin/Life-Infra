---
id: LnCXoIr0Mw8
url: https://www.youtube.com/watch?v=LnCXoIr0Mw8
title: "Build an Agentic GraphRAG System in 1 Hour (MCP + Knowledge Graph) | Databases for AI"
aliases:
  - Build an Agentic GraphRAG System in 1 Hour (MCP + Knowledge Graph) | Databases for AI
channel: AWS Events
channel_url: https://www.youtube.com/channel/UCdoadna9HFHsxXWhafhNvKw
duration: 3616
upload_date: 20260515
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/LnCXoIr0Mw8/maxresdefault.jpg
view_count: 4002
transcript_file: "[[Learn/10-Raw/youtube/LnCXoIr0Mw8|LnCXoIr0Mw8]]"
type: youtube-digest
state: active
---

# Build an Agentic GraphRAG System in 1 Hour (MCP + Knowledge Graph)

> [!quote]- Source description (cleaned)
> Your AI agent shouldn't need a decision tree to decide how to investigate. The answers to complex questions often don't live in a single data source — they span multiple locations, domains, and structures (tabular, connected, unstructured).
>
> Agentic GraphRAG gives the agent a toolkit and lets it choose which source(s) to use:
> - A Neptune MCP server for open-ended knowledge graph exploration
> - Custom domain tools for defined, repeatable, high-confidence subgraph extraction
> - Auto-generated domain tools to query over unstructured documents
>
> Demo: a fraud-detection use case with Amazon Neptune and Amazon Bedrock. The architecture generalizes to any domain where agentic AI needs to follow leads across structured and unstructured data.

> [!info] Orientation
> An episode in AWS's "Databases for AI" live-stream series, hosted by Melissa (a Neptune specialist solutions architect) with Ian (a graph architect on the Amazon Neptune service team) as guest. The format is a guided conversation around three live Jupyter-notebook demos: a Neptune MCP server letting an agent author its own graph queries, a set of hand-built domain-specific tools, and the open-source `graph-rag-toolkit` auto-generating tools over unstructured content. The level is intermediate — viewers are assumed familiar with vanilla RAG and at least the idea of graph RAG; the episode picks up where prior episodes in the series left off and pushes toward "agentic" patterns built on MCP, Neptune, and Bedrock.

## TL;DR

Agentic graph RAG is graph RAG plus an LLM agent that *decides* how to investigate — picking among graph and vector tools, running queries, interpreting results, and iterating, instead of executing a fixed retriever pipeline. The episode shows three complementary ways to expose a graph to that agent, all via MCP:

- **Let the agent write its own queries.** Point an Amazon Neptune MCP server at a graph database, prompt the agent with the domain and a query-writing style, and it authors OpenCypher on the fly. Fastest path from an existing graph to a working investigator; the trade-off is occasional malformed queries and less control.
- **Hand-build domain-specific tools.** Wrap careful OpenCypher (or graph algorithms like Louvain) in Python functions, expose each as an MCP tool. The developer keeps the query expertise; the agent only decides *which* tool to call and *when*. This is the production handoff.
- **Auto-generate tools from unstructured content.** The open-source `graph-rag-toolkit` ingests PDFs/markdown/JSON into a *lexical graph* (a graph index over text, not a knowledge graph), uses multi-tenancy to keep domains separate, infers a schema per tenant, and emits MCP tools whose descriptions the agent reads to choose between knowledge bases. The agent asks natural-language questions; it never sees the graph.

The throughline: stop hardcoding retrieval logic. Layer graph capabilities as tools an LLM-expert can pick from. Freshness is solved upstream (separate ingestion pipelines keep the graph current); safety is solved by IAM (read-only IAM stops creative agents from issuing destructive queries). The three approaches mix and match — a real system will likely combine a knowledge-graph MCP, custom tools for high-confidence subgraphs, and toolkit-generated tools over docs.

## Chapters

| #            | Chapter                                                                               | Time  | Uploader's chapters |
| ------------ | ------------------------------------------------------------------------------------- | ----- | ------------------- |
| **Part I**   | Framing: from graph RAG to agentic graph RAG                                          |       |                     |
| 1            | [[#1. From graph RAG to agentic graph RAG (00:40)]]                                   | 00:40 | —                   |
| 2            | [[#2. Why agents — experts iterate; hardcoded logic doesn't (05:08)]]                 | 05:08 | —                   |
| 3            | [[#3. Knowledge graphs vs auto-built lexical graphs (10:16)]]                         | 10:16 | —                   |
| 4            | [[#4. Combining vector and graph search in Neptune (14:17)]]                          | 14:17 | —                   |
| 5            | [[#5. Three ways to give a graph to an agent (18:55)]]                                | 18:55 | —                   |
| **Part II**  | Demos against a knowledge graph (fraud)                                               |       |                     |
| 6            | [[#6. Demo 1 — letting the agent author its own Neptune queries (24:27)]]             | 24:27 | —                   |
| 7            | [[#7. Securing the agent: read-only IAM and the case for controlled tools (34:50)]]   | 34:50 | —                   |
| 8            | [[#8. Demo 2 — custom domain-specific tools as the production handoff (38:50)]]       | 38:50 | —                   |
| **Part III** | Demo against unstructured content (toolkit)                                           |       |                     |
| 9            | [[#9. The graph-rag-toolkit, lexical graphs, multi-tenancy, inferred schema (47:43)]] | 47:43 | —                   |
| 10           | [[#10. Demo 3 — auto-generated tools over aircraft and NTSB documents (53:31)]]       | 53:31 | —                   |
| 11           | [[#11. Closing — layer tools, don't replace them (57:34)]]                            | 57:34 | —                   |

---

## 1. From graph RAG to agentic graph RAG (00:40)

The episode opens by recapping what graph RAG is, because agentic graph RAG is built on top of it. A standard RAG pipeline loads data, chunks it, generates embeddings, and stores them in a vector store; at query time it retrieves the semantically nearest chunks and hands them to an LLM. Graph RAG enriches that pipeline with a graph that captures *connections* — information that may not be semantically similar to the question but is still relevant by virtue of how it links to information that is.

The recurring "Example Corp" illustration makes the gap concrete. Asked about Example Corp's sales prospects against a repository of articles, vanilla vector RAG retrieves the chunks most semantically similar to the question — enough to draft a passable answer that sales look great. A human reading the same articles spots additional context further down the page that materially changes the picture; that context isn't semantically close to the question, but it's *connected* to the answer entities through other documents. The graph is what surfaces that connected, non-obvious evidence.

Agentic graph RAG then layers a decision-making agent over that retrieval substrate — and the rest of the episode is about what that layer adds and how to build it.

---

## 2. Why agents — experts iterate; hardcoded logic doesn't (05:08)

Graph RAG, out of the box, has almost no intelligence in the retrieval path. The application or its retrievers go fetch information — vector-similar chunks plus graph-connected chunks — and hand everything to the LLM with a prompt asking it to answer given the evidence. The LLM only writes the final answer; the strategy is hardcoded.

Real experts don't work that way. An expert solving a complex problem picks a strategy, gathers some information, looks at what came back, *then* picks the next strategy based on what they now know. Investigation is iterative and contingent, not a fixed pipeline. Hardcoded retrieval is fragile for the same reason hardcoded business logic is: it works today, but every change to the data or the question shape forces a code change.

An agentic solution moves that expert behaviour inside the system. The agent is given (a) some domain knowledge in its prompt — *you are a fraud investigator, look for shared identity attributes, trace money flows* — and (b) a set of tools it can call. It then works out its own step-by-step approach, calling tools, interpreting results, and deciding what to do next, until it has enough evidence to answer. Agentic *graph* RAG is the special case where some of those tools are graph capabilities.

Data freshness fits naturally into this picture: an expert wants the freshest information available, and the system has to make that promise. The answer in this architecture is to push freshness out of the agent — separate ingestion pipelines keep the graph current, and the agent simply trusts that the data it reads is up to date.

---

## 3. Knowledge graphs vs auto-built lexical graphs (10:16)

There are two very different kinds of graph you might point an agent at, and the choice shapes everything else.

A **knowledge graph** is a faithful, hand-modelled representation of a domain. In the fraud example used later, accounts, transactions, merchants, and identity attributes (email, address, date of birth, phone) are each first-class nodes with deliberate relationships between them. Building one takes upfront information-architecture work: deciding the model, the entities, the relationships, the questions you expect to answer. The payoff is a high-fidelity asset over which you can ask very complex questions — the kind where pulling identity attributes out as their own nodes is what lets you spot accounts sharing multiple bits of identity, a classic fraud-ring signal.

The cheaper starting point is to take the unstructured or semi-structured content you already have — PDFs, text, markdown, JSON — and have something *build a graph for you*. That's what Amazon Bedrock Knowledge Bases (via the Neptune-Bedrock integration) and the open-source `graph-rag-toolkit` both do. The graph they build is not a knowledge graph; Ian calls it a **lexical graph** — a graph index over textual content. It doesn't model your domain in any deliberate way; it indexes your documents in a structure that supports both similarity and connection-following retrieval. The bar to entry is much lower, and for many document-centric use cases it's the right starting move.

The framing matters because the three demos that follow split cleanly on this axis: the first two use the hand-modelled fraud knowledge graph; the third uses the toolkit-built lexical graph over aviation documents.

---

## 4. Combining vector and graph search in Neptune (14:17)

A live-chat question prompts a useful detour into how vector similarity and graph traversal physically combine. Neptune ships two engines. **Neptune Database** is the online-transactional graph for very large data sets — think SQL-for-graphs. **Neptune Analytics** is a memory-optimized engine that *also* stores vector embeddings as nodes' properties, so a single instance can do both jobs: a vector-similarity search to find an interesting starting node, then a graph traversal from there, or vice-versa.

If you don't want everything in one place, the alternative is a logical split — a separate graph store and vector store, with an API layered over both. That's the pattern the `graph-rag-toolkit` adopts, and it supports a range of backends behind the abstraction: Neptune Database, Neptune Analytics, S3 vectors, OpenSearch, Postgres with pgvector. When the backend happens to be Neptune Analytics, both stores collapse to the same instance.

The underlying point: graph-and-vector hybrid retrieval requires a mapping between vector hits and graph nodes. Managed offerings (Bedrock Knowledge Bases, the toolkit) handle that mapping for you. If you build your own, you have to design it — your top-*k* similarity results need a reference back into the graph so you can begin a traversal from them.

---

## 5. Three ways to give a graph to an agent (18:55)

Before diving into demos, Ian sketches the three approaches the rest of the episode will walk through. They aren't mutually exclusive — one of the virtues of an agentic architecture is that you can always layer more tools onto the same agent — and a real system will likely combine them.

1. **MCP server fronting a knowledge graph; the agent writes its own queries.** The Amazon Neptune MCP server exposes two tools (get-schema and run-query) over a Neptune graph. The agent is told the domain and given query-writing guidance; it then authors OpenCypher on the fly to investigate.
2. **Hand-built domain-specific tools over the same knowledge graph.** The developer wraps specific graph queries (and graph algorithms like Louvain community detection) in Python functions, exposes each as an MCP tool, and the agent picks among them.
3. **Auto-generated tools over a toolkit-built lexical graph.** The `graph-rag-toolkit` ingests unstructured content into per-tenant lexical graphs, infers a schema for each, and emits MCP tools whose descriptions tell the agent what each knowledge base knows about.

The choice between (1) and (2) is mostly about *who* owns the query expertise — the LLM or the developer — and how much control you need over what queries hit production. The choice to add (3) is about whether you also need to reason over unstructured documents.

---

## 6. Demo 1 — letting the agent author its own Neptune queries (24:27)

The first demo uses a fraud data set built by careful upstream modelling: accounts and merchants connected by transactions, with each account's identity attributes (email, DOB, phone, address) extracted into their own nodes so that shared attributes across accounts become visible as graph structure — the very thing fraud rings give themselves away by.

The setup is short. A local instance of the Amazon Neptune MCP server (from GitHub Labs) is pointed at the graph's endpoint. A small amount of client code lets the agent talk to it, and the server exposes two tools to the agent: one returns the graph schema, the other runs a graph query against the underlying database.

The prompt does two distinct jobs and the split matters. Half of it makes the agent behave like a competent database engineer — how to write good OpenCypher, what to do when a query fails. The other half is *domain expertise* about fraud investigation: look for shared identity resources (devices, IPs, contact details), trace transaction flows, find money-movement patterns. The agent is being told both *how to query* and *what to look for*.

Given the question — *find accounts linked by shared contact details or devices that indicate a single fraudulent actor* — the agent runs as Ian wanted: it first fetches the schema to confirm the data shape matches its understanding, then issues a sequence of OpenCypher queries, each shaped by the previous result. Five queries later it returns a comprehensive answer: a named high-risk fraud cluster, the linked accounts, the shared attributes that tie them together, and recommended next actions. Crucially, none of those queries were written by a human; the agent authored them from the schema, the prompt, and what it learned along the way.

This is the fastest possible on-ramp: if you already have a well-modelled Neptune graph, you can run this pattern *today* by installing the open-source MCP server and giving the agent a domain-aware prompt.

---

## 7. Securing the agent: read-only IAM and the case for controlled tools (34:50)

Melissa raises the obvious question: if the agent can write any query it wants, what stops a hostile question from coaxing it into deleting or corrupting data? The answer is not in the agent or the prompt — it's in IAM. The MCP server runs in an environment whose IAM permissions are scoped to read-only against the underlying Neptune graph. Even if the LLM, in its creativity, decides a delete would help, the request is refused at the database boundary. The right discipline is the standard one: the agent's environment gets the permissions it needs to do its job and nothing more.

That said, IAM only solves the *integrity* half of the problem. There's a separate concern that motivates Demo 2: the agent is occasionally clumsy. Ian notes that with logging on, you can watch it issue a query with slightly wrong syntax, get an error back, and revise. It eventually gets there, but it's hesitant and chatty — fine for prototyping, less great for production where you'd like predictable behaviour and tighter control over what kinds of queries are even possible.

This is the transition point: the prompt-the-agent-to-write-queries pattern is wonderful for getting started, but once you go to production you'll usually want to pull the query authorship back into the codebase.

---

## 8. Demo 2 — custom domain-specific tools as the production handoff (38:50)

The second demo runs against the same fraud graph but inverts the responsibility split. Instead of the agent writing queries, the developer has written two Python functions and exposed each as an MCP tool. `find_fraud_ring_candidates` runs the Louvain community-detection algorithm to surface potentially fraudulent groups. `calculate_fraud_ring_exposure` takes a list of account IDs and traverses the graph to sum the transaction exposure of those accounts. Each function looks like a normal Python method; each encapsulates a piece of OpenCypher or a graph-algorithm call.

The prompt collapses correspondingly. Where Demo 1 needed both database guidance and fraud-domain guidance, Demo 2 only needs *"you are a helpful assistant — answer based on the evidence."* The fraud-domain knowledge has migrated out of the prompt and into the code; the agent now only has to decide *which* tool to call and *when*. Asked to identify the largest potential fraud ring and calculate its exposure, the agent calls `find_fraud_ring_candidates`, then feeds the result into `calculate_fraud_ring_exposure`, and answers. Two tools were exposed and it used both; in a real system you'd expose a much wider library of fraud-investigation tools and let the agent pick.

This is the production handoff Ian was driving at in the previous chapter. The trade-off is real — you now need someone who understands both the graph model and OpenCypher to author the tools — but in return you control exactly what queries can hit the database, you eliminate the agent's syntax-fumbling, and you make the system's behaviour much more predictable. A live-chat question about exposing this safely to a web app gets the same answer: this pattern, plus IAM read-only, plus only including the queries you actually want to allow, is what makes it deployable.

A brief aside about data freshness ties off the fraud-demo arc: in both Demo 1 and Demo 2 the agent reads from the same knowledge graph, which a separate pipeline keeps up to date as new accounts are onboarded and transactions flow through the organization. The agent never has to think about freshness because the upstream ingestion does.

For hosting beyond a notebook, AgentCore is mentioned as the production target for the agent itself; the notebook environment is fine for experimentation.

---

## 9. The graph-rag-toolkit, lexical graphs, multi-tenancy, inferred schema (47:43)

The third demo shifts to the other graph type — the auto-built lexical graph — using the open-source `graph-rag-toolkit`. The toolkit's core job is to ingest unstructured and semi-structured content (PDFs, text files, markdown, JSON) and automatically build a graph that indexes it. It also ships a query engine with built-in retrieval strategies that combine vector similarity (for the obviously relevant content) with graph traversal (for the non-obvious connected content elsewhere in the corpus).

Two toolkit features are load-bearing for the agentic-graph-RAG story.

The first is **multi-tenancy**. The toolkit lets you create multiple, fully-distinct lexical graphs in the same underlying graph database. The intended use isn't only multi-user isolation; it's a divide-and-conquer pattern where each tenant holds a different body of content — different document types, different domains. One tenant per domain keeps the per-graph indexes focused and lets each become its own "knowledge base."

The second is **inferred schema**. As content is ingested, the toolkit builds a domain-semantic schema for the data on the side. With that schema in hand, plus a sample of the data, the toolkit can automatically generate a human-readable description of what a given lexical graph contains. That description is exactly the shape needed for an MCP tool description — which is how the toolkit can hand the agent ready-to-use tools without the developer writing them.

The demo dataset has two lexical graphs in the same Neptune Analytics instance: one ingested from Wikipedia articles about light aircraft, their manufacturers, and their history; the other from National Transportation Safety Board incident reports. Related but distinct bodies of knowledge — exactly the case multi-tenancy is for. Ian shows the inferred schema for one of them: entities like aircraft, facility, manufacturer, and the relationships connecting them, derived from the ingested data rather than declared by hand.

---

## 10. Demo 3 — auto-generated tools over aircraft and NTSB documents (53:31)

The toolkit provides a method that, in one call, starts an MCP server that introspects every lexical graph in the instance, samples each, and generates a tool per graph with a description shaped by the inferred schema. The two tools that appear in this demo are emphatically not described as graphs: the first calls itself an *aviation and aircraft knowledge base* useful for tracing aircraft lineage, with example questions; the second calls itself an *aviation safety and accident investigations knowledge base*. The agent reads these descriptions and decides which to call — it has no idea there's a graph or a query language behind them.

The question is deliberately cross-cutting: *what safety issues and accident patterns do Kit Fox series experimental aircraft demonstrate, and how do these compare to the design features and manufacturing specifications provided by Denney Aircraft?* Answering it requires evidence from both knowledge bases interleaved. Behind the scenes the agent goes back and forth, posing natural-language questions to each tool, interpreting results, deciding what it needs next, and accumulating evidence until it can produce a comprehensive answer about origins, design, and the specific incident patterns.

Two things are worth dwelling on. First, the agent's interaction with the tools is in natural language — there is no OpenCypher in the loop and the agent doesn't know there could be. The toolkit absorbs the query-language complexity entirely. Second, this composes with the earlier demos: the same agent could just as easily be given the Neptune MCP server's schema-and-query tools and a few hand-built domain-specific tools alongside these auto-generated ones, choosing among all of them per investigation step. The three approaches are layers, not alternatives.

---

## 11. Closing — layer tools, don't replace them (57:34)

The closing thought is short and matches the framing of the whole episode. The three patterns shown are not a ranked menu — they're things you layer. You add tools to your agent; you keep adding more tools as the system matures; the agent becomes more powerful, more specialized, and behaves more like an expert over time. That is the agentic-graph-RAG bet: stop orchestrating the investigation by hand, give the agent a rich enough tool palette, and let it investigate.
