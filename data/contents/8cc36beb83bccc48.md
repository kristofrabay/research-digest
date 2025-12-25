# MMORE: Massive Multimodal Open RAG & Extraction

**URL:** https://arxiv.org/html/2509.11937v1
**Published:** 2025-05-26T00:00:00.000Z

---

## Summary

The web page describes **MMORE (Massive Multimodal Open RAG & Extraction)**, an open-source pipeline designed for scalable ingestion, transformation, and retrieval of knowledge from heterogeneous document formats for use with Large Language Models (LLMs).

**Key features and capabilities relevant to your query:**

*   **Multimodal Support:** MMORE supports over fifteen file types, including text, tables, images, emails, audio, and video, processing them into a unified format for downstream LLM applications.
*   **Document Understanding & Parsing:** It integrates extraction tools for tasks like **PDF parsing** (using tools like Surya) and handles various document formats (DOCX, PPTX, spreadsheets).
*   **RAG (Retrieval-Augmented Generation):** It features a robust RAG pipeline with hybrid dense-sparse retrieval, supporting both interactive APIs and batch endpoints. Evaluation on PubMedQA showed that MMORE-augmented LLMs improve biomedical QA accuracy with increasing retrieval depth.
*   **Scalability and Performance:** The architecture is modular and distributed (built on Dask), demonstrating a 3.8-fold speedup over single-node baselines in distributed mode and achieving 40% higher accuracy than Docling on scanned PDFs.
*   **Structured Output:** The processing module standardizes heterogeneous content into a unified JSON-based format called `MultimodalSample`, which interleaves text with modality placeholders (e.g., for images/charts) to preserve context linkage.

While the page discusses the general architecture for handling multimodal data and extraction, it does **not** specifically mention or benchmark proprietary models like **GPT-4V, Claude vision, or Gemini** for vision tasks, nor does it detail specific methods for **chart/table extraction** beyond general document understanding, although it supports spreadsheet formats and mentions layout accuracy. It focuses on the open-source pipeline infrastructure itself.

---

## Full Content

