# M3DocRAG : Multi-modal Retrieval is What You Need 
 for Multi-page Multi-document Understanding

**URL:** https://arxiv.org/html/2411.04952v1
**Published:** 2019-01-02T00:00:00.000Z

---

## Summary

The webpage describes **M3DocRAG**, a novel **multi-modal Retrieval-Augmented Generation (RAG) framework** designed for understanding multi-page and multi-document contexts.

Key aspects relevant to your query include:

*   **Vision-Language Models (MLMs) and Multimodal RAG:** M3DocRAG uses a **multi-modal retriever (ColPali)** to find relevant document pages (as images) and then employs a **Multi-modal Language Model (MLM)** (like Qwen2-VL) for question answering based on the retrieved visual and textual information. This contrasts with text-based RAG, which ignores visual elements.
*   **Document Understanding and PDF Parsing:** The framework is designed to handle complex document contexts, including information spread across multiple pages or documents. It processes document pages as **RGB images**, allowing it to inherently handle visual elements.
*   **Chart/Table Extraction:** The framework accommodates various evidence modalities, including **text, chart, and figure**, by operating on the visual representation of the document pages.
*   **Report Generation with LLMs:** The final stage involves using an MLM to **generate the final answer** based on the retrieved multi-modal evidence.
*   **Specific Models Mentioned:** The paper specifically mentions using **ColPali** as the retrieval model and **Qwen2-VL 7B** as the default MLM, achieving state-of-the-art results on several benchmarks. While **GPT-4V, Claude vision, and Gemini** are not explicitly used or detailed as components in the M3DocRAG pipeline described, the framework is designed to be flexible and could potentially integrate them.
*   **Structured Document Output:** The goal is to answer questions accurately, which implies generating structured textual output (the answer), though the paper focuses more on the retrieval and VQA generation process rather than specific structured output formats.

In summary, M3DocRAG is a multi-modal RAG system that leverages vision-language models to overcome the limitations of traditional text-only RAG and single-page VQA systems when dealing with complex, multi-modal, multi-page documents.

---

## Full Content

