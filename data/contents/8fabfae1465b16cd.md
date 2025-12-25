# Optimizing RAG with Hybrid Search & Reranking

**URL:** https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking
**Published:** 2025-10-21T00:00:00.000Z

---

## Summary

The webpage focuses on **Optimizing Retrieval-Augmented Generation (RAG) with Hybrid Search and Reranking**.

Here is a summary of the topics mentioned in your query that are covered in the page:

*   **RAG Architectures:** The page discusses how hybrid search enhances the retrieval component in RAG systems.
*   **Hybrid Search:** It explains what hybrid search is (combining keyword/sparse vector search, like BM25, with semantic/dense vector search) and its use cases (handling abbreviations, names, and code snippets better than pure vector search).
*   **Rerankers:** It details the process of semantic reranking to reorder the top-k retrieved results based on relevance scores from transformer models.
*   **Vector Databases & Embeddings:** It mentions that standard RAG uses word embeddings and vector similarity search, and discusses how different vector databases (like ChromaDB and Weaviate) support or require custom setups for hybrid search.
*   **Chunking Strategies:** The implementation example shows the use of `RecursiveCharacterTextSplitter` for chunking documents.

**Topics from your query NOT explicitly detailed:**

*   **New efficient models:** The page uses existing models (like BAAI/bge-base-en-v1.5 for embeddings and Zephyr-7B-Beta for the LLM) but does not focus on *new* efficient model developments.
*   **RAG alternatives:** The page focuses on *optimizing* RAG, not alternatives to the RAG architecture itself.

In essence, the page provides a deep dive into using **Hybrid Search** (combining keyword and vector search) and **Reranking** to improve the retrieval quality within a **RAG** pipeline, using specific **chunking** and **vector database** examples.

---

## Full Content