MMORE: Massive Multimodal Open RAG &amp; Extraction
# MMORE: Massive Multimodal Open RAG &amp; Extraction
Alexandre SallinenStefan KrsteskiPaul TeiletcheMarc-Antoine AllardBaptiste LecoeurMichael ZhangDavid KalajdzicMatthias MeyerFabrice NemoMary-Anne Hartley
###### Abstract
We introduceMMORE, an open-source pipeline forMassiveMultimodalOpenRetrieval-Augmented Generation andExtraction, designed to ingest, transform, and retrieve knowledge from heterogeneous document formats at scale.MMOREsupports more than fifteen file types, including text, tables, images, emails, audio, and video, and processes them into a unified format to enable downstream applications for LLMs. The architecture offers modular, distributed processing, enabling scalable parallelization across CPUs and GPUs. On processing benchmarks,MMOREdemonstrates a 3.8-fold speedup over single-node baselines and 40% higher accuracy than Docling on scanned PDFs. The pipeline integrates hybrid dense-sparse retrieval and supports both interactive APIs and batch RAG endpoints. Evaluated on PubMedQA,MMORE-augmented medical LLMs improve biomedical QA accuracy with increasing retrieval depth.MMOREprovides a robust, extensible foundation for deploying task-agnostic RAG systems on diverse, real-world multimodal data. The codebase is available at[https://github.com/swiss-ai/mmore](https://github.com/swiss-ai/mmore).
1EPFL, Switzerland|2ETHZ, Switzerland|
3Harvard University, USA|
![Refer to caption](pipeline.png)Figure 1:The end-to-end pipeline from file-type–specific processing to retrieval-augmented generation (RAG).
## 1Introduction
As of 2025, the public web is conservatively estimated to host more than 2.5 trillion PDF documents, alongside petabytes of mixed-modality slide decks, spreadsheets, images, and audiovisual artefacts> (CloudFiles, [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib4)> )
. Yet fewer than one percent of these resources are represented in popular machine-learning corpora as they are remain locked behind brittle, heterogeneous formats that frustrate automated parsing at scale. Existing pipelines rely on ad hoc mosaics of format-specific utilities, limiting throughput, reproducibility, and long-term maintainability.
As data-supply forecasts estimate that the pool of high-quality human-generated text could be exhausted by prevailing scaling trends as early as 2026> (Villalobos et al., [> 2022
](https://arxiv.org/html/2509.11937v1#bib.bib24)> , [> 2024
](https://arxiv.org/html/2509.11937v1#bib.bib25)> )
, it has become essential to find more format-agnostic preprocessing workflows. Much of this data, particularly in specialized or institutional settings, is unavailable for training but remains crucial for improving the verifiability of LLM outputs through RAG. Hallucinations> (OpenAI, [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib13)> )
and factual drift> (Huang et al., [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib6)> )
remain significant challenges, and robust RAG pipelines are increasingly explored as a means to mitigate these issues, thereby reducing the burden of manual validation and better aligning model outputs with trustworthy source material.
To address these limitations, we introduceMMOREan open-source tool forMassiveMultimodalOpenRetrieval-Augmented Generation andExtraction, a unified pipeline for scalable extraction, transformation, and retrieval of multimodal data.MMOREsupports diverse formats such as documents, presentations, spreadsheets, and multimedia and integrates them into a structured knowledge base, enabling LLMs to access accurate, contextually grounded information via the RAG paradigm.
Designed for modularity and scalability, our pipeline natively supports parallelized processing across multi-node architectures and distributed environments such as Kubernetes clusters. Compared to Docling demonstrates more than 2-fold faster end-to-end processing, while achieving 40% higher layout accuracy on scanned PDFs. In distributed mode, we show that our pipeline processes 720 pages in 185s using four nodes, resulting in 3.8-fold speedup over single-node mode. The results demonstrateMMORE’s effectiveness as a scalable, high-accuracy solution for multimodal document processing in real-world deployment.
## 2Related Work
Large-scale transformation of unstructured documents into structured, machine‑readable format has attracted substantial attention. We group prior work into two strands:(i)document ingestion and parsing pipelines, and(ii)RAG frameworks. To our knowledge, neither line of work simultaneously offers the modality coverage and end‑to‑end throughput required for industrial‑ and small‑scale multimodal assistants that we target withMMORE.
Document Ingestion Pipelines.GPU‑accelerated microservice suites such asNV‑Ingest> (Team, [> 2024
](https://arxiv.org/html/2509.11937v1#bib.bib21)> )
convert PDFs and office documents into page‑level JSON enriched with text blocks, tables, and graphics, and can optionally export embeddings for downstream indexing.Docling> (Auer et al., [> 2024
](https://arxiv.org/html/2509.11937v1#bib.bib1)> )
extends the modality set to spreadsheets, and other common formats, but executes primarily on a single node and therefore exhibits limited throughput in production settings. Classical OCR tools likedoctr> (Mindee, [> 2021
](https://arxiv.org/html/2509.11937v1#bib.bib11)> )
handle text detection and recognition but rely on external systems for layout, embeddings, and indexing.Surya> (Paruchuri &amp; Team, [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib15)> )
adds multilingual OCR and layout analysis but lacks built-in multi-GPU or cluster parallelism. Commercial services such asLLMWhisperer> (Unstract, [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib22)> )
offer similar functionality behind a paywall, which restricts reproducibility and hinders open experimentation. In contrast,MMOREcombines extraction, transformation, embedding, and indexing into a single open‑source pipeline that natively parallelizes across multi‑node, multi‑GPU deployments. Moreover,MMOREuniquely handles audiovisual assets, enabling unified RAG over text, images, and time‑based media.
RAG Frameworks.Open‑source libraries such asLangChain> (Chase, [> 2022
](https://arxiv.org/html/2509.11937v1#bib.bib3)> )
andLlamaIndex> (Liu, [> 2022
](https://arxiv.org/html/2509.11937v1#bib.bib10)> )
provide high-level abstractions for chunking, embedding, retrieval, and prompting. However, they rely on external loaders for modality‑specific parsing and give no guidance on efficient high-throughput ingestion.
Several recent pipelines, such asUnstructured.io> (Unstructured-IO, [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib23)> )
and Haystack> (Pietsch et al., [> 2019
](https://arxiv.org/html/2509.11937v1#bib.bib17)> )
for document parsing, orM3IT> (Li et al., [> 2023
](https://arxiv.org/html/2509.11937v1#bib.bib8)> )
andOpenFlamingo> (Awadalla et al., [> 2023
](https://arxiv.org/html/2509.11937v1#bib.bib2)> )
for multimodal model alignment, address specific components of this pipeline. Yet none provide an integrated, open-source framework that supports ingestion, transformation, and retrieval across heterogeneous, real-world file types at scale.
MMOREcombines a scalable ingestion layer with a task-agnostic retrieval API, unifying document processing and RAG tools to enable multimodal assistants from raw enterprise data in one library.
## 3Architecture
MMOREprovides an end-to-end platform, enabling users to process large document collections, build retrieval indices, and query LLMs with relevant multimodal content, all within a unified framework, as illustrated in Figure[1](https://arxiv.org/html/2509.11937v1#S0.F1).
### 3.1Processing
At the core ofMMORElies a modular, scalable processing pipeline, designed for efficient, multimodal data extraction. Importantly,MMOREreuses open-source extraction tools such asSurya> (Paruchuri &amp; Team, [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib15)> )
for PDF parsing,Whisper> (Radford et al., [> 2023
](https://arxiv.org/html/2509.11937v1#bib.bib19)> )
for audio transcription, and standard Python libraries for office file formats, allowing us to focus on scalable orchestration and integration. A complete list of supported extractors is provided in Appendix[A.1](https://arxiv.org/html/2509.11937v1#A1.SS1). The design prioritizes three main strengths:(i)multimodal document processing,(ii)extensibility to new file types, and(iii)high-throughput distributed execution.
Multimodal Data Extraction.The processor module extracts heterogeneous content from documents and standardizes it into a unified JSON-based format, referred to as theMultimodalSample(see Appendix[A.2](https://arxiv.org/html/2509.11937v1#A1.SS2)). Each sample consists of plain text interleaved with modality placeholders (e.g. images) and a list of the extracted modalities, preserving their type and location. Embedded media are extracted and saved to disk, with placeholder tokens (e.g.,&lt;attachment&gt;) inserted at the corresponding positions within the text. This design supports downstream tasks that require text with tightly linked visual elements, such as multimodal pre-training or RAG.
Extensibility.To facilitate extensibility, we designed a common processor interface that abstracts file-specific handling into modular components. Adding support for a new file type requires only implementing a lightweight subclass, promoting long-term maintainability and community-driven contributions. Each processor needs to define a class that takes a file path as input and outputs aMultimodalSample, leveraging the standardized output format across the system. To date,MMOREsupports more than 15 file types, including, but not limited to, PDFs, DOCX, PPTX, spreadsheets, media files, emails, and HTML pages.
Distributed Processing.MMOREnatively supports both intra-node and inter-node parallelization, exploiting all available CPU and GPU resources without requiring manual configuration from the user. The system is built on top ofDask> (Dask Development Team, [> 2016
](https://arxiv.org/html/2509.11937v1#bib.bib5)> )
, enabling automatic workload balancing, fault tolerance, and seamless scaling across deployment settings, from standalone machines to large multi-node clusters. This design scales across use cases, from individual researchers to large organizations. To further support both ends of the spectrum,MMOREoffers two processing modes: a fast mode for speed and a default mode for accuracy, allowing users to balance performance and fidelity as needed.
### 3.2RAG
The RAG pipeline is composed of three independent components:(i)post-processing,(ii)indexing and retrieval, and(iii)an integrated RAG service. Each part is modular and can be run independently.
Post-processing.This stage filters the extracted text to improve quality for downstream tasks.MMOREexploits the existingdatatrove> (Penedo et al., [> 2024
](https://arxiv.org/html/2509.11937v1#bib.bib16)> )
, a high-throughput filtering library, and includes native support for several post-processing components, including Named Entity Recognition, Chunking, and Tagging.
Indexing and Retrieval.Indexing is crucial to RAG performance, as retrieval relies on how documents are represented.MMOREuses a hybrid indexing strategy, storing both sparse and dense embeddings for each document. Sparse representations support lexical matching and improve interpretability, while dense embeddings enable semantic search using neural similarity. This duality allows users to choose or combine retrieval embeddings depending on their downstream task. The retriever is accessible via our integrated RAG system or as a standalone API.
Integrated RAG system.The RAG system supports both API-based querying and offline batch processing. In batch mode, users provide a JSONL file containing retrieval queries; the system processes each entry and saves the results to a new JSONL file. Both modes allow customization of the model, prompt template, index source, and other parameters via configuration files or API options.
## 4Evaluation Setup
We evaluateMMORE’s processing and RAG modules independently. Below, we detail our methodology for assessing efficiency, accuracy, and scalability.
### 4.1Processing
The processing module is evaluated along two axes: efficiency and accuracy, versusDocling> (Auer et al., [> 2024
](https://arxiv.org/html/2509.11937v1#bib.bib1)> )
as a baseline due to its popularity and ease of use.
Efficiency.We benchmark processing speed using a single A100 80GB. For scalability analysis, we use an 18-page paper and synthetically generate longer documents by duplicating its content to reach 36, 54, 90, to 720 pages. This setup allows us to test throughput for both single-device and distributed processing. The distributed experiments are conducted on a Kubernetes cluster with 1 vs 4 nodes (1 A100 per node) to evaluate parallelization efficiency. To highlightMMORE’s strength in handling heterogeneous data, we also evaluate its performance across a diverse set of 19 files, spanning 9 unique file types.
Accuracy.To assess text extraction quality, we create a benchmark using public-domain books from Project Gutenberg> (Project Gutenberg, [> 1971
](https://arxiv.org/html/2509.11937v1#bib.bib18)> )
by pairing PDF inputs with their corresponding plain-text ground truths. We select two contrasting cases: ”The Blue Castle” (a clean, digital-friendly PDF) and ”The Great Gatsby” (a scanned, image-based file). Each document is truncated to 50k characters to ensure computational feasibility,
particularly for metrics like Levenshtein distance. We report standard metrics: BLEU> (Papineni et al., [> 2002
](https://arxiv.org/html/2509.11937v1#bib.bib14)> )
for n-gram overlap,
ROUGE-L> (Lin, [> 2004
](https://arxiv.org/html/2509.11937v1#bib.bib9)> )
, and character error rate (CER)> (Navarro, [> 2001
](https://arxiv.org/html/2509.11937v1#bib.bib12)> )
. Metric formulations are provided in the Appendix[A.3](https://arxiv.org/html/2509.11937v1#A1.SS3)
### 4.2RAG
To evaluate our RAG pipeline, we focus on the PubMedQA benchmark> (Jin et al., [> 2019
](https://arxiv.org/html/2509.11937v1#bib.bib7)> )
, a biomedical question-answering task. We construct a retrieval corpus by indexing all PubMed abstracts and conclusions into a dense vector database usingMMORE. At inference time, the top-kkmost relevant documents are retrieved using a similarity search and prepended to the original question as context for the language model. We experiment with both Meditron3-8B and Meditron3-70B> (Sallinen et al., [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib20)> )
, evaluating how different values ofkkaffect downstream accuracy. This setup isolates the effect of retrieval depth on performance within a consistent biomedical knowledge source.
## 5Results
### 5.1Processing
||The Blue Castle (digital PDF)|The Great Gatsby (scanned images)|
Method|BLEU↑\\uparrow|ROUGE-L↑\\uparrow|CER↓\\downarrow|BLEU↑\\uparrow|ROUGE-L↑\\uparrow|CER↓\\downarrow|
\\rowcolororange!10
MMORE|0.8608|0.9940|0.0241|0.7973|0.9813|0.0295|
MMORE (fast)|0.8639|0.9963|0.0206|0.0000|0.0000|1.0000|
Docling|0.8643|0.9959|0.0199|0.5451|0.6582|0.5518|
Table 1:Accuracy evaluation on two Project Gutenberg books: “The Blue Castle” and “The Great Gatsby”.3636909018018036036072072005005001000100015001500PDF PagesProcessing Time (seconds)DoclingMMORE (1 node)MMORE (1 node-fast)MMORE (4 nodes)Figure 2:Processing time vs. PDF length forDoclingandMMORE.MMORE(1 node-fast) disables OCR for performance, andMMORE(4 nodes) uses distributed processing.
Efficiency.Figure[2](https://arxiv.org/html/2509.11937v1#S5.F2)shows comparison ofDoclingandMMORE. On short documents (36 pages)Doclingis marginally faster thanMMORE(default). The difference disappears at 90 pages and shifts in favor ofMMOREbeyond 180 pages, where our pipeline scales almost linearly whileDoclingslows down super-linearly. The fast mode, which omits OCR, delivers an additional speed-up of roughly two to three times. Running the default pipeline on four nodes achieves a 3.8-fold reduction in latency compared to the single-node baseline, surpassing even the single-node fast mode and clearly demonstrating the efficiency and scalability of the distributed execution inMMORE. It is also worth mentioning that the batch size is user-configurable. The experiments presented here used a conservative default, leaving around 65GB of the 80GB GPU unused. This highlights the potential for further optimization, as users can adjust the configuration to fully exploit available hardware resources. Table[2](https://arxiv.org/html/2509.11937v1#S5.T2)further illustrates the performance advantage ofMMOREacross multiple file types. In default mode,MMOREreduces the total processing time by 45.48% compared toDocling, with the fast mode achieving an even more pronounced improvement of 155.38%.
|Metric|Docling|MMORE default|MMORE fast|
Total Time (s)|522.98|358.93|204.57|
Num. of Unsupported Files|5|0|0|
Relative Efficiency|baseline|+45.48%|+155.38%|
Table 2:Processing speeds for 9 unique file types - PDF, DOCX, EML, MD, MP4, MP3, PPTX, TXT, XLSX (19 files in total).
Accuracy.Table[1](https://arxiv.org/html/2509.11937v1#S5.T1)reports BLEU, ROUGE-L, and CER on two Project Gutenberg titles. On the digitally formatted ”Blue Castle” book, all three systems achieve near-perfect scores, withDoclingattaining the lowest CER (1.99%); however, differences remain negligible. The scanned version of ”The Great Gatsby”, an image-based document requiring OCR, provides a greater challenge. Here,MMOREfast predictably fails, as it omits OCR entirely. In contrast,MMOREdefault maintains high extraction fidelity, clearly outperformingDocling, whose CER of 55% indicates significant OCR errors. Although these results demonstrate the accuracy of our pipeline, further benchmarking on a larger and more diverse set of documents is necessary to robustly validate its generalization capabilities.
### 5.2RAG
0113374747676787880808282kkPubMedQA Acc. (%)Meditron3-8BMeditron3-70BFigure 3:Effect of retrieved documents (kk) on PubMedQA accuracy for Meditron models usingMMORE’s built-in RAG.
To evaluate RAG performance, we test the Meditron-3 model family with various RAG configurations on the PubMedQA benchmark. Figure[3](https://arxiv.org/html/2509.11937v1#S5.F3)shows that both Meditron-3[8B] and Meditron-3[70B]> (Sallinen et al., [> 2025
](https://arxiv.org/html/2509.11937v1#bib.bib20)> )
consistently improve accuracy with RAG, especially as the number of retrieved documentskkincreases. These results demonstrate that our RAG pipeline effectively injects domain-specific context at inference time, improving answer accuracy.
## 6Conclusion
MMOREis a scalable, open-source pipeline for retrieval-augmented generation over diverse, real-world data. It supports more than 15 file types, including PDFs, spreadsheets, images, audio, and video, and enables structured, high-throughput integration into LLM workflows.
Our results show thatMMOREoutperformsDoclingin both speed and layout fidelity, particularly in OCR-heavy documents, and improves biomedical QA accuracy on PubMedQA via efficient RAG pipelines.
Built for extensibility and deployment at scale,MMOREprovides a flexible foundation for verifiable, multimodal LLM applications. Future work will expand support for multilingual retrieval, audiovisual alignment, and federated processing in privacy-sensitive settings.
## References
* Auer et al. (2024)Auer, C., Lysak, M., Nassar, A., Dolfi, M., Livathinos, N., Vagenas, P., Ramis, C. B., Omenetti, M., Lindlbauer, F., Dinkla, K., et al.Docling technical report.*arXiv preprint arXiv:2408.09869*, 2024.
* Awadalla et al. (2023)Awadalla, A., Gao, I., Gardner, J., Hessel, J., Hanafy, Y., Zhu, W., Marathe, K., Bitton, Y., Gadre, S., Sagawa, S., et al.Openflamingo: An open-source framework for training large autoregressive vision-language models.*arXiv preprint arXiv:2308.01390*, 2023.
* Chase (2022)Chase, H.LangChain.[https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain), 2022.
* CloudFiles (2025)CloudFiles.How many files are there in the world?, 2025.URL[https://www.cloudfiles.io/blog/how-many-files-are-there-in-the-world](https://www.cloudfiles.io/blog/how-many-files-are-there-in-the-world).
* Dask Development Team (2016)Dask Development Team.*Dask: Library for dynamic task scheduling*, 2016.URL[http://dask.pydata.org](http://dask.pydata.org).
* Huang et al. (2025)Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., et al.A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions.*ACM Transactions on Information Systems*, 43(2):1–55, 2025.
* Jin et al. (2019)Jin, Q., Dhingra, B., Liu, Z., Cohen, W., and Lu, X.Pubmedqa: A dataset for biomedical research question answering.In*Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, pp.  2567–2577, 2019.
* Li et al. (2023)Li, L., Yin, Y., Li, S., Chen, L., Wang, P., Ren, S., Li, M., Yang, Y., Xu, J., Sun, X., Kong, L., and Liu, Q.M3it: A large-scale dataset towards multi-modal multilingual instruction tuning.*arXiv preprint arXiv:2306.04387*, 2023.
* Lin (2004)Lin, C.-Y.Rouge: A package for automatic evaluation of summaries.In*Proceedings of the Workshop on Text Summarization Branches Out (WAS 2004)*, pp.  74–81, Barcelona, Spain, 2004. Association for Computational Linguistics.
* Liu (2022)Liu, J.Llamaindex.[https://github.com/jerryjliu/llama\_index](https://github.com/jerryjliu/llama_index), 2022.Version archived at Zenodo, doi:10.5281/zenodo.1234.
* Mindee (2021)Mindee.doctr: Document text recognition.[https://github.com/mindee/doctr](https://github.com/mindee/doctr), 2021.
* Navarro (2001)Navarro, G.A guided tour to approximate string matching.*ACM computing surveys (CSUR)*, 33(1):31–88, 2001.
* OpenAI (2025)OpenAI.Openai o3 and o4-mini system card.[https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf](https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf), 2025.Accessed: 2025-05-23.
* Papineni et al. (2002)Papineni, K., Roukos, S., Ward, T., and Zhu, W.-J.Bleu: a method for automatic evaluation of machine translation.In*Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL)*, pp.  311–318, 2002.
* Paruchuri &amp; Team (2025)Paruchuri, V. and Team, D.Surya: A lightweight document ocr and analysis toolkit.[https://github.com/VikParuchuri/surya](https://github.com/VikParuchuri/surya), 2025.GitHub repository.
* Penedo et al. (2024)Penedo, G., Kydlíček, H., Cappelli, A., Sasko, M., and Wolf, T.Datatrove: large scale data processing, 2024.URL[https://github.com/huggingface/datatrove](https://github.com/huggingface/datatrove).
* Pietsch et al. (2019)Pietsch, M., Möller, T., Kostic, B., Risch, J., Pippi, M., Jobanputra, M., Zanzottera, S., Cerza, S., Blagojevic, V., Stadelmann, T., Soni, T., and Lee, S.Haystack: the end-to-end nlp framework for pragmatic builders, 2019.URL[https://github.com/deepset-ai/haystack](https://github.com/deepset-ai/haystack).Accessed: 2025-05-26.
* Project Gutenberg (1971)Project Gutenberg.Project gutenberg.[https://www.gutenberg.org/](https://www.gutenberg.org/), 1971.Accessed: 2025-05-26.
* Radford et al. (2023)Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., and Sutskever, I.Robust speech recognition via large-scale weak supervision.In*International conference on machine learning*, pp.  28492–28518. PMLR, 2023.
* Sallinen et al. (2025)Sallinen, A., Solergibert, A.-J., Zhang, M., Boyé, G., Dupont-Roc, M., Theimer-Lienhard, X., Boisson, E., Bernath, B., Hadhri, H., Tran, A., et al.Llama-3-meditron: An open-weight suite of medical llms based on llama-3.1.In*Workshop on Large Language Models and Generative AI for Health at AAAI 2025*, 2025.
* Team (2024)Team, N. I. D.*NVIDIA Ingest: An accelerated pipeline for document ingestion*, 2024.URL[https://github.com/NVIDIA/nv-ingest](https://github.com/NVIDIA/nv-ingest).
* Unstract (2025)Unstract.Llmwhisperer.[https://unstract.com/llmwhisperer/](https://unstract.com/llmwhisperer/), 2025.Accessed: 2025-05-25.
* Unstructured-IO (2025)Unstructured-IO.Unstructured: Open-source pre-processing tools for unstructured data.[https://github.com/Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured), 2025.Accessed: 2025-05-26.
* Villalobos et al. (2022)Villalobos, P., Ho, A., Sevilla, J., Besiroglu, T., Heim, L., and Hobbhahn, M.Will we run out of data? limits of LLM scaling based on human-generated data.*arXiv preprint arXiv:2211.04325*, 2022.doi:10.48550/arXiv.2211.04325.URL[https://arxiv.org/abs/2211.04325](https://arxiv.org/abs/2211.04325).
* Villalobos et al. (2024)Villalobos, P., Ho, A., Sevilla, J., Besiroglu, T., Heim, L., and Hobbhahn, M.Will we run out of data? limits of LLM scaling based on human-generated data  (v2, 2024 update).*arXiv preprint arXiv:2211.04325v2*, 2024.doi:10.48550/arXiv.2211.04325.URL[https://arxiv.org/abs/2211.04325v2](https://arxiv.org/abs/2211.04325v2).Version 2, revised 4 June 2024.
## Appendix AAppendix
### A.1Document Ingestion
To better situateMMOREwithin the ecosystem of document ingestion systems, Table[A.1](https://arxiv.org/html/2509.11937v1#A1.SS1)presents a fine-grained comparison with two representative alternatives:DoclingandNV-Ingest(part of NeMo Retriever). We evaluate them across modality support, indexing capabilities, and RAG integration. Green cells indicate native support, while grey cells denote the absence of the corresponding capability.
|Feature|Docling|NV-Ingest111[NeMo Retriever Documentation](https://docs.nvidia.com/nemo/retriever/extraction/overview/)|MMORE|
\\rowcolorgray!20Supported Modalities|
PDF|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|
DOCX|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|
PPTX|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|
XLSX / spreadsheets|\\cellcolorTickGreen✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
TXT|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|
HTML|\\cellcolorTickGreen✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
Markdown|\\cellcolorTickGreen✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
CSV|\\cellcolorTickGreen✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
Images (PNG/JPEG/SVG/TIFF/BMP)|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|
Audio|\\cellcolorLightGrey✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
Video|\\cellcolorLightGrey✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
EML|\\cellcolorLightGrey✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
\\rowcolorgray!20Indexing &amp; Embedding|
Native engine included|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|
LangChain / LlamaIndex connector|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|
\\rowcolorgray!20RAG|
Built–in RAG pipeline|\\cellcolorLightGrey✓|\\cellcolorLightGrey✓|\\cellcolorTickGreen✓|
Plugin–based RAG|\\cellcolorTickGreen✓|\\cellcolorTickGreen✓|\\cellcolorLightGrey✓|
Open–Source license|MIT|Apache 2.0|Apache 2.0|
Table 3:Fine-grained comparison of Docling, NV-Ingest, and MMORE document-ingestion pipelines. Green cells indicate native support; grey cells indicate absence of the capability.
MMOREsupports a wide range of file formats through modular extractors. For each supported type, we define adefault modeprioritizing accuracy and afast modeoptimized for speed. When no alternative tool is available, the fast mode is left unspecified (–). A complete list of tools used per file type is shown in Table[4](https://arxiv.org/html/2509.11937v1#A1.T4).
|File Type|Default Mode Tool(s)|Fast Mode Tool(s)|
\\rowcolorgray!5
DOCX|python-docxfor text and image extraction|–|
MD|markdownfor text,markdownifyfor HTML conversion|–|
\\rowcolorgray!5
PPTX|python-pptxfor text and image extraction|–|
XLSX|openpyxlfor table and text extraction|–|
\\rowcolorgray!5
TXT|Python built-inopen()|–|
EML|Python built-inemailmodule|–|
\\rowcolorgray!5
Audio/Video (MP4, MP3, etc.)|moviepyfor frames,whisper-large-v3-turbofor transcription|whisper-tiny|
PDF|marker-pdffor OCR/structured data|PyMuPDF|
\\rowcolorgray!5
HTML|BeautifulSoup|–|
Table 4:Overview of supported file types and extraction tools inMMORE. Full URLs are included in the project documentation.
### A.2Multimodal Sample
The format provides a standardized representation for processed documents, combining extracted text with references to non-text elements. As shown in the example, the ”text” field contains the document’s content with&lt;attachment&gt;placeholders (which are configurable) marking modality locations, while the modalities array contains all embedded objects with their types and storage paths.
Format Example:[⬇](data:text/plain;base64,ewogICJ0ZXh0IjogIkEgcmVwb3J0IGNvbnRhaW5pbmcgYSBjb29sIGltYWdlIDxhdHRhY2htZW50PiBhbmQgYSBjaGFydCA8YXR0YWNobWVudD4uLi4iLAogICJtb2RhbGl0aWVzIjogWwogICAgewogICAgICAidHlwZSI6ICJpbWFnZSIsCiAgICAgICJ2YWx1ZSI6ICJjaGFydF91cmxfMi5wbmciCiAgICB9LAogICAgewogICAgICAidHlwZSI6ICJpbWFnZSIsCiAgICAgICJ2YWx1ZSI6ICJjaGFydF91cmxfMS5wbmciCiAgICB9CiAgXQp9){"text":"Areportcontainingacoolimage&lt;attachment&gt;andachart&lt;attachment&gt;...","modalities":[{"type":"image","value":"chart\_url\_2.png"},{"type":"image","value":"chart\_url\_1.png"}]}The standardized format for document processing.
### A.3Processing Accuracy - Metrics
To quantify extraction accuracy, we used a combination of machine translation, summarization and string similarity metrics. Their definitions are given below.
BLEU Score (bilingual evaluation understudy)> (
> Papineni et al.
> , [> 2002
](https://arxiv.org/html/2509.11937v1#bib.bib14)> )
:
The BLEU score evaluates the overlap between the n-grams (sequences of words of lengthnn) between the extracted text and the ground truth. It is defined as:
|BLEU=BP⋅exp⁡(∑n=1Nwn​log⁡pn)\\text{BLEU}=\\text{BP}\\cdot\\exp\\left(\\sum\_{n=1}^{N}w\_{n}\\log p\_{n}\\right)||(1)|
wherepnp\_{n}is the precision for n-grams of lengthnn, ranging from [1 to 4],wnw\_{n}are the weights (uniform), and brevity penalty (BP), given by:
|BP={1if​c&gt;rexp⁡(1−rc)if​c≤r\\text{BP}=\\begin{cases}1&amp;&amp;\\text{if }c&gt;&gt;r\\\\
\\exp\\left(1-\\frac{r}{c}\\right)&amp;&amp;\\text{if }c\\leq r\\end{cases}||(2)|
Here,ccis the length of the candidate (extracted) text, andrris the length of the reference (ground truth). BLEU considers how much of the extracted text matches the reference text in terms of word sequences, while also penalizing outputs that are too short.
ROUGE-L (recall-oriented understudy for gisting evaluation)> (
> Lin
> , [> 2004
](https://arxiv.org/html/2509.11937v1#bib.bib9)> )
:
ROUGE-L measures the quality of the extracted text using the longest common subsequence (LCS) between the extracted text and the ground truth. The LCS is the longest sequence of words appearing in the same order in both texts (though not necessarily consecutively). ROUGE-L is calculated as:
|ROUGE-L=Fmeasure=(1+β2)⋅Precision⋅Recallβ2⋅Precision+Recall\\text{ROUGE-L}=F\_{\\text{measure}}=\\frac{(1+\\beta^{2})\\cdot\\text{Precision}\\cdot\\text{Recall}}{\\beta^{2}\\cdot\\text{Precision}+\\text{Recall}}||(3)|
whereβ\\betais a weighting factor (set to 1 for equal weighting), and:
|Precision|=LCSLength of Extracted Text,\\displaystyle=\\frac{\\text{LCS}}{\\text{Length of Extracted Text}},||(4)|
|Recall|=LCSLength of Ground Truth.\\displaystyle=\\frac{\\text{LCS}}{\\text{Length of Ground Truth}}.||
Levenshtein distance - character error rate (CER)> (
> Navarro
> , [> 2001
](https://arxiv.org/html/2509.11937v1#bib.bib12)> )
:
Given two strings,s1s\_{1}(extracted text) ands2s\_{2}(ground truth), the Levenshtein distanced​(s1,s2)d(s\_{1},s\_{2})measures the minimum number of insertions, deletions, or substitutions required to transforms1s\_{1}intos2s\_{2}. We normalize this distance over the length of the ground truth and is defined as:
|CER=d​(s1,s2)|s1|\\text{CER}=\\frac{d(s\_{1},s\_{2})}{|s\_{1}|}||(5)|