M3DocRAG: Multi-modal Retrieval is What You Need for Multi-page Multi-document Understanding
# M3DocRAG: Multi-modal Retrieval is What You Need
for Multi-page Multi-document Understanding
Jaemin Cho1Debanjan Mahata2Ozan İrsoy2Yujie He2Mohit Bansal1
1UNC Chapel Hill2Bloomberg
{jmincho,mbansal}@cs.unc.edu{dmahata,oirsoy,yhe247}@bloomberg.netWork done during an internship at Bloomberg as a recipient of the Bloomberg Data Science Ph.D. Fellowship.
###### Abstract
Document visual question answering (DocVQA) pipelines that answer questions from documents have broad applications.
Existing methods focus on
handling single-page documents with multi-modal language models (MLMs),
or
rely on
text-based retrieval-augmented generation (RAG)
that uses text extraction tools such as optical character recognition (OCR).
However, there are difficulties in applying these methods in real-world scenarios:
(a) questions often require information across different pages or documents, where MLMs cannot handle many long documents;
(b) documents often have important information in visual elements
such as figures,
but
text extraction tools
ignore them.
We introduceM3DocRAG,
a novel multi-modal RAG framework that
flexibly accommodates
various document contexts (closed-domain and open-domain),
question hops (single-hop and multi-hop),
and evidence modalities (text, chart, figure,*etc*.).M3DocRAGfinds relevant documents and answers questions using a multi-modal retriever and an MLM, so that it can efficiently handle single or many documents while preserving visual information.
Since previous DocVQA datasets ask questions in the context of a specific document,
we also presentM3DocVQA, a new benchmark for evaluating open-domain DocVQA over 3,000+ PDF documents with 40,000+ pages.
In three benchmarks (M3DocVQA/MMLongBench-Doc/MP-DocVQA),
empirical results show thatM3DocRAGwith ColPali and Qwen2-VL 7B
achieves superior performance than many strong baselines, including state-of-the-art performance in MP-DocVQA.
We provide comprehensive analyses of different indexing, MLMs, and retrieval models.
Lastly, we qualitatively show thatM3DocRAGcan successfully handle various scenarios, such as when relevant information exists across multiple pages and when answer evidence only exists in images.
![Refer to caption](x1.png)Figure 1:Comparison of multi-modal document understanding pipelines.
Previous works focus on(a) Single-page DocVQAthat cannot handle many long documents
or(b) Text-based RAGthat ignores visual information.
Our(c)M3DocRAGframework
retrieves relevant documents and answers questions using multi-modal retrieval and MLM components, so that it can efficiently handle many long documents while preserving visual information.
## 1Introduction and Background
Document visual question answering (DocVQA)> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> , [> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> , [> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> , [> 14
](https://arxiv.org/html/2411.04952v1#bib.bib14)> , [> 31
](https://arxiv.org/html/2411.04952v1#bib.bib31)> ]
is a multi-modal task that answers textual questions by interpreting information contained within document images.
Existing methods on DocVQA
either focus on
visual question answering (VQA) on a single-page document ([Fig.1](https://arxiv.org/html/2411.04952v1#S0.F1)(a))
or
extract text from documents
(*e.g*., via optical character recognition (OCR)> [
[> 53
](https://arxiv.org/html/2411.04952v1#bib.bib53)> , [> 43
](https://arxiv.org/html/2411.04952v1#bib.bib43)> ]
or PDF text extraction> [
[> 49
](https://arxiv.org/html/2411.04952v1#bib.bib49)> , [> 18
](https://arxiv.org/html/2411.04952v1#bib.bib18)> ]
)
and use retrieval-augmented generation (RAG)> [
[> 35
](https://arxiv.org/html/2411.04952v1#bib.bib35)> ]
,
where a retrieval model finds relevant paragraphs and
a language model answers questions given the paragraphs ([Fig.1](https://arxiv.org/html/2411.04952v1#S0.F1)(b)).
However, there are difficulties in applying these methods in real-world document understanding scenarios:
(a) questions often require information across different pages or documents, where existing VQA methods cannot handle many long documents;
(b) some documents feature complex visual formats such as tables, charts, and mixed layouts,
but text extraction methods such as OCR
ignore these nuances,
leading to incomplete or inaccurate document interpretations. Accurately and efficiently answering questions across numerous, lengthy documents with intricate layouts would greatly benefit many domains such as finance, healthcare, and law, where document AI assistants can streamline the daily processing of large volumes of documents, improving productivity and enabling faster, more informed decision-making.
![Refer to caption](x2.png)Figure 2:Comparison of existing DocVQA datasets (left;*e.g*., DocVQA> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> ]
) and ourM3DocVQAdataset (right).
In contrast to previous DocVQA datasets that have questions that are specific to a single provided PDF (*e.g*., “What was the gross profit in the year 2009?”),M3DocVQAhas information-seeking questions that benchmark open-domain question answering capabilities across more than 3,000 PDF documents (*i.e*., 40,000+ pages).
To overcome these limitations of existing DocVQA approaches,
we
introduceM3DocRAG(Multi-modalMulti-pageMulti-DocumentRetrieval-AugmentedGeneration;[Sec.2](https://arxiv.org/html/2411.04952v1#S2)),
a novel multi-modal RAG framework that
flexibly accommodates
various document contexts (closed-domain and open-domain),
question hops (single-hop and multi-hop),
and evidence modalities (text, chart, figure,*etc*.).
As illustrated in[Fig.1](https://arxiv.org/html/2411.04952v1#S0.F1)(c), theM3DocRAGframework
retrieves relevant document pages using a multi-modal retrieval model, such as ColPali> [
[> 17
](https://arxiv.org/html/2411.04952v1#bib.bib17)> ]
, and
generates answers to questions from the retrieved pages using a multi-modal language model (MLM), such as Qwen2-VL> [
[> 59
](https://arxiv.org/html/2411.04952v1#bib.bib59)> ]
.M3DocRAGoperates in three stages:
In (1) document embedding ([Sec.2.1](https://arxiv.org/html/2411.04952v1#S2.SS1)), we convert all document pages into RGB images and extract visual embeddings (*e.g*., via ColPali) from the page images.
In (2) page retrieval ([Sec.2.2](https://arxiv.org/html/2411.04952v1#S2.SS2)), we retrieve the top-K pages of high similarity with text queries (*e.g*., MaxSim operator for ColPali).
For the open-domain setting,
we create approximate page indices, such as inverted file index (IVF)> [
[> 52
](https://arxiv.org/html/2411.04952v1#bib.bib52)> , [> 66
](https://arxiv.org/html/2411.04952v1#bib.bib66)> ]
, for faster search.
In (3) question answering ([Sec.2.3](https://arxiv.org/html/2411.04952v1#S2.SS3)), we conduct visual question answering with MLM to obtain the final answer.
Please also see[Fig.3](https://arxiv.org/html/2411.04952v1#S1.F3)for the detailed illustration of the framework.M3DocRAGcan flexibly handle DocVQA in both closed domain (*i.e*., a single document) and
open-domain (*i.e*., a large corpus of documents) settings.
![Refer to caption](x3.png)Figure 3:OurM3DocRAGframework ([Sec.2](https://arxiv.org/html/2411.04952v1#S2)) consists of three stages:
(1) document embedding ([Sec.2.1](https://arxiv.org/html/2411.04952v1#S2.SS1)),
(2) page retrieval ([Sec.2.2](https://arxiv.org/html/2411.04952v1#S2.SS2)),
and (3) question answering ([Sec.2.3](https://arxiv.org/html/2411.04952v1#S2.SS3)).
In(1) document embedding, we extract visual embedding (with ColPali) to represent each page from all PDF documents.
In(2) page retrieval, we retrieve the top-K pages of high relevance (MaxSim scores) with text queries.
In an open-domain setting, we create approximate page indices for faster search.
In(3) question answering, we conduct visual question answering with multi-modal LM (*e.g*.Qwen2-VL) to obtain the final answer.
WhileM3DocRAGframework supports DocVQA in an open-domain setting,
the existing DocVQA datasets are not adequate for this setting, since their questions are in the context of a specific document, such as “What was the gross profit in the year
2009?”> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> , [> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> , [> 14
](https://arxiv.org/html/2411.04952v1#bib.bib14)> , [> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
, as illustrated in[Fig.2](https://arxiv.org/html/2411.04952v1#S1.F2)(left).
Hence, we also introduceM3DocVQA(Multi-modalMulti-pageMulti-DocumentVisualQuestionAnswering), an open-domain dataset that significantly raises the challenge of DocVQA to answering questions from a large document corpus
([Sec.3](https://arxiv.org/html/2411.04952v1#S3)).
By extending the MultimodalQA dataset’s> [
[> 54
](https://arxiv.org/html/2411.04952v1#bib.bib54)> ]
closed-domain context to an open-domain setting,M3DocVQAintroduces 2,441 multi-hop questions spanning 3,368 PDF documents, which collectively contain over 41,005 pages of diverse multi-modal content, including text, images, and tables. This dataset presents real-world challenges by requiring models to navigate complex reasoning paths across pages and within various types of document elements, better reflecting the intricacies of document understanding.
To demonstrate the effectiveness ofM3DocRAG,
we compareM3DocRAGwith state-of-the-art baselines
in three benchmarks:M3DocVQA,
MMLongBench-Doc> [
[> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
,
and MP-DocVQA> [
[> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> ]
,
which cover both open-domain ([Sec.5.1](https://arxiv.org/html/2411.04952v1#S5.SS1)) and closed-domain ([Sec.5.2](https://arxiv.org/html/2411.04952v1#S5.SS2)) DocVQA settings.
Experiment results show thatM3DocRAGwith ColPali and Qwen2-VL 8B
achieves superior performance than many strong baselines,
including the state-of-the-art performance in MP-DocVQA.
We also provide a comprehensive analysis ([Sec.5.3](https://arxiv.org/html/2411.04952v1#S5.SS3)) about different indexing, MLMs, and retrieval components.
Finally, we show qualitative examples ([Sec.5.4](https://arxiv.org/html/2411.04952v1#S5.SS4)) whereM3DocRAGcan successfully handle various scenarios, such as when the relevant information exists across multiple pages and when answer evidence only exists in images.
Overall,M3DocRAGis an effective, efficient, and flexible framework for answering questions from multi-modal documents in various settings.
## 2M3DocRAG: A Unified Framework for Multi-modal, Multi-page, Multi-document Understanding
We proposeM3DocRAG,
a novel multi-modal RAG framework that
flexibly accommodates
various document contexts (closed-domain and open-domain),
question hops (single-hop and multi-hop),
and evidence modalities (text, chart, figure,*etc*.).
As illustrated in[Fig.3](https://arxiv.org/html/2411.04952v1#S1.F3),M3DocRAGoperates in three stages:
(1) encoding document images into visual embeddings ([Sec.2.1](https://arxiv.org/html/2411.04952v1#S2.SS1)),
(2) retrieving relevant document pages ([Sec.2.2](https://arxiv.org/html/2411.04952v1#S2.SS2)),
and (3) generating answers to questions based on the retrieved pages ([Sec.2.3](https://arxiv.org/html/2411.04952v1#S2.SS3)).
Below, we explain the problem definition and the details of each stage.
#### Problem definition.
We define a corpus of documents asC={D1,D2,…,DM}𝐶subscript𝐷1subscript𝐷2…subscript𝐷𝑀C=\\{D\_{1},D\_{2},\\dots,D\_{M}\\}italic\_C = { italic\_D start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , italic\_D start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT , …, italic\_D start\_POSTSUBSCRIPT italic\_M end\_POSTSUBSCRIPT }, whereM𝑀Mitalic\_Mis the total number of documents, and each documentDisubscript𝐷𝑖D\_{i}italic\_D start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPTconsists of a set of pages,Pisubscript𝑃𝑖P\_{i}italic\_P start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT, represented as RGB images. From the documents inC𝐶Citalic\_C, we construct a global set of page imagesP=⋃i=1MPi={p1,p2,…,pN}𝑃superscriptsubscript𝑖1𝑀subscript𝑃𝑖subscript𝑝1subscript𝑝2…subscript𝑝𝑁P=\\bigcup\_{i=1}^{M}P\_{i}=\\{p\_{1},p\_{2},\\dots,p\_{N}\\}italic\_P = ⋃start\_POSTSUBSCRIPT italic\_i = 1 end\_POSTSUBSCRIPT start\_POSTSUPERSCRIPT italic\_M end\_POSTSUPERSCRIPT italic\_P start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT = { italic\_p start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , italic\_p start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT , …, italic\_p start\_POSTSUBSCRIPT italic\_N end\_POSTSUBSCRIPT }, where eachpjsubscript𝑝𝑗p\_{j}italic\_p start\_POSTSUBSCRIPT italic\_j end\_POSTSUBSCRIPTrepresents an individual page image, andN𝑁Nitalic\_Nis the total number of page images across all documents inC𝐶Citalic\_C(*i.e*.,N=∑i=1M|Pi|𝑁superscriptsubscript𝑖1𝑀subscript𝑃𝑖N=\\sum\_{i=1}^{M}|P\_{i}|italic\_N = ∑start\_POSTSUBSCRIPT italic\_i = 1 end\_POSTSUBSCRIPT start\_POSTSUPERSCRIPT italic\_M end\_POSTSUPERSCRIPT | italic\_P start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT |). The objective ofM3DocRAGis to accurately answer a given questionq𝑞qitalic\_qusing the multi-modal information
available in the corpus of documentsC𝐶Citalic\_C.
First,
we
identifyPKqsubscriptsuperscript𝑃𝑞𝐾P^{q}\_{K}italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPT,
the topK𝐾Kitalic\_K(≪Nmuch-less-thanabsent𝑁\\ll N≪ italic\_N) pages that are most relevant to answering the queryq𝑞qitalic\_qfrom the global page setP𝑃Pitalic\_P.
Then, we obtain the final answer with a question answering model that takes retrieved page imagesPKqsubscriptsuperscript𝑃𝑞𝐾P^{q}\_{K}italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPTand queryq𝑞qitalic\_qas inputs.
The problem of question answering can be categorized into two settings with different document context sizes:
Closed-domain question answering– The queryq𝑞qitalic\_qshould be answerable from a given single documentDisubscript𝐷𝑖D\_{i}italic\_D start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT. The retrieval model outputs the topK𝐾Kitalic\_Krelevant page imagesPKqsubscriptsuperscript𝑃𝑞𝐾P^{q}\_{K}italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPT, from the page imagesPisubscript𝑃𝑖P\_{i}italic\_P start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPTof the documentDisubscript𝐷𝑖D\_{i}italic\_D start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT.
Open-domain question answering–
The queryq𝑞qitalic\_qmay require information from single or multiple documents within the entire document corpusC𝐶Citalic\_C.
The retrieval model outputs the topK𝐾Kitalic\_Krelevant page imagesPKqsubscriptsuperscript𝑃𝑞𝐾P^{q}\_{K}italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPTfrom the entire set of page imagesP𝑃Pitalic\_P.
### 2.1Document Embedding
InM3DocRAG, both textual queryq𝑞qitalic\_qand page imagesP𝑃Pitalic\_Pare projected into a shared multi-modal embedding space using ColPali> [
[> 17
](https://arxiv.org/html/2411.04952v1#bib.bib17)> ]
.
ColPali is a multi-modal retrieval model based on a late interaction mechanism, which encodes the text and image inputs into unified vector representations and retrieves the topK𝐾Kitalic\_Kmost relevant images.
ColPali adopts both training objective and similarity scoring from ColBERT> [
[> 29
](https://arxiv.org/html/2411.04952v1#bib.bib29)> , [> 50
](https://arxiv.org/html/2411.04952v1#bib.bib50)> ]
, which utilizes a shared architecture to encode either textual or visual inputs. In our framework, each pagep⊆Pi𝑝subscript𝑃𝑖p\\subseteq P\_{i}italic\_p ⊆italic\_P start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPTof a documentDisubscript𝐷𝑖D\_{i}italic\_D start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPTis treated as a single image with fixed dimensions (width×\\times×height).
From an image of a page, we extract a dense visual embeddingEp∈ℝnv×dsuperscript𝐸𝑝superscriptℝsuperscript𝑛𝑣𝑑E^{p}\\in\\mathbb{R}^{n^{v}\\times d}italic\_E start\_POSTSUPERSCRIPT italic\_p end\_POSTSUPERSCRIPT ∈blackboard\_R start\_POSTSUPERSCRIPT italic\_n start\_POSTSUPERSCRIPT italic\_v end\_POSTSUPERSCRIPT ×italic\_d end\_POSTSUPERSCRIPT, wherenvsuperscript𝑛𝑣n^{v}italic\_n start\_POSTSUPERSCRIPT italic\_v end\_POSTSUPERSCRIPTrepresents the number of visual tokens per page (which remains constant across all pages), andd𝑑ditalic\_ddenotes the embedding dimension (*e.g*., 128). For a textual queryq𝑞qitalic\_q, we similarly obtain an embeddingEq∈ℝnq×dsuperscript𝐸𝑞superscriptℝsuperscript𝑛𝑞𝑑E^{q}\\in\\mathbb{R}^{n^{q}\\times d}italic\_E start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT ∈blackboard\_R start\_POSTSUPERSCRIPT italic\_n start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT ×italic\_d end\_POSTSUPERSCRIPT, wherenqsuperscript𝑛𝑞n^{q}italic\_n start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPTis the number of text tokens.
For efficiency, we treat each page of a document independently. This allows us to flatten all pages in the document corpusC𝐶Citalic\_Cinto a single page-level embedding tensor:EC∈ℝN×nv×dsuperscript𝐸Csuperscriptℝ𝑁superscript𝑛𝑣𝑑E^{\\text{C}}\\in\\mathbb{R}^{N\\times n^{v}\\times d}italic\_E start\_POSTSUPERSCRIPT C end\_POSTSUPERSCRIPT ∈blackboard\_R start\_POSTSUPERSCRIPT italic\_N ×italic\_n start\_POSTSUPERSCRIPT italic\_v end\_POSTSUPERSCRIPT ×italic\_d end\_POSTSUPERSCRIPT, whereN𝑁Nitalic\_Nrepresents the total number of pages in the entire document corpus,nvsuperscript𝑛𝑣n^{v}italic\_n start\_POSTSUPERSCRIPT italic\_v end\_POSTSUPERSCRIPTis the number of visual tokens per page, andd𝑑ditalic\_dis the embedding dimension.M3DocRAGcan flexibly adapt to different retrieval settings, such as a single-page document (N=1𝑁1N=1italic\_N = 1), a single document with multiple pages (*e.g*.N=100𝑁100N=100italic\_N = 100),
and a large corpus of multi-page documents (*e.g*.N&gt;1,000𝑁1000N&gt;1,000italic\_N &gt;&gt; 1 , 000).
### 2.2Page Retrieval
The relevance between the queryq𝑞qitalic\_qand the pagep𝑝pitalic\_pis computed using theMaxSimscores⁢(q,p)𝑠𝑞𝑝s(q,p)italic\_s ( italic\_q , italic\_p ):
|s⁢(q,p)=∑i=1nqmaxj∈[nv]⁡Ei,⋅q⋅Ej,⋅p𝑠𝑞𝑝superscriptsubscript𝑖1superscript𝑛𝑞subscript𝑗delimited-[]superscript𝑛𝑣⋅subscriptsuperscript𝐸𝑞𝑖⋅subscriptsuperscript𝐸𝑝𝑗⋅s(q,p)=\\sum\_{i=1}^{n^{q}}\\max\_{j\\in[n^{v}]}E^{q}\_{i,\\cdot}\\cdot E^{p}\_{j,\\cdot}italic\_s ( italic\_q , italic\_p ) = ∑start\_POSTSUBSCRIPT italic\_i = 1 end\_POSTSUBSCRIPT start\_POSTSUPERSCRIPT italic\_n start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT end\_POSTSUPERSCRIPT roman\_max start\_POSTSUBSCRIPT italic\_j ∈[ italic\_n start\_POSTSUPERSCRIPT italic\_v end\_POSTSUPERSCRIPT ] end\_POSTSUBSCRIPT italic\_E start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_i , ⋅end\_POSTSUBSCRIPT ⋅italic\_E start\_POSTSUPERSCRIPT italic\_p end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_j , ⋅end\_POSTSUBSCRIPT||
where⋅⋅\\cdot⋅denotes the dot product, andEi,⋅∈ℝdsubscript𝐸𝑖⋅superscriptℝ𝑑E\_{i,\\cdot}\\in\\mathbb{R}^{d}italic\_E start\_POSTSUBSCRIPT italic\_i , ⋅end\_POSTSUBSCRIPT ∈blackboard\_R start\_POSTSUPERSCRIPT italic\_d end\_POSTSUPERSCRIPTdenotes thei𝑖iitalic\_i-th row (vector) of the embedding matrixE∈ℝn×d𝐸superscriptℝ𝑛𝑑E\\in\\mathbb{R}^{n\\times d}italic\_E ∈blackboard\_R start\_POSTSUPERSCRIPT italic\_n ×italic\_d end\_POSTSUPERSCRIPT.
We then identifyPKqsubscriptsuperscript𝑃𝑞𝐾P^{q}\_{K}italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPT,
the topK𝐾Kitalic\_K(≪Nmuch-less-thanabsent𝑁\\ll N≪ italic\_N) pages that
are most relevant to answering the queryq𝑞qitalic\_q;*i.e*.we searchK𝐾Kitalic\_Kpages scoring highests⁢(q,p)𝑠𝑞𝑝s(q,p)italic\_s ( italic\_q , italic\_p ).
That is,
|PKq={p1q,p2q,…,pKq}=argtop−kp∈P⁡s⁢(q,p)subscriptsuperscript𝑃𝑞𝐾subscriptsuperscript𝑝𝑞1subscriptsuperscript𝑝𝑞2…subscriptsuperscript𝑝𝑞𝐾subscriptargtopk𝑝𝑃𝑠𝑞𝑝P^{q}\_{K}=\\{p^{q}\_{1},p^{q}\_{2},\\dots,p^{q}\_{K}\\}=\\operatorname{argtop-k}\_{p%
\\in P}s(q,p)italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPT = { italic\_p start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , italic\_p start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT , …, italic\_p start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPT } = start\_OPFUNCTION roman\_argtop - roman\_k end\_OPFUNCTION start\_POSTSUBSCRIPT italic\_p ∈italic\_P end\_POSTSUBSCRIPT italic\_s ( italic\_q , italic\_p )||
#### Approximate indexing for open-domain page retrieval.
Searching pages over
in a large document corpus
can be time-consuming and computationally expensive.
When a faster search is desired,
we create page indices offline by applying approximate nearest neighborhood search, based on Faiss> [
[> 26
](https://arxiv.org/html/2411.04952v1#bib.bib26)> , [> 16
](https://arxiv.org/html/2411.04952v1#bib.bib16)> ]
.
We use exact search for closed-domain page retrieval and employ
inverted file index (IVF)> [
[> 52
](https://arxiv.org/html/2411.04952v1#bib.bib52)> , [> 66
](https://arxiv.org/html/2411.04952v1#bib.bib66)> ]
(IVFFlatin Faiss) for an open-domain setting, which could reduce page retrieval latency from 20s/query to less than 2s/query when searching across 40K pages.
See[Sec.5.3](https://arxiv.org/html/2411.04952v1#S5.SS3)for a detailed comparison of speed-accuracy tradeoffs across different indexing methods.
### 2.3Question Answering
We run visual question answering by giving the text queryq𝑞qitalic\_qand retrieved page imagesPKqsubscriptsuperscript𝑃𝑞𝐾P^{q}\_{K}italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPTto a multi-modal language model to obtain the final answer.
For this, we employ multi-modal language models (*e.g*.Qwen2-VL> [
[> 59
](https://arxiv.org/html/2411.04952v1#bib.bib59)> ]
) that consist of a visual encoderEncVissuperscriptEncVis\\texttt{Enc}^{\\texttt{Vis}}Enc start\_POSTSUPERSCRIPT Vis end\_POSTSUPERSCRIPTand a language modelLM.
The visual encoder takesK𝐾Kitalic\_K-retrieved page imagesPKqsubscriptsuperscript𝑃𝑞𝐾P^{q}\_{K}italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPTas inputs and outputs visual embeddings (different from ColPali encoder’s outputs). The language model takes the visual embeddings and text embeddings of queryq𝑞qitalic\_qas inputs and outputs the final answera𝑎aitalic\_ain the autoregressive manner:
|a=LM⁢(EncVis⁢(PKq),q).𝑎LMsuperscriptEncVissubscriptsuperscript𝑃𝑞𝐾𝑞a=\\texttt{LM}(\\texttt{Enc}^{\\texttt{Vis}}(P^{q}\_{K}),q).italic\_a = LM ( Enc start\_POSTSUPERSCRIPT Vis end\_POSTSUPERSCRIPT ( italic\_P start\_POSTSUPERSCRIPT italic\_q end\_POSTSUPERSCRIPT start\_POSTSUBSCRIPT italic\_K end\_POSTSUBSCRIPT ) , italic\_q ) .||
![Refer to caption](x4.png)Figure 4:Illustration of PDF collections inM3DocVQA.
We first collect the URLs of all supporting contexts (Wikipedia documents) of individual questions of MultimodalQA> [
[> 54
](https://arxiv.org/html/2411.04952v1#bib.bib54)> ]
. Then, we create PDF versions from their URLs by rendering them in a web browser.
## 3M3DocVQA: A New Benchmark for Open-domain Document Understanding
We presentM3DocVQA(Multi-modalMulti-pageMulti-DocumentVisualQuestionAnswering), a new open-domain DocVQA benchmark designed to evaluate the ability to answer questions using multi-modal information from a large corpus of documents.
As illustrated in[Fig.2](https://arxiv.org/html/2411.04952v1#S1.F2), existing DocVQA datasets> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> , [> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> , [> 31
](https://arxiv.org/html/2411.04952v1#bib.bib31)> , [> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
primarily focus on evaluating question answering within the context of a single document (*i.e*., closed-domain).
These datasets are not well-suited for benchmarking open-domain visual question answering, where relevant information, often in multiple modalities such as text, images, and tables, must be retrieved from multiple documents. This limitation stems from their questions being designed around specific content on certain pages within a single document.
In real-world scenarios, users often seek answers that span across multiple documents and modalities, making open-domain settings critical.
However, the questions in the existing DocVQA datasets are not applicable in such an open-domain setting.
For example, a question from MP-DocVQA, such as“What was the gross profit in the year 2009?”assumes that the model already has access to specific information within the document.
M3DocVQAchallenges models in an open-domain DocVQA setting,
where they must navigate a large ‘haystack’ of multi-modal documents and retrieve relevant information to generate the final answer.
The dataset consists of 2,441 multi-hop questions spread across 3,368 PDF documents, totaling 41,005 pages.
Each question is supported by evidence found in one or more documents, spanning multiple modalities such as text, images, and tables, capturing the complexity and diversity typical of real-world documents.
Additionally, we provide the training split, consisting of 24,162 Wikipedia PDFs.
Although the documents in the training split were not utilized in our experiments,
they offer future researchers the opportunity to explore even larger-scale retrieval tasks or use the documents for training models, further expanding the potential applications ofM3DocVQA.
To createM3DocVQA, we extend the question-answer pairs from a short-context VQA dataset to a more complex setting that includes 1) PDF documents and 2) open-domain contexts. Specifically, we use the question-answer pairs from the development split111The test split of MultimodalQA> [
[> 54
](https://arxiv.org/html/2411.04952v1#bib.bib54)> ]
is unavailable, and previous works have used the development split for comparison.of MultimodalQA> [
[> 54
](https://arxiv.org/html/2411.04952v1#bib.bib54)> ]
, where models answer multi-hop questions based on short multi-modal contexts (*e.g*., short text passages, 1-2 images, a table) sourced from Wikipedia. We retrieved the URLs of all Wikipedia documents used as context in any of the MultimodalQA development split questions.
Then we generated PDF versions of the Wikipedia pages by rendering them in a Chromium web browser> [
[> 56
](https://arxiv.org/html/2411.04952v1#bib.bib56)> ]
, using the Playwright Python package> [
[> 45
](https://arxiv.org/html/2411.04952v1#bib.bib45)> ]
. These PDFs retain all vector graphics and metadata, ensuring zoom-in functionality and maintaining operational hyperlinks. In addition, no objects are split between different pages in the resulting PDFs.
Table 1:Open-domain DocVQA evaluation results onM3DocVQA.
The scores are based on F1, unless otherwise noted.
Index:FlatIP+IVFFlat.
Method|# Pages|Evidence Modalities|Question Hops|Overall|
Image|Table|Text|Single-hop|Multi-hop|EM|F1|
Text RAG (w/ ColBERT v2)|||||||||
Llama 3.1 8B|1|8.3|15.7|29.6|25.3|12.3|15.4|20.0|
Llama 3.1 8B|2|7.7|16.8|31.7|27.4|12.1|15.8|21.2|
Llama 3.1 8B|4|7.8|21.0|34.1|29.4|15.2|17.8|23.7|
M3DocRAG(w/ ColPali)|||||||||
Qwen2-VL 7B (Ours)|1|25.1|27.8|39.6|37.2|25.0|27.9|32.3|
Qwen2-VL 7B (Ours)|2|26.8|30.4|42.1|41.0|25.2|29.9|34.6|
Qwen2-VL 7B (Ours)|4|24.7|30.4|41.2|43.2|26.6|31.4|36.5|
While bothM3DocVQAand MultimodalQA> [
[> 54
](https://arxiv.org/html/2411.04952v1#bib.bib54)> ]
share the goal of evaluating
question answering given multi-modal context,M3DocVQAintroduces a more demanding scenario by requiring models to retrieve relevant information from a large set of documents, as opposed to being provided with a short context.
In MultimodalQA, models are given short, curated context (*e.g*., a paragraph from a Wikipedia document) that directly contains the information needed to answer the questions, simplifying the task to reasoning within the provided material. In contrast,M3DocVQApresents an open-domain setting, where models must retrieve information from a diverse collection of 3,368 PDF documents before attempting to answer any question.
This not only requires handling large-scale document retrieval but also dealing with multi-modal content–text, images, and tables–distributed across multiple documents. This key distinction highlightsM3DocVQA’s ability to simulate real-world challenges, where the relevant data is often spread across multiple sources. Consequently,M3DocVQAserves as a robust benchmark for retrieval-augmented generation tasks in document understanding, pushing the boundaries of models to deal with large-scale, multi-modal, and multi-document settings.
## 4Experiment Setup
#### Datasets.
We benchmarkM3DocRAGon three PDF document understanding datasets that represent different scenarios:
(1)M3DocVQA(Open-domain DocVQA);
(2) MMLongBench-Doc> [
[> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
(Closed-domain DocVQA);
(3) MP-DocVQA> [
[> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> ]
(Closed-domain DocVQA).
InM3DocVQA,M3DocRAGprocesses over 3,000 PDFs, totaling more than 40,000 pages.
For MP-DocVQA, models handle a single PDF with up to 20 pages for each question.
For MMLongBench-Doc, models handle a single PDF with up to 120 pages for each question.
#### Evaluation Metrics.
ForM3DocVQA, we follow the evaluation setup of MultimodalQA> [
[> 54
](https://arxiv.org/html/2411.04952v1#bib.bib54)> ]
.
For MMLongBench-Doc> [
[> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
and MP-DocVQA> [
[> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> ]
, we follow their official evaluation setups.
ForM3DocVQA, we evaluate answer accuracy with exact match (EM) and F1.
For MMLongBench-Doc,
we extract short answers with GPT4o> [
[> 46
](https://arxiv.org/html/2411.04952v1#bib.bib46)> ]
from the model outputs and
report answer accuracy with generalized accuracy (based on a rule-based evaluation script covering different answer types) and F1 score.
For MP-DocVQA, we report answer accuracy with ANLS> [
[> 8
](https://arxiv.org/html/2411.04952v1#bib.bib8)> ]
and page retrieval with accuracy (same as recall@1, as there is a single page annotation for each question) by submitting the generation results to the test server.222[https://rrc.cvc.uab.es/?ch=17&amp;com=tasks](https://rrc.cvc.uab.es/?ch=17&amp;com=tasks)
#### Models.
We mainly experiment with the ColPali v1> [
[> 17
](https://arxiv.org/html/2411.04952v1#bib.bib17)> ]
333[https://huggingface.co/vidore/colpali](https://huggingface.co/vidore/colpali)retrieval model and various recent open source multi-modal LMs with&lt;&lt;&lt;10B parameters,
including Idefics 2> [
[> 33
](https://arxiv.org/html/2411.04952v1#bib.bib33)> ]
, Idefics 3> [
[> 32
](https://arxiv.org/html/2411.04952v1#bib.bib32)> ]
, InternVL 2> [
[> 12
](https://arxiv.org/html/2411.04952v1#bib.bib12)> ]
, and Qwen2-VL> [
[> 59
](https://arxiv.org/html/2411.04952v1#bib.bib59)> ]
.
We also experiment with a text-based RAG pipeline by combining recent widely used text retrieval and language models:
ColBERT v2> [
[> 50
](https://arxiv.org/html/2411.04952v1#bib.bib50)> ]
and Llama 3.1> [
[> 37
](https://arxiv.org/html/2411.04952v1#bib.bib37)> ]
.
We also compare ColPali v1 with ColQwen v0.1> [
[> 17
](https://arxiv.org/html/2411.04952v1#bib.bib17)> ]
,444[https://huggingface.co/vidore/colqwen2-v0.1](https://huggingface.co/vidore/colqwen2-v0.1)another recent multi-modal retrieval model that was trained with same objective/dataset as ColPali but initialized with Qwen2-VL 2B> [
[> 59
](https://arxiv.org/html/2411.04952v1#bib.bib59)> ]
backbone.
For reproducible evaluation, we use deterministic greedy decoding for answer generation.
We compare these multi-modal and text-based RAG pipelines with recent top entries with comparable parameters (&lt;&lt;&lt;10B) reported on the leaderboards.
#### Other implementation details.
We use PyTorch> [
[> 47
](https://arxiv.org/html/2411.04952v1#bib.bib47)> , [> 48
](https://arxiv.org/html/2411.04952v1#bib.bib48)> ]
, Transformers> [
[> 60
](https://arxiv.org/html/2411.04952v1#bib.bib60)> ]
, and FlashAttention-2> [
[> 13
](https://arxiv.org/html/2411.04952v1#bib.bib13)> ]
libraries for running models.
We use Tesseract> [
[> 53
](https://arxiv.org/html/2411.04952v1#bib.bib53)> ]
for OCR in text RAG baselines, following> Ma et al.
> [
[> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
.
We use Faiss> [
[> 26
](https://arxiv.org/html/2411.04952v1#bib.bib26)> , [> 16
](https://arxiv.org/html/2411.04952v1#bib.bib16)> ]
for document indexing.
We use the pdf2image> [
[> 6
](https://arxiv.org/html/2411.04952v1#bib.bib6)> ]
library to convert each PDF page into an RGB image with a resolution of DPI=144.
While all PDF pages inM3DocVQAhave the same size –8.5 (width)×\\times×11 (height) in inches (*i.e*.US letter size) and 1224 (width)×\\times×1584 (height) in pixels,
in MP-DocVQA and MMLongBench-Doc datasets, pages have slightly different sizes.
To handle this, we resize page images to the most common image size within the dataset –1700 (width)×\\times×2200 (height) for MP-DocVQA,
and to the most common image size within each PDF document for MMLongBench-Doc.
All experiments are conducted with a single H100 80GB GPU.
We provide up to 4 pages as visual inputs to our multi-modal LMs, the maximum number of images we could fit in the single GPU.
Table 2:Closed-domain DocVQA evaluation results on MMLongBench-Doc.
We report the generalized accuracy (ACC) across five evidence source modalities: text (TXT), layout (LAY), chart (CHA), table (TAB), and image (IMG), and three evidence locations: single-page (SIN), cross-page (MUL), and unanswerable (UNA).
The scores from non-RAG methods are from> Ma et al.
> [
[> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
.
Method|# Pages|Evidence Modalities|Evidence Locations|Overall|
TXT|LAY|CHA|TAB|IMG|SIN|MUL|UNA|ACC|F1|
Text Pipeline|
LMs||||||||||||
ChatGLM-128k> [
[> 5
](https://arxiv.org/html/2411.04952v1#bib.bib5)> ]
|up to 120|23.4|12.7|9.7|10.2|12.2|18.8|11.5|18.1|16.3|14.9|
Mistral-Instruct-v0.2> [
[> 25
](https://arxiv.org/html/2411.04952v1#bib.bib25)> ]
|up to 120|19.9|13.4|10.2|10.1|11.0|16.9|11.3|24.1|16.4|13.8|
Text RAG||||||||||||
ColBERT v2 + Llama 3.1|1|20.1|14.8|12.7|17.4|7.4|21.8|7.8|41.3|21.0|16.1|
ColBERT v2 + Llama 3.1|4|23.7|17.7|14.9|24.0|11.9|25.7|12.2|38.1|23.5|19.7|
Multi-modal Pipeline|
Multi-modal LMs||||||||||||
DeepSeek-VL-Chat> [
[> 38
](https://arxiv.org/html/2411.04952v1#bib.bib38)> ]
|up to 120|7.2|6.5|1.6|5.2|7.6|5.2|7.0|12.8|7.4|5.4|
Idefics2> [
[> 33
](https://arxiv.org/html/2411.04952v1#bib.bib33)> ]
|up to 120|9.0|10.6|4.8|4.1|8.7|7.7|7.2|5.0|7.0|6.8|
MiniCPM-Llama3-V2.5> [
[> 64
](https://arxiv.org/html/2411.04952v1#bib.bib64)> , [> 61
](https://arxiv.org/html/2411.04952v1#bib.bib61)> ]
|up to 120|11.9|10.8|5.1|5.9|12.2|9.5|9.5|4.5|8.5|8.6|
InternLM-XC2-4KHD> [
[> 15
](https://arxiv.org/html/2411.04952v1#bib.bib15)> ]
|up to 120|9.9|14.3|7.7|6.3|13.0|12.6|7.6|9.6|10.3|9.8|
mPLUG-DocOwl 1.5> [
[> 22
](https://arxiv.org/html/2411.04952v1#bib.bib22)> ]
|up to 120|8.2|8.4|2.0|3.4|9.9|7.4|6.4|6.2|6.9|6.3|
Qwen-VL-Chat> [
[> 4
](https://arxiv.org/html/2411.04952v1#bib.bib4)> ]
|up to 120|5.5|9.0|5.4|2.2|6.9|5.2|7.1|6.2|6.1|5.4|
Monkey-Chat> [
[> 36
](https://arxiv.org/html/2411.04952v1#bib.bib36)> ]
|up to 120|6.8|7.2|3.6|6.7|9.4|6.6|6.2|6.2|6.2|5.6|
M3DocRAG||||||||||||
ColPali + Idefics2 (Ours)|1|10.9|11.1|6.0|7.7|15.7|15.4|7.2|8.1|11.2|11.0|
ColPali + Qwen2-VL 7B (Ours)|1|25.7|21.0|18.5|16.4|19.7|30.4|10.6|5.8|18.8|20.1|
ColPali + Qwen2-VL 7B (Ours)|4|30.0|23.5|18.9|20.1|20.8|32.4|14.8|5.8|21.0|22.6|
## 5Results and Key Findings
In the following,
we describe experiment results ofM3DocRAGand baselines in both open-domain ([Sec.5.1](https://arxiv.org/html/2411.04952v1#S5.SS1)) and closed-domain settings ([Sec.5.2](https://arxiv.org/html/2411.04952v1#S5.SS2)).
Next, we provide ablation studies ([Sec.5.3](https://arxiv.org/html/2411.04952v1#S5.SS3)) about different page indexing strategies and
different multi-modal LMs and retrieval models.
Lastly, we show qualitative examples ([Sec.5.4](https://arxiv.org/html/2411.04952v1#S5.SS4)) whereM3DocRAGcan tackleM3DocVQAquestions whose answer source exists in various modalities.
### 5.1Open-domain DocVQA
#### Multi-modal RAG outperforms text RAG, especially on non-text evidence sources.
[Table1](https://arxiv.org/html/2411.04952v1#S3.T1)shows the evaluation results onM3DocVQA.
As a model needs to find relevant documents from 3,000+ PDFs for each question, we focus solely on RAG pipelines.
We observe that ourM3DocRAG(ColPali + Qwen2-VL 7B) significantly outperforms text RAG (ColBERT v2 + Llama 3.1 8B), across all different evidence modalities / question hops / # pages.
The performance gap is especially big when the evidence involves images, underscoring thatM3DocRAGaddresses the information loss over non-textual content by text-only pipelines.
We also notice that providing more retrieved pages as context generally increases the performance of both text RAG andM3DocRAG(using the top 4 pages gives higher performance than the top 1 and 2 pages).
### 5.2Closed-domain DocVQA
#### Multi-modal RAG boosts long document understanding of MLMs.
In MMLongBench-Doc, the models must handle a long PDF document (up to 120 pages) for each question.
Since many multi-modal LMs have limited context length,> Ma et al.
> [
[> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
employed a concatenation strategy that combines all screenshot pages into either 1 or 5 images and inputs these concatenated images to multi-modal LMs.[Table2](https://arxiv.org/html/2411.04952v1#S4.T2)shows that
ColPali + Idefics2 surpass
Idefics2 without RAG, as well as all previous multi-modal entries.
In addition, ColPali + Qwen2-VL 7B achieves the best scores in overall F1 and most evidence modality/page settings.
This demonstrates the effectiveness of multi-modal retrieval over handling many pages by concatenating low-resolution images.
As observed inM3DocVQAexperiments,
we also notice that providing more retrieved pages as context generally increases the performance of both text RAG andM3DocRAG(using the top 4 pages gives higher performance than the top 1 page).
#### M3DocRAGachieves the state-of-the-art performance in MP-DocVQA.
In MP-DocVQA, the models must handle a PDF document of up to 20 pages for each question.[Table3](https://arxiv.org/html/2411.04952v1#S5.T3)presents the top-performing entries in the MP-DocVQA test split leaderboard, comparing text-based and multi-modal RAG pipelines. While the text RAG (ColBERT v2 + Llama 3.1) falls short compared to existing approaches, all multi-modal RAG pipelines outperform their text-based counterpart.
Notably, theM3DocRAGpipeline (ColPali + Qwen2-VL 7B) delivers the state-of-the-art results on MP-DocVQA.
It is interesting that while the existing entries were fine-tuned specifically for MP-DocVQA,
the components used inM3DocRAG(ColPali or Qwen2-VL 7B) were not tailored to this dataset –although Qwen2-VL 7B might have been trained on DocVQA> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> ]
, which shares some images with MP-DocVQA.
Table 3:Closed-domain DocVQA evaluation results on MP-DocVQA.
The RAG methods retrieve a single page to the downstream QA models.
Method|Answer Accuracy|Page Retrieval|
ANLS|R@1|
Multimodal LMs|||
Arctic-TILT 0.8B> [
[> 10
](https://arxiv.org/html/2411.04952v1#bib.bib10)> ]
|0.8122|50.79|
GRAM> [
[> 9
](https://arxiv.org/html/2411.04952v1#bib.bib9)> ]
|0.8032|19.98|
GRAM C-Former> [
[> 9
](https://arxiv.org/html/2411.04952v1#bib.bib9)> ]
|0.7812|19.98|
ScreenAI 5B> [
[> 3
](https://arxiv.org/html/2411.04952v1#bib.bib3)> ]
|0.7711|77.88|
Text RAG|||
ColBERT v2 + Llama 3.1 8B|0.5603|75.33|
M3DocRAG|||
ColPali + Qwen2-VL 7B (Ours)|0.8444|81.05|
Table 4:Speed-accuracy tradeoff with different indexing strategies onM3DocVQA.
Method: ColPali + Qwen2-VL 7B.
# Pages|Indexing|Latency (s) (↓↓\\downarrow↓)|Accuracy (↑↑\\uparrow↑)|
Retrieval|VQA|EM|F1|
1|FlatIP|21.0|1.1|28.9|33.7|
1|FlatIP + IVFFlat|1.8|1.1|27.9|32.3|
1|FlatIP + IVFPQ|0.2|1.1|25.9|30.3|
2|FlatIP + IVFFlat|1.8|2.4|29.9|34.6|
2|FlatIP + IVFPQ|0.2|2.4|29.0|33.5|
4|FlatIP + IVFFlat|1.8|4.8|31.4|36.5|
4|FlatIP + IVFPQ|0.2|4.8|29.9|34.7|
### 5.3Additional analysis
#### Different page indexing: speed and accuracy.
In[Table4](https://arxiv.org/html/2411.04952v1#S5.T4), we analyze the speed and accuracy of ColPali+Qwen2-VL 7B pipeline with different document embedding indexing methods.
While the naive indexing with exact search (FlatIP) is slow (21s per query),
we find that using approximate indexing such as inverted file> [
[> 66
](https://arxiv.org/html/2411.04952v1#bib.bib66)> , [> 52
](https://arxiv.org/html/2411.04952v1#bib.bib52)> ]
(IVFFlat) and product quantization> [
[> 27
](https://arxiv.org/html/2411.04952v1#bib.bib27)> ]
(IVFPQ) can retain most of the accuracy, while making the search significantly faster (&lt;2absent2&lt;2&lt; 2s per query). We useFlatIP+IVFFlatindexing by default, and users can choose appropriate indexing methods depending on their deployment requirements.
Table 5:Comparison of different multimodal LMs withinM3DocRAG, evaluated across different document understanding benchmarks.
For retrieval, we use the top-1 page from ColPali for all datasets.
We useFlatIP+IVFFlatindexing forM3DocVQA.
Multimodal LMs|M3DocVQA|MMLongBench-Doc|MP-DocVQA|
F1 (↑↑\\uparrow↑)|Acc (↑↑\\uparrow↑)|ANLS (↑↑\\uparrow↑)|
Idefics2 8B|27.8|10.8|0.56|
Idefics3 8B|31.8|16.4|0.77|
InternVL2 8B|30.9|17.3|0.81|
Qwen2-VL 7B|32.3|18.8|0.84|
#### Different multi-modal LMs.
In[Table5](https://arxiv.org/html/2411.04952v1#S5.T5), we compare four different multi-modal LMs in theM3DocRAGframework: Idefics2 8B> [
[> 33
](https://arxiv.org/html/2411.04952v1#bib.bib33)> ]
, Idefics3 8B> [
[> 32
](https://arxiv.org/html/2411.04952v1#bib.bib32)> ]
, InternVL2 8B> [
[> 12
](https://arxiv.org/html/2411.04952v1#bib.bib12)> ]
, and Qwen2-VL 7B> [
[> 59
](https://arxiv.org/html/2411.04952v1#bib.bib59)> ]
.
The Qwen2-VL 7B model outperforms other MLMs in all three benchmarks. Thus, we use the model as our default MLM component.
Table 6:Comparison of different multi-modal retrieval models withinM3DocRAGframework, evaluated across different document understanding benchmarks.
We provide Qwen2-VL 7B with top-4 pages for MMLongBench-Doc/M3DocVQAand top-1 page for MP-DocVQA from the retrieval models.
We useFlatIP+IVFFlatindexing forM3DocVQA.
Ret. Models|M3DocVQA|MMLongBench-Doc|MP-DocVQA|
F1 (↑↑\\uparrow↑)|Acc (↑↑\\uparrow↑)|ANLS (↑↑\\uparrow↑)|
ColPali v1|36.5|21.0|0.84|
ColQwen v0.1|32.1|21.5|0.86|
#### Different multi-modal retrieval models.
In[Table6](https://arxiv.org/html/2411.04952v1#S5.T6), we compare two different multi-modal retrival models inM3DocRAGframework: ColPali v1 and ColQwen v0.1 (see[Sec.4](https://arxiv.org/html/2411.04952v1#S4)for details). Both models are trained with the same training objectives but are initialized with different MLM architectures: PaliGemma 2B> [
[> 7
](https://arxiv.org/html/2411.04952v1#bib.bib7)> ]
and Qwen2-VL 2B> [
[> 59
](https://arxiv.org/html/2411.04952v1#bib.bib59)> ]
, respectively.
We find that ColPali achieves significantly better performance inM3DocVQA, while ColQwen achieves slightly better performance in MP-DocVQA and MMLongBench-Doc. Thus, we use ColPali as our default retrieval model.
![Refer to caption](x5.png)Figure 5:Qualitative example of ColPali + Qwen2-VL 7B onM3DocVQA. Image regions relevant to the question/answer are highlighted with orange boxes. The answer information is only stored visually within the game logo, where a man is leaning on a motorcycle.![Refer to caption](x6.png)Figure 6:Qualitative example of ColPali + Qwen2-VL 7B onM3DocVQA. Image regions relevant to the question/answer are highlighted with orange boxes. The question requires multi-page/document reasoning.![Refer to caption](x7.png)Figure 7:Qualitative example of ColPali + Qwen2-VL 7B onM3DocVQA. Image regions relevant to the question/answer are highlighted with orange boxes.
The VQA component could combine both the retrieved knowledge (Tropi was transferred on 11 July 2017) and its own knowledge (Valencia CF has a logo with a bat) to provide the final answer.
### 5.4Qualitative Examples
In[Fig.5](https://arxiv.org/html/2411.04952v1#S5.F5),[Fig.6](https://arxiv.org/html/2411.04952v1#S5.F6), and[Fig.7](https://arxiv.org/html/2411.04952v1#S5.F7),
we provide qualitative examples ofM3DocRAG(ColPali + Qwen2-VL 7B)’s question answering results on severalM3DocVQAexamples.
In[Fig.5](https://arxiv.org/html/2411.04952v1#S5.F5),
the answer information is only visually stored within the game logo (‘man is leaning on a motorcycle’), andM3DocRAGcould find the information.
In[Fig.6](https://arxiv.org/html/2411.04952v1#S5.F6),
the question requires multi-hop reasoning across different pages/documents, andM3DocRAGcould combine information from multiple retrieved pages.
In[Fig.7](https://arxiv.org/html/2411.04952v1#S5.F7), although ColPali did not retrieve the page that contains information about a team whose logo features a bat,
Qwen-2 VL leverages its own knowledge ‘Valencia CF has a logo featuring a bat’,
and could provide the final answer.
Overall, the qualitative examples showcase thatM3DocRAGcan successfully tackle different questions whose answer sources exist in various modalities.
## 6Related Work
#### Document visual question answering.
> Mathew et al.
> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> ]
proposed document visual question answering (DocVQA) task,
where a model extracts information from documents by treating them as images, like in generic visual question answering> [
[> 1
](https://arxiv.org/html/2411.04952v1#bib.bib1)> ]
.
Most research on DocVQA focuses on handling a single-page document> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> , [> 41
](https://arxiv.org/html/2411.04952v1#bib.bib41)> , [> 22
](https://arxiv.org/html/2411.04952v1#bib.bib22)> , [> 58
](https://arxiv.org/html/2411.04952v1#bib.bib58)> , [> 55
](https://arxiv.org/html/2411.04952v1#bib.bib55)> , [> 23
](https://arxiv.org/html/2411.04952v1#bib.bib23)> , [> 30
](https://arxiv.org/html/2411.04952v1#bib.bib30)> , [> 34
](https://arxiv.org/html/2411.04952v1#bib.bib34)> , [> 63
](https://arxiv.org/html/2411.04952v1#bib.bib63)> ]
,
and it has been now a common practice to include the single-page DocVQA> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> ]
as a part of the image understanding evaluation suite among recent MLMs> [
[> 12
](https://arxiv.org/html/2411.04952v1#bib.bib12)> , [> 59
](https://arxiv.org/html/2411.04952v1#bib.bib59)> , [> 7
](https://arxiv.org/html/2411.04952v1#bib.bib7)> , [> 32
](https://arxiv.org/html/2411.04952v1#bib.bib32)> , [> 46
](https://arxiv.org/html/2411.04952v1#bib.bib46)> , [> 20
](https://arxiv.org/html/2411.04952v1#bib.bib20)> ]
.
Several recent works study applying MLMs for DocVQA on multi-page documents> [
[> 31
](https://arxiv.org/html/2411.04952v1#bib.bib31)> , [> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> , [> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
.
However, all previous works on DocVQA have focused on handling questions in the context of a specific document, such as “What was the gross profit in the year
2009?”> [
[> 42
](https://arxiv.org/html/2411.04952v1#bib.bib42)> , [> 57
](https://arxiv.org/html/2411.04952v1#bib.bib57)> , [> 14
](https://arxiv.org/html/2411.04952v1#bib.bib14)> , [> 40
](https://arxiv.org/html/2411.04952v1#bib.bib40)> ]
.
While this is probably due to the limited context length of the backbone multi-modal LMs,
this does not reflect real-world scenarios, where users often ask questions that require information across different pages/documents.
We address the limitation and proposeM3DocRAGframework andM3DocVQAdataset for effective, efficient, and flexible document understanding under
various document contexts (closed-domain and open-domain),
question hops (single-hop and multi-hop),
and evidence modalities (text, chart, figure,*etc*.).
#### Retrieval-augmented generation.
Retrieval-augmented generation (RAG)> [
[> 35
](https://arxiv.org/html/2411.04952v1#bib.bib35)> ]
has emerged as a hybrid approach combining retrieval systems with generative models to improve the quality and relevance of generated content> [
[> 19
](https://arxiv.org/html/2411.04952v1#bib.bib19)> ]
.
RAG has been widely studied for open-domain question answering> [
[> 21
](https://arxiv.org/html/2411.04952v1#bib.bib21)> , [> 65
](https://arxiv.org/html/2411.04952v1#bib.bib65)> , [> 28
](https://arxiv.org/html/2411.04952v1#bib.bib28)> , [> 24
](https://arxiv.org/html/2411.04952v1#bib.bib24)> , [> 39
](https://arxiv.org/html/2411.04952v1#bib.bib39)> , [> 2
](https://arxiv.org/html/2411.04952v1#bib.bib2)> ]
, where the community has well-established practices for text-based pipelines.
A line of work in VQA
studies RAG on visual questions that require world knowledge> [
[> 62
](https://arxiv.org/html/2411.04952v1#bib.bib62)> , [> 11
](https://arxiv.org/html/2411.04952v1#bib.bib11)> , [> 44
](https://arxiv.org/html/2411.04952v1#bib.bib44)> , [> 51
](https://arxiv.org/html/2411.04952v1#bib.bib51)> ]
,
but their retrieval context is usually generic images and/or short text snippets and does not cover DocVQA settings.
To the best of our knowledge, no prior work has explored RAG setting for multi-modal document understanding only with multi-modal models (instead of using OCR methods).
Our framework tackles open-domain question answering over documents with complex multi-modal contexts, including textual, tabular, and visual information across different pages and documents.
## 7Conclusion
We introduceM3DocRAG,
a novel multi-modal RAG framework that
flexibly accommodates
various document contexts (closed-domain and open-domain),
question hops (single-hop and multi-hop),
and evidence modalities (text, chart, figure,*etc*.).
InM3DocRAG,
a multi-modal retrieval model identifies relevant pages from single or multiple documents, which are then processed by a multi-modal language model, where all documents are represented as pixels.
Next, we introduceM3DocVQA, the first benchmark that evaluates open-domain multi-modal document understanding capabilities.M3DocVQAconsists of 2,000+ questions and 3,000+ PDF documents, and the questions need to be answered with various modalities such as images, text, and tables.
Our experiments in three datasets (M3DocVQA, MP-DocVQA, and MMLongBench-Doc) demonstrate significant advantages ofM3DocRAGover existing methods, including the state-of-the-art performance in MP-DocVQA.
We also provide analysis comparing different indexing strategies, multi-modal LMs, and multi-modal retrieval models.
Finally, we show qualitative examples whereM3DocRAGcan successfully tackle different questions whose answer sources exist in various modalities.
We hope that our work encourages future advancements in multi-modal frameworks for document understanding, paving the way for more robust, scalable, and practical solutions in real-world applications.
## Ethical Considerations
#### Limitations.
Since our multimodal retrieval models and multimodal LMs were trained with English-heavy datasets, they might not understand prompts or documents written in non-English.
While ourM3DocRAGframework can benefit many document understanding applications, the model components could present false or biased information. Thus, the framework should be used with human supervision in real-world applications. Note thatM3DocRAGis designed with flexibility so that users can update or replace components as more accurate solutions for each element of the framework become available in the future.
#### Data collection.
We do not involve human subjects during data collection.
We do not claim ownership/rights of the Wikipedia documents, and we attribute the source Wikipedia document URLs to all pages.
## References
* Antol et al. [2015]Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret Mitchell, Dhruv Batra, C. Lawrence Zitnick, and Devi Parikh.VQA: Visual question answering.In*ICCV*, 2015.
* Asai et al. [2023]Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi.Self-rag: Learning to retrieve, generate, and critique through self-reflection, 2023.
* Baechler et al. [2024]Gilles Baechler, Srinivas Sunkara, Maria Wang, Fedir Zubach, Hassan Mansoor, Vincent Etter, Victor Cărbune, Jason Lin, Jindong Chen, and Abhanshu Sharma.ScreenAI: A Vision-Language Model for UI and Infographics Understanding, 2024.
* Bai et al. [2023]Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou.Qwen-VL: A frontier large vision-language model with versatile abilities.*arXiv preprint*, abs/2308.12966, 2023.
* Bai et al. [2024]Yushi Bai, Xin Lv, Jiajie Zhang, Yuze He, Ji Qi, Lei Hou, Jie Tang, Yuxiao Dong, and Juanzi Li.LongAlign: A recipe for long context alignment of large language models.*arXiv preprint*, abs/2401.18058, 2024.
* Belval [2017]Edouard Belval.pdf2image, 2017.
* Beyer et al. [2024]Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Bošnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai.PaliGemma: A versatile 3B VLM for transfer, 2024.
* Biten et al. [2019]Ali Furkan Biten, Andres Mafla, Lluis Gomez, Valveny C V Jawahar, and Dimosthenis Karatzas.Scene Text Visual Question Answering.In*ICCV*, 2019.
* Blau et al. [2024]Tsachi Blau, Sharon Fogel, Roi Ronen, Alona Golts, Roy Ganz, Elad Ben Avraham, Aviad Aberdam, Shahar Tsiper, and Ron Litman.Gram: Global reasoning for multi-page vqa.In*Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 15598–15607, 2024.
* Borchmann et al. [2024]Łukasz Borchmann, Michał Pietruszka, Wojciech Jaśkowski, Dawid Jurkiewicz, Piotr Halama, Paweł Józiak, Łukasz Garncarek, Paweł Liskowski, Karolina Szyndler, Andrzej Gretkowski, Julita Ołtusek, Gabriela Nowakowska, Artur Zawłocki, Łukasz Duhr, Paweł Dyda, and Michał Turski.Arctic-TILT. Business Document Understanding at Sub-Billion Scale, 2024.
* Chen et al. [2022]Wenhu Chen, Hexiang Hu, Xi Chen, Pat Verga, and William W Cohen.Murag: Multimodal retrieval-augmented generator for open question answering over images and text.*arXiv preprint arXiv:2210.02928*, 2022.
* Chen et al. [2024]Zhe Chen, Weiyun Wang, Hao Tian, Shenglong Ye, Zhangwei Gao, Erfei Cui, Wenwen Tong, Kongzhi Hu, Jiapeng Luo, Zheng Ma, et al.How far are we to gpt-4v? closing the gap to commercial multimodal models with open-source suites.*arXiv preprint arXiv:2404.16821*, 2024.
* Dao [2024]Tri Dao.FlashAttention-2: Faster attention with better parallelism and work partitioning.In*International Conference on Learning Representations (ICLR)*, 2024.
* Ding et al. [2023]Yihao Ding, Siwen Luo, Hyunsuk Chung, and Soyeon Caren Han.Pdfvqa: A new dataset for real-world vqa on pdf documents.In*Joint European Conference on Machine Learning and Knowledge Discovery in Databases*, pages 585–601. Springer, 2023.
* Dong et al. [2024]Xiaoyi Dong, Pan Zhang, Yuhang Zang, Yuhang Cao, Bin Wang, Linke Ouyang, Songyang Zhang, Haodong Duan, Wenwei Zhang, Yining Li, et al.Internlm-Xcomposer2-4KHD: A pioneering large vision-language model handling resolutions from 336 pixels to 4k hd.*arXiv preprint*, abs/2404.06512, 2024.
* Douze et al. [2024]Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff Johnson, Gergely Szilvasy, Pierre-Emmanuel Mazaré, Maria Lomeli, Lucas Hosseini, and Hervé Jégou.The faiss library, 2024.
* Faysse et al. [2024]Manuel Faysse, Hugues Sibille, Tony Wu, Bilel Omrani, Gautier Viaud, Céline Hudelot, and Pierre Colombo.ColPali: Efficient Document Retrieval with Vision Language Models, 2024.
* Fenniak and PyPDF2 Contributors [2022]Mathieu Fenniak and PyPDF2 Contributors.The PyPDF2 library, version 2, 2022.
* Gao et al. [2023]Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang.Retrieval-augmented generation for large language models: A survey.*arXiv preprint arXiv:2312.10997*, 2023.
* Gemini Team [2024]Gemini Team.Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context, 2024.
* Guu et al. [2020]Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Ming-Wei Chang.REALM: Retrieval-Augmented Language Model Pre-Training.In*ICML*, 2020.
* Hu et al. [2024]Anwen Hu, Haiyang Xu, Jiabo Ye, Ming Yan, Liang Zhang, Bo Zhang, Chen Li, Ji Zhang, Qin Jin, Fei Huang, and Jingren Zhou.mplug-docowl 1.5: Unified structure learning for ocr-free document understanding, 2024.
* Huang et al. [2022]Yupan Huang, Tengchao Lv, Lei Cui, Yutong Lu, and Furu Wei.Layoutlmv3: Pre-training for document ai with unified text and image masking.In*Proceedings of the 30th ACM International Conference on Multimedia*, page 4083–4091, New York, NY, USA, 2022. Association for Computing Machinery.
* Izacard and Grave [2021]Gautier Izacard and Edouard Grave.Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering.In*EACL*, 2021.
* Jiang et al. [2023]Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.Mistral 7b, 2023.
* Johnson et al. [2021]Jeff Johnson, Matthijs Douze, and Hervé Jégou.Billion-scale similarity search with gpus.*IEEE Transactions on Big Data*, 7(3):535–547, 2021.
* Jégou et al. [2011]Herve Jégou, Matthijs Douze, and Cordelia Schmid.Product quantization for nearest neighbor search.*IEEE Transactions on Pattern Analysis and Machine Intelligence*, 33(1):117–128, 2011.
* Karpukhin et al. [2020]Vladimir Karpukhin, O Barlas, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih.Dense Passage Retrieval for Open-Domain Question Answering.In*EMNLP*, pages 6769–6781, 2020.
* Khattab and Zaharia [2020]Omar Khattab and Matei Zaharia.ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.*SIGIR 2020 - Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval*, pages 39–48, 2020.
* Kim et al. [2022]Geewook Kim, Teakgyu Hong, Moonbin Yim, JeongYeon Nam, Jinyoung Park, Jinyeong Yim, Wonseok Hwang, Sangdoo Yun, Dongyoon Han, and Seunghyun Park.Ocr-free document understanding transformer.In*European Conference on Computer Vision (ECCV)*, 2022.
* Landeghem et al. [2023]Jordy Van Landeghem, Rafał Powalski, Rubèn Tito, Dawid Jurkiewicz, Matthew Blaschko, Łukasz Borchmann, Mickaël Coustaty, Sien Moens, Michał Pietruszka, Bertrand Ackaert, Tomasz Stanisławek, Paweł Józiak, and Ernest Valveny.Document Understanding Dataset and Evaluation (DUDE).In*ICCV*, 2023.
* Laurençon et al. [2024a]Hugo Laurençon, Andrés Marafioti, Victor Sanh, and Léo Tronchon.Building and better understanding vision-language models: insights and future directions, 2024a.
* Laurençon et al. [2024b]Hugo Laurençon, Léo Tronchon, Matthieu Cord, and Victor Sanh.What matters when building vision-language models?, 2024b.
* Lee et al. [2023]Kenton Lee, Mandar Joshi, Iulia Turc, Hexiang Hu, Fangyu Liu, Julian Eisenschlos, Urvashi Khandelwal, Peter Shaw, Ming-Wei Chang, and Kristina Toutanova.Pix2struct: screenshot parsing as pretraining for visual language understanding.In*Proceedings of the 40th International Conference on Machine Learning*. JMLR.org, 2023.
* Lewis et al. [2020]Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen Tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela.Retrieval-augmented generation for knowledge-intensive NLP tasks.In*NeurIPS*, 2020.
* Li et al. [2023]Zhang Li, Biao Yang, Qiang Liu, Zhiyin Ma, Shuo Zhang, Jingxu Yang, Yabo Sun, Yuliang Liu, and Xiang Bai.Monkey: Image resolution and text label are important things for large multi-modal models.*arXiv preprint*, abs/2311.06607, 2023.
* Llama Team [2024]Llama Team.The llama 3 herd of models, 2024.
* Lu et al. [2024]Haoyu Lu, Wen Liu, Bo Zhang, Bingxuan Wang, Kai Dong, Bo Liu, Jingxiang Sun, Tongzheng Ren, Zhuoshu Li, Yaofeng Sun, et al.DeepSeek-VL: towards real-world vision-language understanding.*arXiv preprint*, abs/2403.05525, 2024.
* Luo et al. [2023]Hongyin Luo, Yung-Sung Chuang, Yuan Gong, Tianhua Zhang, Yoon Kim, Xixin Wu, Danny Fox, Helen Meng, and James Glass.Sail: Search-augmented instruction learning, 2023.
* Ma et al. [2024]Yubo Ma, Yuhang Zang, Liangyu Chen, Meiqi Chen, Yizhu Jiao, Xinze Li, Xinyuan Lu, Ziyu Liu, Yan Ma, Xiaoyi Dong, et al.Mmlongbench-doc: Benchmarking long-context document understanding with visualizations.*arXiv preprint arXiv:2407.01523*, 2024.
* Mathew et al. [2021a]Minesh Mathew, Viraj Bagal, Rubèn Pérez Tito, Dimosthenis Karatzas, Ernest Valveny, and C.V. Jawahar.Infographicvqa.*2022 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)*, pages 2582–2591, 2021a.
* Mathew et al. [2021b]Minesh Mathew, Dimosthenis Karatzas, and CV Jawahar.Docvqa: A dataset for vqa on document images.In*Proceedings of the IEEE/CVF winter conference on applications of computer vision*, pages 2200–2209, 2021b.
* Memon et al. [2020]Jamshed Memon, Maira Sami, Rizwan Ahmed Khan, and Mueen Uddin.Handwritten optical character recognition (ocr): A comprehensive systematic literature review (slr).*IEEE Access*, 8:142642–142668, 2020.
* Mensink et al. [2023]Thomas Mensink, Jasper Uijlings, Lluis Castrejon, Arushi Goel, Felipe Cadar, Howard Zhou, Fei Sha, André Araujo, and Vittorio Ferrari.Encyclopedic VQA: Visual questions about detailed properties of fine-grained categories.In*Proceedings of the IEEE International Conference on Computer Vision*, pages 3090–3101, 2023.
* Microsoft [2021]Microsoft.Playwright for python, 2021.
* OpenAI [2024]OpenAI.Hello gpt-4o, 2024.
* Paszke et al. [2017]Adam Paszke, Sam Gross, Soumith Chintala, Gregory Chana, Edward Yang, Zachary DeVito, Zeming Lin, Alban Desmaison, Luca Antiga, and Adam Lerer.Automatic differentiation in PyTorch.In*NIPS Workshop*, 2017.
* Paszke et al. [2019]Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Yang, Zach DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala.PyTorch: An imperative style, high-performance deep learning library.*Advances in Neural Information Processing Systems*, 32(NeurIPS), 2019.
* pdfminer [2019]pdfminer.pdfminer.six, 2019.
* Santhanam et al. [2022]Keshav Santhanam, Omar Khattab, Jon Saad-Falcon, Christopher Potts, and Matei Zaharia.ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction.*NAACL 2022 - 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Proceedings of the Conference*, pages 3715–3734, 2022.
* Schwenk et al. [2022]Dustin Schwenk, Apoorv Khandelwal, Christopher Clark, Kenneth Marino, and Roozbeh Mottaghi.A-okvqa: A benchmark for visual question answering using world knowledge, 2022.
* Sivic and Zisserman [2003]Sivic and Zisserman.Video google: a text retrieval approach to object matching in videos.In*Proceedings Ninth IEEE International Conference on Computer Vision*, pages 1470–1477 vol.2, 2003.
* Smith [2007]Ray Smith.An overview of the tesseract ocr engine.In*ICDAR*, 2007.
* Talmor et al. [2021]Alon Talmor, Ori Yoran, Amnon Catav, Dan Lahav, Yizhong Wang, Akari Asai, Gabriel Ilharco, Hannaneh Hajishirzi, and Jonathan Berant.Multimodalqa: Complex question answering over text, tables and images.*arXiv preprint arXiv:2104.06039*, 2021.
* Tang et al. [2023]Zineng Tang, Ziyi Yang, Guoxin Wang, Yuwei Fang, Yang Liu, Chenguang Zhu, Michael Zeng, Cha Zhang, and Mohit Bansal.Unifying vision, text, and layout for universal document processing, 2023.
* The Chromium Project Authors [2024]The Chromium Project Authors.The chromium projects, 2024.
* Tito et al. [2023]Rubèn Tito, Dimosthenis Karatzas, and Ernest Valveny.Hierarchical multimodal transformers for multipage docvqa.*Pattern Recognition*, 144:109834, 2023.
* Wang et al. [2023]Dongsheng Wang, Natraj Raman, Mathieu Sibue, Zhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, and Xiaomo Liu.DocLLM: A layout-aware generative language model for multimodal document understanding, 2023.
* Wang et al. [2024]Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, and Junyang Lin.Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution.*arXiv preprint arXiv:2409.12191*, 2024.
* Wolf et al. [2020]Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, and Jamie Brew.HuggingFace’s Transformers: State-of-the-art Natural Language Processing.In*EMNLP*, 2020.
* Xu et al. [2024]Ruyi Xu, Yuan Yao, Zonghao Guo, Junbo Cui, Zanlin Ni, Chunjiang Ge, Tat-Seng Chua, Zhiyuan Liu, and Gao Huang.LLaVA-UHD: An LMM perceiving any aspect ratio and high-resolution images.*arXiv preprint*, abs/2403.11703, 2024.
* Yasunaga et al. [2023]Michihiro Yasunaga, Armen Aghajanyan, Weijia Shi, Rich James, Jure Leskovec, Percy Liang, Mike Lewis, Luke Zettlemoyer, and Wen-tau Yih.Retrieval-Augmented Multimodal Language Modeling.In*ICML*, 2023.
* Ye et al. [2023]Jiabo Ye, Anwen Hu, Haiyang Xu, Qinghao Ye, Mingshi Yan, Guohai Xu, Chenliang Li, Junfeng Tian, Qi Qian, Ji Zhang, Qin Jin, Liang He, Xin Lin, and Feiyan Huang.Ureader: Universal ocr-free visually-situated language understanding with multimodal large language model.In*Conference on Empirical Methods in Natural Language Processing*, 2023.
* Yu et al. [2024]Tianyu Yu, Haoye Zhang, Yuan Yao, Yunkai Dang, Da Chen, Xiaoman Lu, Ganqu Cui, Taiwen He, Zhiyuan Liu, Tat-Seng Chua, and Maosong Sun.RLAIF-V: Aligning mllms through open-source ai feedback for super gpt-4v trustworthiness.*arXiv preprint*, abs/2405.17220, 2024.
* Zhu et al. [2021]Fengbin Zhu, Wenqiang Lei, Chao Wang, Jianming Zheng, Soujanya Poria, and Tat-Seng Chua.Retrieving and reading: A comprehensive survey on open-domain question answering.*arXiv preprint arXiv:2101.00774*, 2021.
* Zobel and Moffat [2006]Justin Zobel and Alistair Moffat.Inverted files for text search engines.*ACM Comput. Surv.*, 38(2):6–es, 2006.
