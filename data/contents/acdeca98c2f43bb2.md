# High-performance embedding model inference

**URL:** https://www.baseten.co/resources/guide/high-performance-embedding-model-inference/
**Published:** 2025-10-16T00:00:00.000Z

---

## Summary

The webpage provides a guide on **high-performance embedding model inference**, covering how to make embeddings fast, reliable, and cost-efficient at scale.

It explains:
*   **What embeddings are:** Vector representations of text (or other input) used for semantic similarity, powering applications like semantic search and **RAG (Retrieval-Augmented Generation)**.
*   **Vector Databases:** Specialized systems needed to store and query embeddings efficiently (mentioning Chroma, Pinecone, Qdrant, Weaviate, and vector support in PostgreSQL, MongoDB, etc.).
*   **State-of-the-art models:** Discusses the proliferation of open-source models (like Qwen, Gemma, BGE) and the need for optimized serving infrastructure for production use.
*   **Challenges:** Embedding inference workloads require optimizing for both **high-throughput backfills** (offline indexing) and **low-latency lookups** (online user queries).
*   **Baseten's Solution:** Details the **Baseten Inference Stack**, which includes the high-performance runtime **BEI** (Baseten Embedding Inference), optimized infrastructure (Multi-cloud Capacity Management, autoscaling), the **Baseten Performance Client** (to overcome client-side bottlenecks), and **Baseten Chains** (for multi-step pipelines like RAG).

While the page extensively covers **Vector databases**, **embeddings (new efficient models)**, and **RAG architectures**, it **does not** specifically detail:
*   RAG alternatives
*   Hybrid search
*   Chunking strategies
*   Context window management

No answer found for the specific topics of 'RAG alternatives, hybrid search, chunking strategies, context window management'.

---

## Full Content