Optimizing RAG with Hybrid Search &amp; Reranking | VectorHub by Superlinked
[![VectorHub by Superlinked](https://superlinked.com/vectorhub/_next/static/media/vectorhub-logo.d71e47bd.svg)](https://superlinked.com/vectorhub/)
[Building Blocks](https://superlinked.com/vectorhub/building-blocks)[Articles](https://superlinked.com/vectorhub/all-articles)[Tips](https://superlinked.com/vectorhub/all-tips)[Contributing](https://superlinked.com/vectorhub/contributing/contributing)[VDB Comparison](https://superlinked.com/vector-db-comparison/)
[](https://www.reddit.com/r/AskAISearch/)
Search
Subscribe
![](https://superlinked.com/vectorhub/_next/static/media/thick-arrow.99bec954.svg)
Menu
[
![](https://superlinked.com/vectorhub/_next/static/media/superlinked-logo-sm.ed70be12.svg)Explore Full Stack AI Solutions
📚Learn more about Superlinked
](https://www.superlinked.com)
Home
Manifesto
Most Recent
Compare Vector DBs
ContributeSubscribe
Table of Contents
What is Hybrid Search?
Use cases for Hybrid Search
Some limitations
Implementation Architecture
Implementation Example
Taking Hybrid Search Further with Advanced Frameworks
Conclusion
Contributors
Update on Github
Was this helpful?
Copy page
AI Summary
Publication Date:October 22, 2025|
#RAG
|Update on Github
# Optimizing RAG with Hybrid Search &amp; Reranking
## Takeaways
[Watch Summary](https://youtu.be/a6GUS2NfI5Q)
* Hybrid search effectively handles edge cases like GAN abbreviations and person names
* Code search needs both approaches as demonstrated by Stack Overflow&#x27;s semantic + lexical system
* Method balancing through H=(1-α)K+αV formula enables fine-tuned performance
* Ranking refinement through RRF effectively combines results from different methods
* Location and name queries like &quot;Strait of Hormuz&quot; perform better with hybrid approaches
* Database choice impacts implementation - Weaviate offers native hybrid while ChromaDB needs custom setup
Retrieval-Augmented Generation (RAG) is revolutionizing traditional search engines and AI methodologies for information retrieval. However, standard RAG systems employing simple semantic search often lack efficiency and precision when dealing with extensive data repositories. Hybrid search, on the other hand, combines the strengths of different search methods, unlocking new levels of efficiency and accuracy.**Hybrid search is flexible and can be adapted to tackle a wider range of information needs**.
Hybrid search can also be paired with**semantic reranking**(to reorder outcomes) to further enhance performance. Combining hybrid search with reranking holds immense potential for various applications, including natural language processing tasks like question answering and text summarization, even for implementation at a large-scale.
In our article, we&#x27;ll delve into the nuances and limitations of hybrid search and reranking. Though pure vector search is preferable, in many cases hybrid search can enhance the retrieval component in**[RAG (Retrieval Augmented Generation)](retrieval-augmented-generation)**, and thereby deliver impactful and insightful text generation across various domains.
## What is Hybrid Search?
In current Retrieval-Augmented Generation (RAG) systems, word embeddings are used to represent data in the vector database, and vector similarity search is commonly used for searching through them. For LLMs and RAG systems, embeddings - because they capture semantic relationships between words - are generally preferred over keyword-based representations like Bag-of-words (BoW) approaches.
But each of vector similarity search and keyword search has its own strengths and weaknesses. Vector similarity search is good, for example, at dealing with queries that contain typos, which usually don’t change the overall intent of the sentence. However, vector similarity search is not as good at precise matching on keywords, abbreviations, and names, which can get lost in vector embeddings along with the surrounding words. Here, keyword search performs better.
That being said, keyword search is not as good as vector similarity search at fetching relevant results based on semantic relationships or meaning, which are only available via word embeddings. For example, a keyword search will relate the words*“the river bank”*and*“the Bank of America”*even though there is no actual semantic connection between the terms - a difference to which vector similarity search is sensitive. Keyword search would, therefore, benefit from vector search, but the prevailing approach is not to combine them but rather to implement them separately using distinct methodologies.
\*\*In hybrid search - a keyword-sensitive semantic search approach, we combine vector search and keyword search algorithms to \*\*[**take advantage of their respective strengths while mitigating their respective limitations**](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/azure-ai-search-outperforming-vector-search-with-hybrid/ba-p/3929167).
## Use cases for Hybrid Search
Vector similarity search proves to be inadequate in certain scenarios, including:
* Matching abbreviations like GAN or LLaMA in the query and knowledge base.
* Identifying exact words of names or objects, like “Biden” or “Salvador Dali&quot;.
* Identifying exact code snippets in programming languages. (Taking a similarity search approach in such instances is practically useless.)
In such instances, hybrid search is extremely useful. Keyword search guarantees that abbreviations, annotations, names, and code stay on the radar, while vector search ensures that search results are contextually relevant. The new Stack Overflow, for example, has adopted just such an approach.
Stack Overflow has moved from simple lexical search to semantic and hybrid search, leveraging AI to make its search algorithms more powerful. Their earlier approach, which used the[TF-IDF](https://en.wikipedia.org/wiki/Tf–idf)algorithm to match on user search string keywords - including exact code snippets, could miss posts that were relevant but didn&#x27;t contain those exact keywords. Stack Overflow&#x27;s new hybrid search methodology finds semantically relevant content from their corpus, and also matches the exact code entered by the user if necessary. This[significantly improved Stack Overflow&#x27;s search results](https://stackoverflow.blog/2023/07/31/ask-like-a-human-implementing-semantic-search-on-stack-overflow/?source=post_page-----c75203c2f2f5--------------------------------).
## Some limitations
While hybrid search confers advantages in many use cases, it is not a silver bullet. It has limitations, including:
* **Latency**: Hybrid search involves performing two search algorithms, so it may be slower than a semantic search when executing on a large knowledge corpus.
* **Computational Expense**: Developing and customizing models for hybrid search can be computationally expensive. It&#x27;s best to consider hybrid search only if your system requires keyword-backed results.
* **Native Support in Databases**: Not all vector databases support hybrid search. You need to ensure the vector database you choose does.
That being said, there*are*many vector databases that incorporate functions that implement hybrid search - e.g., Pinecone, ElasticSearch, Apache Cassandra, and Weaviate. Check out the[Vector DB Comparison table](https://vdbs.superlinked.com/)to see which vector databases support hybrid search.
## Implementation Architecture
![Hybrid Search Architecture](https://raw.githubusercontent.com/superlinked/VectorHub/main/docs/assets/use_cases/hybrid_search_&amp;_rerank_rag/HybridSearch.png "Fig 1")
The hybrid search algorithm combines keyword search and vector search to retrieve relevant content from a corpus. Let&#x27;s take a look at the**components that make up the architecture of hybrid search**.
### Keyword Search
**Sparse vectors**are vectors with high dimensionality, where most elements are zero. They usually symbolize various language tokens, non-zero values signifying their respective importance. Keyword search is also called**sparse vector search**. The**BM25 (Best Match 25)**algorithm is a popular and effective ranking function employed for keyword matching in embeddings. BM25 finds the most relevant documents for a given query by examining two things:
* How often do the query words appear in each document? (the more, the better)
* How rare are the query words across all the documents? (the rarer, the better)
The BM25 score for documentDDDfor queryQQQis calculated as the sum of the scores for individual query terms. Here&#x27;s the formula for calculating the BM25 score:
BM25(D,Q)=∑q∈QIDF(q)⋅TF(q,D)⋅(k1+1)TF(q,D)+k1⋅(1−b+b⋅∣D∣avgdl)\\text{BM25}(D, Q) = \\sum\_{q \\in Q} \\text{IDF}(q) \\cdot \\frac{\\text{TF}(q, D) \\cdot (k\_1 + 1)}{\\text{TF}(q, D) + k\_1 \\cdot (1 - b + b \\cdot \\frac{|D|}{\\text{avgdl}})}BM25(D,Q)=∑q∈Q​IDF(q)⋅TF(q,D)+k1​⋅(1−b+b⋅avgdl∣D∣​)TF(q,D)⋅(k1​+1)​
where,
* IDF(q)\\text{IDF}(q)IDF(q)denotes inverse document frequency
* TF(q,D)\\text{TF}(q,D)TF(q,D)denotes term frequency
* ∣D∣|D|∣D∣is the document length
* avgdl\\text{avgdl}avgdlis the average document length
* k1k\_1k1​andbbbare tunable constants
Notice that the BM25 algorithm is a refined version of the[TF-IDF(Term-Frequency Inverse-Document Frequency)](https://en.wikipedia.org/wiki/Tf–idf)algorithm.
### Vector Search
**Dense vectors, or embeddings**are arrays with a high number of dimensions, filled predominantly with meaningful, non-zero values. Machine learning frequently employs these to represent the underlying semantics and connections of words in a numerical format, thereby effectively encapsulating their semantic essence. Dense vector search is a method used in semantic search systems for finding similar items in a vector space.
A common approach to vector search is[cosine similarity search](https://en.wikipedia.org/wiki/Cosine_similarity). Cosine similarity is calculated as the result of the dot product of the vectors, normalized by the multiplication of their magnitudes. The nearer the outcome is to 1, the more similar the vectors are.
C(A,B)=cos⁡(θ)=A⋅B∣∣A∣∣⋅∣∣B∣∣C(A,B) = \\cos(\\theta) = \\frac{A \\cdot B}{||A|| \\cdot ||B||}C(A,B)=cos(θ)=∣∣A∣∣⋅∣∣B∣∣A⋅B​
### Combination
The results from each algorithm have to be fused to implement a hybrid search. There are various strategies to combine them and get a score. To balance the keyword search score and vector search score to meet our requirements, we use the following formula:
H=(1−α)K+αVH = (1-\\alpha) K + \\alpha VH=(1−α)K+αV
where,
* HHHis the hybrid search score
* α\\alphaαis the weighted parameter
* KKKis the keyword search score
* VVVis the vector search score
The hybrid score is a pure vector score when αis 1, and a pure keyword score when αis 0.
**Reciprocal Rank Fusion (RRF)**is one of several available methods for combining dense and sparse search scores. RRF ranks each passage according to its place in the keyword and vector outcome lists, and then merges these rankings to generate a unified result list. The RRF score is determined by summing the inverse rankings from each list. Positioning the document’s rank in the denominator imposes a penalty on documents that appear lower in the list.
RRF(d)=∑d∈D1k+r(d)\\text{RRF}(d) = \\sum\_{d \\in D} \\frac{1}{k + r(d)}RRF(d)=∑d∈D​k+r(d)1​
where,
* DDDrepresents the set of documents
* kkkis a constant
* r(d)r(d)r(d)is the rank of documentddd
### Reranking
![Reranking Diagram](https://raw.githubusercontent.com/superlinked/VectorHub/main/docs/assets/use_cases/hybrid_search_&amp;_rerank_rag/Rerank.png "Fig 3")
Typically, algorithms yield top-k matches. But these top-k matches may not always include the relevant sections, or, conversely, not all relevant sections may be within these top-k matches. We can ameliorate this issue by ranking all retrieved content based on a score indicating semantic relevance to the query.
To do this, responses from the retriever must be passed to a**semantic scoring model**. Semantic scoring models are transformer models that take in queries and documents to produce a score in a calibrated range. This reranking process returns a list of documents, sorted according to relevance score, from highest to lowest, and incorporated into the response payload of the query.
## Implementation Example
Let’s test the performance of a normal vector search algorithm and a hybrid search algorithm in various contexts. We will be using[ChromaDB](https://www.trychroma.com/)supported by[LangChain](https://www.langchain.com/)and models from HuggingFace. ChromaDB has no direct implementations for hybrid search, but for clarity, we will create an ensemble in the same way we discussed in the theory.
First, we install and import the required libraries.
```
`!pipinstalllangchain langchain-community rank\_bm25 pypdf unstructured chromadb!pipinstallunstructured[&#x27;pdf&#x27;]unstructured!apt-getinstallpoppler-utils!apt-getinstall-y tesseract-ocr!apt-getinstall-y libtesseract-dev!pipinstallpytesseract!pipinstallbitsandbytes accelerate peft safetensors sentencepiece`
```
Next, we load our document and split it into chunks of the required size.
```
`fromlangchain.document\_loadersimportUnstructuredPDFLoaderfromlangchain.text\_splitterimportRecursiveCharacterTextSplitterfromlangchain.vectorstoresimportChromafromlangchain.embeddingsimportHuggingFaceInferenceAPIEmbeddingsfromlangchain.llmsimportHuggingFaceHubimporttorchfromtransformersimport(AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig,pipeline,)fromlangchainimportHuggingFacePipelinefromlangchain.retrieversimportBM25Retriever,EnsembleRetrieverimportos`
```
Now, we load the PDF document and split it into chunks of the desired length with sufficient overlap. In this step, you can adjust the chunk size based on the length of your document and the requirements of your LLM.
```
`doc\_path=&quot;/content/document.pdf&quot;file=UnstructuredPDFLoader(doc\_path)docs=file.load()`
```
```
`# create chunkssplitter=RecursiveCharacterTextSplitter(chunk\_size=200,chunk\_overlap=30)chunks=splitter.split\_documents(docs)`
```
Next, we create a vector store using the embeddings we obtain from the text.
```
`embeddings=HuggingFaceInferenceAPIEmbeddings(api\_key=HF\_TOKEN,model\_name=&quot;BAAI/bge-base-en-v1.5&quot;)vectorstore=Chroma.from\_documents(chunks,embeddings)`
```
Now, we build the keyword and semantic retrievers separately. For keyword matching, we use the[BM25 retriever](https://python.langchain.com/docs/integrations/retrievers/bm25)from Langchain. By setting k to 3, we’re asking the retriever to return the 3 most relevant documents or vectors from the vector store.
```
`vectorstore\_retreiver=vectorstore.as\_retriever(search\_kwargs={&quot;k&quot;:3})keyword\_retriever=BM25Retriever.from\_documents(chunks)keyword\_retriever.k=3`
```
Now, we create the ensemble retriever, which is a weighted combination of the keyword and semantic retrievers above.
```
`ensemble\_retriever=EnsembleRetriever(retrievers=[vectorstore\_retreiver,keyword\_retriever],weights=[0.3,0.7])`
```
We can modify the**weights**parameter to balance the impact of both search outcomes appropriately as needed. The weight values correspond to**α**and**1-α**, as we discussed above. Here, we have weighted keywords more heavily, with a value of 0.7.
Our RAG pipeline needs an LLM. We utilize a quantized version of[Zephyr-7B-Beta](http://HuggingFaceH4/zephyr-7b-beta)for lightweight and optimized performance.
```
`model\_name=&quot;HuggingFaceH4/zephyr-7b-beta&quot;# function for loading 4-bit quantized modeldefload\_quantized\_model(model\_name:str):&quot;&quot;&quot;model\_name: Name or path of the model to be loaded.return: Loaded quantized model.&quot;&quot;&quot;bnb\_config=BitsAndBytesConfig(load\_in\_4bit=True,bnb\_4bit\_use\_double\_quant=True,bnb\_4bit\_quant\_type=&quot;nf4&quot;,bnb\_4bit\_compute\_dtype=torch.bfloat16,)model=AutoModelForCausalLM.from\_pretrained(model\_name,load\_in\_4bit=True,torch\_dtype=torch.bfloat16,quantization\_config=bnb\_config,)returnmodel# initializing tokenizerdefinitialize\_tokenizer(model\_name:str):&quot;&quot;&quot;model\_name: Name or path of the model for tokenizer initialization.return: Initialized tokenizer.&quot;&quot;&quot;tokenizer=AutoTokenizer.from\_pretrained(model\_name,return\_token\_type\_ids=False)tokenizer.bos\_token\_id=1# Set beginning of sentence token idreturntokenizertokenizer=initialize\_tokenizer(model\_name)model=load\_quantized\_model(model\_name)# specify stop token idsstop\_token\_ids=[0]# build huggingface pipeline for using zephyr-7b-betapipeline=pipeline(&quot;text-generation&quot;,model=model,tokenizer=tokenizer,use\_cache=True,device\_map=&quot;auto&quot;,max\_length=2048,do\_sample=True,top\_k=5,num\_return\_sequences=1,eos\_token\_id=tokenizer.eos\_token\_id,pad\_token\_id=tokenizer.pad\_token\_id,)llm=HuggingFacePipeline(pipeline=pipeline)`
```
Now, we define the hybrid search and semantic search retrievers.
```
`fromlangchain.chainsimportRetrievalQAnormal\_chain=RetrievalQA.from\_chain\_type(llm=llm,chain\_type=&quot;stuff&quot;,retriever=vectorstore\_retreiver)hybrid\_chain=RetrievalQA.from\_chain\_type(llm=llm,chain\_type=&quot;stuff&quot;,retriever=ensemble\_retriever)response=PREFFERED\_CHAIN.invoke(&quot;QUERY&quot;)`
```
Let’s check responses from both retrievers in various contexts. First, we will**query in a general context without keywords, abbreviations, or location filters**.
```
`Query: What are the two strategic challenges that the United States faces according to the National Security Strategy?Semantic SearchResult: According to the given context, the United States faces two strategic challenges as stated in the 2022 National Security Strategy. The challenges are that the post-Cold War era is over, and a competition is underway between major powers to shape what comes next.Hybrid SearchResult: According to the 2022 National Security Strategy, the United States faces two strategic challenges: the end of the post-Cold War era and a competition underway between major powers to shape what comes next, and the recognition that the democratic allies and partners in the Indo-Pacific and Europe are mutually reinforcing and intertwined fates.`
```
Both results are somewhat accurate and satisfactory. Now, let us try again,**this time incorporating abbreviations and name filters**to see how that works.
```
`Query: How did Joe Biden help deepen NATO relationship?Semantic SearchResult: Under Joe Biden&#x27;s leadership, America has deepened its relationship with NATO by responding to global challenges and strengthening NATO, making it stronger and more united than it has ever been, as we look to continue promoting stability, prosperity, and growth.Hybrid SearchResult: Under Joe Biden&#x27;s leadership, the United States has worked to deepen NATO&#x27;s relationship through various means. First, he has emphasized the importance of NATO&#x27;s collective defense commitment, reiterating that the United States will defend every inch of NATO territory, which has helped build trust and confidence among alliance members. Second, Biden has played a key role in modernizing NATO&#x27;s strategies and capabilities to address emerging threats, such as cyber-attacks and hybrid warfare. Third, he has prioritized engagement with key NATO partners, such as Sweden and Finland, to broaden and deepen the transatlantic bond. Fourth, Biden has advocated for increased funding and resources for NATO, which has helped strengthen the alliance&#x27;s military and economic capabilities. Overall, Biden&#x27;s efforts have contributed to a more cohesive and effective NATO, which is better equipped to address global challenges and opportunities.`
```
The results of the hybrid search are more detailed, provide a more comprehensive response, including the names of countries and other specific information. Now,**let’s add specific locations to see how each approach fares**.
```
`Query: How is Strait of Hormuz important in Biden&#x27;s strategy?Semantic SearchResult: The passage doesn&#x27;t explicitly state how the Strait of Hormuz is important in Biden&#x27;s strategy. However, it does mention that the United States and its allies have a shared responsibility to maintain a free and open Indo-Pacific, which includes protecting the freedom of navigation. It is possible that preserving freedom of navigation in this area is also a part of Biden&#x27;s overall strategy for the region.Hybrid SearchResult: Biden&#x27;s strategy emphasizes the importance of ensuring freedom of navigation through the Strait of Hormuz, a waterway located in the Middle East. This strategy aims to prevent any country from dominating the region through military efforts and ensures that there are no efforts to control the waterways. This emphasis on freedom of navigation is crucial for the United States and its allies as a significant portion of the world&#x27;s oil supply passes through this waterway. Any disruption or control of this waterway could have significant economic and geopolitical implications, making Biden&#x27;s strategy to maintain this freedom critical.`
```
The hybrid search appears to perform better in providing a specific and detailed response to the query, whereas the semantic search produced a more generalized interpretation without explicitly addressing the importance of the Strait of Hormuz and a geographical overview of the place.
### Other database options
Our implementation example above uses ChromaDB. Your use case may warrant using a different database. Other databases, for example,[Weaviate DB](https://weaviate.io/),**offer native support and implementation for hybrid search**. Here&#x27;s how you would define the retriever component for hybrid search in Weaviate DB.
```
`fromlangchain.retrievers.weaviate\_hybrid\_searchimportWeaviateHybridSearchRetrieverretriever=WeaviateHybridSearchRetriever(alpha=0.5,# defaults to 0.5, which is equal weighting between keyword and semantic searchclient=client,# keyword arguments to pass to the Weaviate clientindex\_name=&quot;&quot;,# The name of the index to usetext\_key=&quot;&quot;,# The name of the text key to useattributes=[],# The attributes to return in the results)hybrid\_chain=RetrievalQA.from\_chain\_type(llm=llm,chain\_type=&quot;stuff&quot;,retriever=retriever)`
```
The value of the**alpha**parameter in the Weaviate retriever can be adjusted to control the relative impact of semantic and keyword searches.
Because the retrievers created above score the top k responses internally and return the highest-scoring response, we may not always need to perform reranking explicitly. In the event of low accuracy in the retrieved content, you can implement a reranker directly using libraries from Cohere, or build your own custom reranking function. When using a reranker from[Cohere](https://cohere.com/rerank), the following changes should be made in the retriever.
```
`fromlangchain.retrieversimportContextualCompressionRetrieverfromlangchain.retrievers.document\_compressorsimportCohereRerankcompressor=CohereRerank()compression\_retriever=ContextualCompressionRetriever(base\_compressor=compressor,base\_retriever=ensemble\_retriever)hybrid\_chain=RetrievalQA.from\_chain\_type(llm=llm,chain\_type=&quot;stuff&quot;,retriever=compression\_retriever)`
```
## Taking Hybrid Search Further with Advanced Frameworks
While the implementations we&#x27;ve explored demonstrate the power of combining keyword and vector search, building production-ready hybrid search systems often requires handling more complex scenarios. Real-world applications need to seamlessly combine not just text embeddings and keyword matching, but also structured metadata like numerical ratings, categories, timestamps, and user preferences - all while maintaining high performance and relevance.
This is where specialized frameworks like[Superlinked](https://github.com/superlinked/superlinked)become valuable. Superlinked extends the hybrid search concept by enabling you to encode structured and unstructured data together into unified vector representations. Instead of manually balancing keyword and vector search results, you can create custom schema that naturally incorporate multiple data types:
```
`fromsuperlinkedimportframeworkassl# Define schema combining text content with structured metadataclassDocument(sl.Schema):id:sl.IdFieldcontent:sl.Stringcategory:sl.Stringrating:sl.Integertimestamp:sl.Timestampdocument=Document()# Create unified embedding spacescontent\_space=sl.TextSimilaritySpace(text=document.content,model=&quot;all-MiniLM-L6-v2&quot;)category\_space=sl.CategoricalSimilaritySpace(category=document.category)rating\_space=sl.NumberSpace(number=document.rating,min\_value=1,max\_value=5)recency\_space=sl.RecencySpace(timestamp=document.timestamp,period\_time\_unit=sl.TimeUnit.DAY)# Combine into a single index with query-time weight controlsindex=sl.Index([content\_space,category\_space,rating\_space,recency\_space])`
```
This approach eliminates the need for complex result fusion algorithms like RRF, as the different signals are naturally combined during the embedding process itself. The framework also provides production-ready deployment options with REST API servers and integrates with popular vector databases like Redis, MongoDB, and Qdrant.
For teams looking to implement sophisticated hybrid search systems that go beyond basic keyword + vector combinations, frameworks like Superlinked offer a more scalable path from experimentation to production deployment. Talk to our co-founders[here](https://getdemo.superlinked.com/?utm_source=VH_optimizingRAG).
## Conclusion
We&#x27;ve looked at how RAG system performance can be enhanced by using hybrid search along with reranking, as compared with using keyword search or vector search on their own. By combining keyword and vector search into one hybrid method, we can match on keywords in contextually relevant content, achieving more refined responses. Using hybrid search, the retriever&#x27;s higher recall rates permit the LLM to produce higher-quality outputs.
## Contributors
* [Ashish Abraham, author](https://www.linkedin.com/in/ashish-abraham-811a23201/)
* [Mór Kapronczay, contributor](https://www.linkedin.com/in/mór-kapronczay-49447692)
* [Robert Turner, editor](https://robertturner.co/copyedit)
![](https://superlinked.com/vectorhub/_next/static/media/thick-arrow.99bec954.svg)
Stay updated withVectorHub
Subscribe
![arrow](https://superlinked.com/vectorhub/_next/static/media/thick-arrow.99bec954.svg)
Continue Reading
![Build RAG using LangChain &amp; Superlinked](https://innovative-ants-bf39f838ee.media.strapiapp.com/superlinked_langchain_retriever_1740909387.png)
Build RAG using LangChain &amp; Superlinked
Learn to build advanced RAG systems with LangChain &amp; Superlinked. Master multi-space vector indexing...
October 22, 2025
![Migrating from Algolia to Superlinked](https://innovative-ants-bf39f838ee.media.strapiapp.com/algolia_to_superlinked_d0addcf635.png)
Migrating from Algolia to Superlinked
Learn how to migrate from Algolia to Superlinked for advanced semantic search and unified production...
November 26, 2025
![How to get consistent, quality RAG results using Superlinked](https://innovative-ants-bf39f838ee.media.strapiapp.com/How_to_get_consistent_quality_RAG_results_using_Superlinked_3c5cd9cc52.png)
How to get consistent, quality RAG results using Superlinked
In this article, we’ll show you how to improve retrieval quality using the Superlinked library in an...
October 22, 2025