High-performance embedding model inference | Guides
Baseten acquires Parsed: Own your intelligence by unifying training and inference.[READ](https://www.baseten.co/blog/parsed-baseten)
[Resources / Guides](https://www.baseten.co/resources/type/guide/)
# High-performance embedding model inference
Embeddings quietly power everything from semantic search to RAG and AI agents. This guide covers how to make them fast, reliable, and cost-efficient at scale.
[
Download now](https://www.datocms-assets.com/104802/1759406466-combined_document_final.pdf?dl=high-performance-embedding-model-inference.pdf)
### Authors
[Philip Kiely](https://www.baseten.co/author/philip-kiely/)
[
Download now](https://www.datocms-assets.com/104802/1759406466-combined_document_final.pdf?dl=high-performance-embedding-model-inference.pdf)
### Share
* []()
* []()
* [](https://www.facebook.com/sharer/sharer.php?u=https://www.baseten.co/resources/guide/high-performance-embedding-model-inference/)
![The complete guide to high-performance embedding model inference](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1759406793-cover-7.png%3Fauto%3Dformat%26fit%3Dcrop%26w%3D800&amp;w=1920&amp;q=75)
## High-performance embedding model inference: How to scale semantic search, RAG, and agents[](#high-performance-embedding-model-inference-how-to-scale-semantic-search-rag-and-agents)
Embedding models are the connective tissue of modern AI systems, powering semantic search, retrieval-augmented generation (RAG), recommender systems, and compound AI agents. From indexing millions of documents to handling a single high-value query in real time, embedding inference performance directly shapes product quality.
When embeddings are slow, search results feel stale. When throughput is low, ingestion pipelines stall. The challenge is clear: deliver both high throughput and low latency in production, without overspending on infrastructure.
This guide shows how to meet those demands, and how Baseten provides the fastest embedding model runtime in production today.
## What are embeddings?[](#what-are-embeddings)
An embedding model transforms a variable-length chunk of text –or another modality of input like an image –into a fixed-length vector representation that captures the semantic meaning of the input. By encoding content into this shared semantic vector space, you can compare the similarity between items with simple math.
The output vectors from embedding models vary in dimensionality, or the count of numbers in the vector, ranging from a few hundred to a few thousand dimensions. Higher-dimensionality vectors store more data, while lower-dimensionality vectors are faster and cheaper to store and process. Most modern embedding models use Matryoshka Representation Learning to enable a single model to encode information at various dimensionalities while retaining as much data as possible in smaller dimensions.
Embedding models are used for more than just RAG. These models and their outputs quietly power everything from upgrading legacy ML systems to building cutting-edge agents.
Embeddings are useful for:
* **Context:**The “R” in “RAG” is retrieval, and embeddings let you retrieve meaningful context for LLM prompts and agentic actions.
* **Memory:**Interface efficiently with memory by shifting information from the context window to a vector store.
* **Personalization:**Build user profiles by embedding data and activity.
* **Search:**Quickly scan massive corpuses for relevant results.
* **Classification:**Categorize items based on semantic similarity, or detect anomalies.
* **Recommender systems:**Recommend similar content or products.
Building these systems takes more than just an embedding model. Once you have generated the embeddings, you need infrastructure to store and query them efficiently. That’s where vector databases come in as specialized systems that support fast nearest-neighbor search across billions of vectors. There are a number of excellent vendor options on the market, from purpose-built vector databases like Chroma, Pinecone, Qdrant, and Weaviate, to vector support within larger ecosystems like AWS, MongoDB, PostgreSQL, and many others.
Just like you need a specialized database for storing and using embeddings, you also need specialized infrastructure for running the models. Previously, ML engineers trained regression and tree-based models for classification and recommendation, and AI engineers relied on techniques like fuzzy string matching and knowledge graph traversal for search.
But with the rise of models like BERT in 2018, language model-based embedding systems took over many of these workloads thanks to their increased accuracy and flexibility. Today, embedding models are often built from the same neural networks that power large language models like Mistral and Qwen, ranging from one to eight billion parameters. But unlike LLMs, embedding models are generally deterministic, taken directly from hidden states rather than sampling for inference.
✕![While embedding models used to be based on smaller architectures, today they often range 1-8B parameters with LLM backbones from families like Mistral and Qwen.](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1759397556-frame-2085653530-1.png%3Fauto%3Dformat%26w%3D1200&amp;w=3840&amp;q=75)While embedding models used to be based on smaller architectures, today they often range 1-8B parameters with LLM backbones from families like Mistral and Qwen.
These larger embedding models require more powerful hardware, especially for high-volume production inference. Where before a tree-based classifier may have run on a modestly-specced CPU, today’s embedding models require GPUs like H100 or B200 for fast inference.
## State-of-the-art open-source embedding models[](#state-of-the-art-open-source-embedding-models)
Embedding models are among the smallest generative AI models by parameter count. This makes them relatively cheap to train, leading to a proliferation of open-source models available on the market.
AI engineers choose open-source models for a wide range of reasons. It often comes down to domain-specific quality, consistently low latency, strong unit economics, and zero platform risk. That last point is especially important for embedding models, where the output of one model is not compatible with other models. So if you build on a closed-source model but lose access due to a deprecation, you’ll have to go through the time and expense of regenerating all of your previous embeddings in a new model.
On quality, open-source embedding models are up to par with closed-source options from vendors like OpenAI and Google Gemini. On top of strong out-of-the-box performance, embedding models’ small size and straightforward architecture make them a great candidate for fine-tuning to improve domain-specific quality. Some teams even train their own frontier embedding models to power search or retrieval within their domain.
Strong starting points in the world of open-source embedding models include:
* **Qwen:**The open-source AI research lab within Alibaba consistently releases excellent general-purpose embedding models in a range of sizes.
* **Gemma:**Embedding models from Google’s open-source Gemma lab offer frontier performance at small sizes.
* **BGE:**The BGE family of embedding models by BAAI (Beijing Academy of Artificial Intelligence) includes reranking in addition to embedding.
* Open-source options from startups like**Nomic**,**Jina**,**MixedBread**, and**ZeroEntropy**, which release multi-modal models and models for specific domains like coding.
While closed-source embedding models from labs like OpenAI are a great way to get started and are cost-effective for low-traffic prototypes and side projects, production applications are better served by open-source models. However, to unlock the benefits of consistent low latency and cost-effective large-scale inference, you need an optimized model serving solution for your open-source or fine-tuned embedding model.
## Why embedding inference is uniquely challenging[](#why-embedding-inference-is-uniquely-challenging)
Embedding inference workloads have unique characteristics compared to serving other models like LLMs. Firstly, embedding inference systems need to support two very different traffic profiles:
1. **High-throughput backfills:**Bulk operations like indexing millions of documents, updating product catalogs, or even preparing data for LLM pre-training.
2. **Low-latency lookups:**Individual user-facing queries for search, retrieval, or recommendation, where every millisecond affects user experience.
Generally, inference performance optimization is discussed in terms of trading off latency for throughput or vice versa. But embedding jobs combine:
* **High concurrency**(thousands of simultaneous requests)
* **Small input size**but high frequency (short text, but lots of it)
* **Small model size**(1-8 billion parameters, but very large memory requirements for batching)
* **Tight SLAs**(especially for search and recommender systems)
While you can build systems that serve this dual profile, let’s first consider how to optimize for each individually.
### Optimizing for offline throughput[](#optimizing-for-offline-throughput)
If you’re configuring a model deployment only for throughput —for example, to support a database backfill by embedding an entire corpus —you mostly care about stability and cost. These “offline” or non-latency-sensitive jobs involve processing billions, or even trillions, of tokens of input data, and their runtime is generally measured in GPU hours rather than wall-clock time.
Some examples of offline embedding model workloads include:
* **Large-scale search**index creation
* **Document corpus embedding**for future retrieval
* **Synthetic data processing**for LLM pre-training
* **Classification**on massive datasets
Throughput optimization is the engineering work required to process this many requests without losing data, as cost-effectively as possible. This includes:
* **Provisioning sufficient hardware**to run the job in a reasonable amount of wall clock time.
* **Batching requests intelligently**to combine as many inputs as possible into each forward pass.
* **Queueing requests and load balancing**across GPUs to ensure that requests are not lost and GPUs don’t crash.
* **Recovering from any issues**that do occur and re-processing any missed requests.
* **Writing efficient and highly parallel client code**to ensure that the inference system is receiving as much traffic as it can handle.
These large offline workloads can take hundreds or thousands of GPU hours for extremely large corpora, so even modest throughput gains can yield huge cost savings.
### Optimizing for online latency[](#optimizing-for-online-latency)
In contrast, other embedding workloads must be optimized for online latency, where the user-facing time between request and response is essential. Throughput still matters, as you may need to support many concurrent users, but consistently low P90/P99 latency is key for online workloads.
Some applications where latency matters most include:
* **Multi-step AI agents**using embeddings as part of real-time actions
* **Real-time semantic search**in customer-facing apps
* **Live content recommendations**
Where latency-sensitive LLM requests are generally measured in hundreds of milliseconds, embedding inference budgets are often just tens of milliseconds, including network latency. Achieving these instant responses requires:
* **Runtime optimizations**to use the most performant engines and kernels for inference.
* **Model quantization**to reduce load on the GPU during inference (done in floating point number formats to avoid loss in quality).
* **Autoscaling infrastructure**to keep latencies low when usage spikes.
At Baseten, we’ve seen all kinds of embedding workloads and developed tooling and expertise on handling everything from large-scale offline jobs to high-concurrency online requests. With the[Baseten Inference Stack](https://www.baseten.co/resources/guide/the-baseten-inference-stack/), we’ve developed the fastest and most scalable platform for running inference on open-source, fine-tuned, and custom-built embedding models.
## How Baseten built the fastest embedding inference stack[](#how-baseten-built-the-fastest-embedding-inference-stack)
Solving for both latency and throughput requires end-to-end optimizations across the stack, from eliminating client code bottlenecks to building performant infrastructure to on-GPU model performance work.
At Baseten, our Inference Stack draws upon years of work on scalable, cloud-agnostic, fault-tolerant infrastructure and runtime optimizations. Together, four pieces of the stack deliver the world’s fastest and highest-throughput embedding inference service:
1. **Baseten Inference-optimized Infrastructure:**The[core set of technologies](https://www.baseten.co/resources/guide/the-baseten-inference-stack/#inference-optimized-infrastructure)powering cloud-agnostic and scalable infrastructure across all model deployments.
2. **Baseten Embeddings Inference (BEI):**Our best-in-class embedding-specific runtime with support for leading open-source model architectures.
3. **Baseten Performance Client:**An open-source client library designed to avoid bottlenecks in running high-throughput embedding workloads.
4. **Baseten Chains:**Our framework for writing multi-step, multi-model compound AI pipelines and reducing latency overhead between steps.
With these tools, you can serve embedding inference for any volume of traffic with incredibly tight latency budgets.
### Baseten Embedding Inference (BEI)[](#baseten-embedding-inference-bei)
[Baseten Embedding Inference (BEI)](https://www.baseten.co/blog/introducing-baseten-embeddings-inference-bei/)is the world’s most performant runtime for LLM-based embedding models. In a benchmark, BEI on B200s achieved 3.3x higher throughput than vLLM and 3.6x higher throughput than TEI running on H100s.
BEI uses TensorRT-LLM’s advanced kernels, FP8 quantization capabilities, and advanced batching with support for both Hopper and Blackwell GPU architectures to achieve the highest possible performance.
✕![BEI has four main components: the model server, tokenizer, batch manager, and TRT-LLM inference engine.](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1759403536-diagram-3-6-edited.png%3Fauto%3Dformat%26w%3D1200&amp;w=3840&amp;q=75)BEI has four main components: the model server, tokenizer, batch manager, and TRT-LLM inference engine.
BEI has four main components:
1. **The model server**processes inputs and outputs and handles any errors. BEI uses the Rust-based frontend service from text-embeddings-inference for this task.
2. **The tokenizer**is a multi-core system responsible for turning requests into tokenized sentences.
3. **The batch manager**packs individual tokenized sentences into batches up to a maximum sequence size, using a scheduling policy to maximize GPU utilization, minimize tail effects, and preserve request order.
4. **The TensorRT-LLM inference engine**runs inference in C++ using tokenized batches and creates embeddings.
Each request flows through all four components on the way in, but skips the tokenizer on the way out as embedding and classification outputs are numerical.
On the infrastructure side, BEI integrates seamlessly with Baseten’s traffic-based autoscaling and asynchronous inference queueing, ensuring smooth handling of traffic spikes, efficient resource use, and graceful spin-down of replicas. This combination of throughput, concurrency, and low latency makes BEI a Pareto improvement for embedding, reranking, classification, and reward models.
### Baseten Inference-optimized Infrastructure[](#baseten-inference-optimized-infrastructure)
At the infrastructure layer, embedding performance is generally based on three factors: hardware provisioning, geo-aware load balancing, and request queueing. In short, we need to ensure that there is a GPU ready to process the request, that the request goes to the right GPU, and that in high-throughput cases, the request can wait if the GPU is full.
#### Multi-cloud Capacity Management[](#multi-cloud-capacity-management)
Multi-cloud capacity management (MCM) is a set of automations, tools, and practices around provisioning and operating compute resources across multiple cloud service providers (CSPs) and regions in a standardized and repeatable manner.
Baseten’s multi-cloud capacity management system:
* Ensures**high uptime**with optional active-active reliability
* Supports the**lowest possible latencies**with multi-region deployments for geographic proximity to end users
* Adheres to**data residency and sovereignty**requirements with region-locked deployments
* Unlocks an optimal customer**cost-performance ratio**
MCM makes siloed compute completely fungible: different clusters, regions, and cloud providers become one elastic, universal cloud. It’s built on years of engineering work to make resource provisioning and allocation identical from provider to provider, despite the unique wrinkles that each CSP has, from networking stacks to exact resource SKUs.
✕![At the core of MCM is a globally consistent orchestration layer built on top of Kubernetes, with a global scheduler and a hub-and-spoke model.](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1759404361-diagram-4-1.png%3Fauto%3Dformat%26w%3D1200&amp;w=3840&amp;q=75)At the core of MCM is a globally consistent orchestration layer built on top of Kubernetes, with a global scheduler and a hub-and-spoke model.
We use MCM to route traffic across 10+ clouds and dozens of regions, optimizing for the closest resources while ensuring uptime. An H100 in`us-east-1`on AWS becomes equivalent to an H100 in`us-west4`on GCP.
#### Autoscaling with fast cold starts[](#autoscaling-with-fast-cold-starts)
Autoscaling is essential to systems like embeddings models with variable traffic. Autoscaling determines:
1. How quickly you can scale to handle a spike in traffic
2. How cost-efficient your hardware usage is when traffic slows back down
To keep latencies low as traffic scales, we need to dynamically allocate additional GPUs as the number of requests exceeds the batch size configured on the model server. For example, if you’re serving Qwen3 Embedding on an H100 GPU with a batch size of 32 requests, but are now seeing 50 requests at a time coming in, you’d want to scale horizontally to a second GPU to avoid queue time increasing request latencies. Of course, when traffic settles back down, you’ll want to automatically spin down that extra replica.
Baseten’s Inference-optimized Infrastructure includes a traffic-based autoscaling system that holds requests in a queue while a new GPU is spun up, then routes those requests across the expanded profile of compute resources. A key component of this system is fast cold starts. New GPU resources need to be online in seconds to smoothly scale against sudden traffic spikes.
#### Large queue support[](#large-queue-support)
When processing a large corpus, we generally need to scale past a single replica. In a traffic-based autoscaling system, we might run in a steady state with a handful of replicas serving production traffic, then get hit with a huge corpus to process.
Baseten’s Inference-optimized Infrastructure includes a queueing system to appropriately handle backpressure to keep everything running, enqueue additional requests as more replicas spin up (with fast cold starts), and distribute load evenly among the system as more replicas come online. Of course, the replicas will need to be gracefully spun down after the spike in usage.
The infrastructure system also supports asynchronous inference for queue processing. With asynchronous inference, you get a response as soon as the request is enqueued. Once the inference output is ready, it’s returned via webhook. This asynchronous setup is ideal for many high-volume offline workloads.
#### Baseten Performance Client[](#baseten-performance-client)
With a high-performance, high-throughput model server, client code can end up the bottleneck in embedding system performance, especially in offline batch jobs. The[Baseten Performance Client](https://www.baseten.co/blog/your-client-code-matters-10x-higher-embedding-throughput-with-python-and-rust/)is a Python library written in Rust that overcomes these bottlenecks by properly parallelizing requests on the client side. The Baseten Performance Client is fully OpenAI-compatible and is a drop-in replacement for the OpenAI SDK, but delivers up to 12x better throughput for large batch embedding workloads.
✕![The Baseten Performance Client achieves 12x faster corpus backfill in an extremely high-volume test.](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1759404956-diagram-9-2.png%3Fauto%3Dformat%26w%3D1200&amp;w=3840&amp;q=75)The Baseten Performance Client achieves 12x faster corpus backfill in an extremely high-volume test.
Traditional Python clients are constrained by the Global Interpreter Lock (GIL), which serializes execution and limits CPU utilization in I/O-heavy scenarios. Even asynchronous approaches like asyncio cannot fully harness multi-core systems at scale.
The Baseten Performance Client removes this bottleneck by using Rust and PyO3 to release the GIL during network-bound tasks. Embedding requests execute on a global Tokio runtime (a high-performance async executor in Rust), allowing true parallelism across CPU cores. The GIL is reacquired only to return results, minimizing Python overhead.
In benchmarks with over 2 million parallel inputs, the Performance Client completed embedding in 1:11 vs. 15+ minutes for the AsyncOpenAI client. It also achieved ≈280% CPU utilization on a 16-core machine, compared to 100% on a single core with Python clients.
Using the Baseten Performance Client, you can ensure that every step of your embedding inference pipeline is fully optimized.
#### Baseten Chains[](#baseten-chains)
Many use cases for embedding models, like agentic memory and RAG, use an embedding model as part of a multi-step, multi-model pipeline. Baseten Chains is a framework for deploying these compound AI workloads on co-located infrastructure with independent component scaling, reducing network overhead in system-wide latency and preventing bottlenecks in autoscaling.
For example, an agent with a memory function that relies on embedding-based retrieval would ordinarily need to wait for the network overhead between the language model, business logic server, and embedding model service. With Chains, each of these components is co-located with appropriate resource allocation, saving dozens or even hundreds of milliseconds of latency and simplifying deployment.
## Conclusion[](#conclusion)
Embedding models are no longer a niche capability; they are the foundation of modern AI applications, powering semantic search, RAG pipelines, personalization engines, recommender systems, and agent memory. But as their importance has grown, so too has the complexity of deploying them in production. The dual demands of high-throughput offline processing and low-latency online inference push traditional infrastructure to its limits.
Baseten’s Inference Stack was purpose-built to meet these challenges. By combining cutting-edge runtime optimizations (BEI), cloud-agnostic multi-region infrastructure, intelligent autoscaling, and high-performance client libraries, Baseten enables organizations to serve embeddings at scale with unparalleled speed, reliability, and efficiency. Whether embedding billions of documents for indexing or delivering millisecond-level results in customer-facing applications, Baseten delivers the fastest runtime and the most cost-effective path to production.
As AI systems evolve toward more complex, multi-step agents and compound pipelines, embeddings will only become more critical. With Baseten, teams can confidently adopt open-source and fine-tuned models, unlock frontier-level performance, and future-proof their applications against platform risk. The result: scalable semantic infrastructure that keeps pace with the speed of innovation.
If you want to learn more about how to run embedding model inference at scale with Baseten, you can[talk to our engineers](https://www.baseten.co/talk-to-us/).
#### Contributors[](#contributors)
A big shout-out and thank you to our contributors:
* [Philip Kiely](https://www.linkedin.com/in/philipkiely/)
* [Michael Feil](https://www.linkedin.com/in/michael-feil/)
Trusted by top engineering and machine learning teams
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1764774959-lockup_horizontal_2d_light.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://cursor.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1764600859-notion_logo_1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.notion.com/)
[![OpenEvidence logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761391-openevidence.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://www.openevidence.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1740008335-664287c9ef936d8ce43517f8_abridge-logo-wordmark-black.webp%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](http://abridge.com)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1752855457-clay-logo-dark-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1200&amp;q=75)](https://www.clay.com/)
[![Gamma logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1747248934-gamma-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://gamma.app/)
[![Writer logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761686-logo-writer.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://writer.com)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663023-zed-industries.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](http://zed.dev)
[![Amp logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1765831248-amp-logo-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://ampcode.com/)
[![Superhuman logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1765300450-superhuman_id2iogfm7h_0-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://superhuman.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1762279283-type-text-format-none-color-off-black-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1200&amp;q=75)](https://www.bland.ai)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662897-logo-descript.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=640&amp;q=75)](https://www.descript.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663073-ambience-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.ambiencehealthcare.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663002-hex.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=828&amp;q=75)](https://hex.tech/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662984-logo-picnic.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://picnichealth.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1724272610-wispr.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://wispr.ai)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1762205905-logo-v3-clickup-light-2.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://clickup.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662959-logo-patreon.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://patreon.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663144-cisco.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://www.cisco.com/)
[![Rime logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761536-rime.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://rime.ai/)
[![Latent Health logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1757530494-8fd7442a5cdce7c96fd35426bf539665159e74a6-edited.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://latenthealth.com/)
[![Praktika AI logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1753418350-praktika-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://praktika.ai/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662918-retool.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=828&amp;q=75)](https://retool.com/ai)
[![Oxen AI logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1762842118-oxen-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://www.oxen.ai)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761178-canopy.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://canopylabs.ai/)
[![Scaled Cognition logo in grayscale](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1764791291-679bbd929b00774d4eb24f4b_scaled-cognition-logo-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.scaledcognition.com/)
[![Aurelio](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1763483655-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://aurelioterminal.com)
[![toby](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1724710988-toby.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://www.trytoby.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663203-logo-robust-intelligence.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.robustintelligence.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758314778-partner-mixedbreadai-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://www.mixedbread.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1764774959-lockup_horizontal_2d_light.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://cursor.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1764600859-notion_logo_1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.notion.com/)
[![OpenEvidence logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761391-openevidence.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://www.openevidence.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1740008335-664287c9ef936d8ce43517f8_abridge-logo-wordmark-black.webp%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](http://abridge.com)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1752855457-clay-logo-dark-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1200&amp;q=75)](https://www.clay.com/)
[![Gamma logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1747248934-gamma-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://gamma.app/)
[![Writer logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761686-logo-writer.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://writer.com)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663023-zed-industries.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](http://zed.dev)
[![Amp logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1765831248-amp-logo-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://ampcode.com/)
[![Superhuman logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1765300450-superhuman_id2iogfm7h_0-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://superhuman.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1762279283-type-text-format-none-color-off-black-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1200&amp;q=75)](https://www.bland.ai)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662897-logo-descript.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=640&amp;q=75)](https://www.descript.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663073-ambience-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.ambiencehealthcare.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663002-hex.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=828&amp;q=75)](https://hex.tech/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662984-logo-picnic.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://picnichealth.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1724272610-wispr.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://wispr.ai)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1762205905-logo-v3-clickup-light-2.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://clickup.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662959-logo-patreon.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://patreon.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663144-cisco.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://www.cisco.com/)
[![Rime logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761536-rime.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://rime.ai/)
[![Latent Health logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1757530494-8fd7442a5cdce7c96fd35426bf539665159e74a6-edited.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://latenthealth.com/)
[![Praktika AI logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1753418350-praktika-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://praktika.ai/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758662918-retool.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=828&amp;q=75)](https://retool.com/ai)
[![Oxen AI logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1762842118-oxen-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://www.oxen.ai)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758761178-canopy.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://canopylabs.ai/)
[![Scaled Cognition logo in grayscale](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1764791291-679bbd929b00774d4eb24f4b_scaled-cognition-logo-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.scaledcognition.com/)
[![Aurelio](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1763483655-logo.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://aurelioterminal.com)
[![toby](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1724710988-toby.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1080&amp;q=75)](https://www.trytoby.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758663203-logo-robust-intelligence.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=1920&amp;q=75)](https://www.robustintelligence.com/)
[![Logo](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1758314778-partner-mixedbreadai-1.png%3Fauto%3Dcompress%252Cformat%26h%3D50&amp;w=3840&amp;q=75)](https://www.mixedbread.com/)
## Related resources
[
Explore resources](https://www.baseten.co/resources/)
Community
#### [Baseten AI Wrapped: 3 trends to help you build better in 2026](https://www.baseten.co/blog/baseten-ai-wrapped-3-trends-to-help-you-build-better-in-2026/)
Amir Haghighat
1other
![Baseten AI Wrapped](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1766189337-base_wrapped.png%3Fauto%3Dformat%26fit%3Dcrop%26h%3D325%26w%3D675&amp;w=3840&amp;q=99)
Event
‌#### [HumanX](https://www.baseten.co/resources/event/humanx/)
![humanx](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1766014148-unnamed-4.png%3Far64%3DMjox%26auto%3Dformat%26fit%3Dcrop%26w%3D750&amp;w=3840&amp;q=99)
Event
‌#### [Low Latency, High Spin Happy Hour](https://www.baseten.co/resources/event/low-latency-high-spin-happy-hour/)
![spin sf](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1766013941-happy-hour-spin-sf.png%3Far64%3DMjox%26auto%3Dformat%26fit%3Dcrop%26w%3D750&amp;w=3840&amp;q=99)
## Explore Baseten today
[
Start deploying](https://login.baseten.co/sign-up)[
Talk to an engineer](https://www.baseten.co/talk-to-us/)
