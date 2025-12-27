# Computer Science > Artificial Intelligence

**URL:** https://arxiv.org/abs/2412.12119
**Published:** 2024-12-02T00:00:00.000Z

---

## Summary

The webpage describes a paper titled "Mastering Board Games by External and Internal Planning with Language Models." This work focuses on **advancing the planning and reasoning capabilities of Large Language Models (LLMs)** to enable reliable performance in complex domains, specifically demonstrated through board games (Chess, Fischer Random/Chess960, Connect Four, and Hex).

The paper introduces and compares two search-based planning approaches:
1.  **External Search:** The LLM guides **Monte Carlo Tree Search (MCTS)** rollouts and evaluations without relying on an external game engine.
2.  **Internal Search:** The LLM is trained to generate a linearized tree of search and the final choice **in-context**.

Both methods build upon an LLM pre-trained on domain knowledge to capture transition and value functions with minimal **hallucinations**. The results show substantial improvements in strength over the base model, achieving **Grandmaster-level performance in chess** while operating within a human-like search budget. This approach suggests general future applications beyond board games.

The summary directly addresses several concepts in your query:
*   **Reasoning LLMs** and **planning with LLMs** are central themes.
*   **MCTS (Monte Carlo Tree Search) for language models** is explicitly mentioned as part of the external search approach.
*   **Hallucination reduction** is noted as a goal achieved by minimizing hallucinations.

---

## Full Content

[2412.12119] Mastering Board Games by External and Internal Planning with Language Models
[Skip to main content](#content)
[![Cornell University](https://arxiv.org/static/browse/0.3.4/images/icons/cu/cornell-reduced-white-SMALL.svg)](https://www.cornell.edu/)
We gratefully acknowledge support from the Simons Foundation,[member institutions](https://info.arxiv.org/about/ourmembers.html), and all contributors.[Donate](https://info.arxiv.org/about/donate.html)
[](https://arxiv.org/IgnoreMe)
[![arxiv logo](https://arxiv.org/static/browse/0.3.4/images/arxiv-logo-one-color-white.svg)](https://arxiv.org/)&gt;[cs](https://arxiv.org/list/cs/recent)&gt;arXiv:2412.12119
[Help](https://info.arxiv.org/help)|[Advanced Search](https://arxiv.org/search/advanced)
All fieldsTitleAuthorAbstractCommentsJournal referenceACM classificationMSC classificationReport numberarXiv identifierDOIORCIDarXiv author IDHelp pagesFull text
Search
[![arXiv logo](https://arxiv.org/static/browse/0.3.4/images/arxiv-logomark-small-white.svg)](https://arxiv.org/)
[![Cornell University Logo](https://arxiv.org/static/browse/0.3.4/images/icons/cu/cornell-reduced-white-SMALL.svg)](https://www.cornell.edu/)
open search
GO
open navigation menu
# Computer Science \> Artificial Intelligence
**arXiv:2412.12119**(cs)
[Submitted on 2 Dec 2024 ([v1](https://arxiv.org/abs/2412.12119v1)), last revised 23 May 2025 (this version, v3)]
# Title:Mastering Board Games by External and Internal Planning with Language Models
Authors:[John Schultz](https://arxiv.org/search/cs?searchtype=author&amp;query=Schultz,+J),[Jakub Adamek](https://arxiv.org/search/cs?searchtype=author&amp;query=Adamek,+J),[Matej Jusup](https://arxiv.org/search/cs?searchtype=author&amp;query=Jusup,+M),[Marc Lanctot](https://arxiv.org/search/cs?searchtype=author&amp;query=Lanctot,+M),[Michael Kaisers](https://arxiv.org/search/cs?searchtype=author&amp;query=Kaisers,+M),[Sarah Perrin](https://arxiv.org/search/cs?searchtype=author&amp;query=Perrin,+S),[Daniel Hennes](https://arxiv.org/search/cs?searchtype=author&amp;query=Hennes,+D),[Jeremy Shar](https://arxiv.org/search/cs?searchtype=author&amp;query=Shar,+J),[Cannada Lewis](https://arxiv.org/search/cs?searchtype=author&amp;query=Lewis,+C),[Anian Ruoss](https://arxiv.org/search/cs?searchtype=author&amp;query=Ruoss,+A),[Tom Zahavy](https://arxiv.org/search/cs?searchtype=author&amp;query=Zahavy,+T),[Petar Veličković](https://arxiv.org/search/cs?searchtype=author&amp;query=Veličković,+P),[Laurel Prince](https://arxiv.org/search/cs?searchtype=author&amp;query=Prince,+L),[Satinder Singh](https://arxiv.org/search/cs?searchtype=author&amp;query=Singh,+S),[Eric Malmi](https://arxiv.org/search/cs?searchtype=author&amp;query=Malmi,+E),[Nenad Tomašev](https://arxiv.org/search/cs?searchtype=author&amp;query=Tomašev,+N)
View a PDF of the paper titled Mastering Board Games by External and Internal Planning with Language Models, by John Schultz and 15 other authors
[View PDF](https://arxiv.org/pdf/2412.12119)[HTML (experimental)](https://arxiv.org/html/2412.12119v3)> > Abstract:
> Advancing planning and reasoning capabilities of Large Language Models (LLMs) is one of the key prerequisites towards unlocking their potential for performing reliably in complex and impactful domains. In this paper, we aim to demonstrate this across board games (Chess, Fischer Random / Chess960, Connect Four, and Hex), and we show that search-based planning can yield significant improvements in LLM game-playing strength. We introduce, compare and contrast two major approaches: In external search, the model guides Monte Carlo Tree Search (MCTS) rollouts and evaluations without calls to an external game engine, and in internal search, the model is trained to generate in-context a linearized tree of search and a resulting final choice. Both build on a language model pre-trained on relevant domain knowledge, reliably capturing the transition and value functions in the respective environments, with minimal hallucinations. We evaluate our LLM search implementations against game-specific state-of-the-art engines, showcasing substantial improvements in strength over the base model, and reaching Grandmaster-level performance in chess while operating closer to the human search budget. Our proposed approach, combining search with domain knowledge, is not specific to board games, hinting at more general future applications. Comments:|70 pages, 10 figures|
Subjects:|Artificial Intelligence (cs.AI); Computation and Language (cs.CL); Machine Learning (cs.LG)|
Cite as:|[arXiv:2412.12119](https://arxiv.org/abs/2412.12119)[cs.AI]|
|(or[arXiv:2412.12119v3](https://arxiv.org/abs/2412.12119v3)[cs.AI]for this version)|
|[https://doi.org/10.48550/arXiv.2412.12119](https://doi.org/10.48550/arXiv.2412.12119)
Focus to learn more
arXiv-issued DOI via DataCite
|
## Submission history
From: Matej Jusup [[view email](https://arxiv.org/show-email/26e12cf5/2412.12119)]
**[[v1]](https://arxiv.org/abs/2412.12119v1)**Mon, 2 Dec 2024 18:56:51 UTC (3,124 KB)
**[[v2]](https://arxiv.org/abs/2412.12119v2)**Tue, 29 Apr 2025 18:06:45 UTC (680 KB)
**[v3]**Fri, 23 May 2025 01:35:09 UTC (680 KB)
Full-text links:## Access Paper:
View a PDF of the paper titled Mastering Board Games by External and Internal Planning with Language Models, by John Schultz and 15 other authors
* [View PDF](https://arxiv.org/pdf/2412.12119)
* [HTML (experimental)](https://arxiv.org/html/2412.12119v3)
* [TeX Source](https://arxiv.org/src/2412.12119)
[![license icon](https://arxiv.org/icons/licenses/by-4.0.png)view license](http://creativecommons.org/licenses/by/4.0/)
Current browse context:
cs.AI
[&lt;&lt;prev](https://arxiv.org/prevnext?id=2412.12119&amp;function=prev&amp;context=cs.AI) | [next&gt;&gt;](https://arxiv.org/prevnext?id=2412.12119&amp;function=next&amp;context=cs.AI)
[new](https://arxiv.org/list/cs.AI/new)|[recent](https://arxiv.org/list/cs.AI/recent)|[2024-12](https://arxiv.org/list/cs.AI/2024-12)
Change to browse by:
[cs](https://arxiv.org/abs/2412.12119?context=cs)
[cs.CL](https://arxiv.org/abs/2412.12119?context=cs.CL)
[cs.LG](https://arxiv.org/abs/2412.12119?context=cs.LG)
### References &amp; Citations
* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2412.12119)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2412.12119)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2412.12119)
export BibTeX citationLoading...
## BibTeX formatted citation
&times;
loading...
Data provided by:
### Bookmark
[![BibSonomy logo](https://arxiv.org/static/browse/0.3.4/images/icons/social/bibsonomy.png)]()[![Reddit logo](https://arxiv.org/static/browse/0.3.4/images/icons/social/reddit.png)]()
Bibliographic Tools
# Bibliographic and Citation Tools
Bibliographic Explorer Toggle
Bibliographic Explorer*([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*
Connected Papers Toggle
Connected Papers*([What is Connected Papers?](https://www.connectedpapers.com/about))*
Litmaps Toggle
Litmaps*([What is Litmaps?](https://www.litmaps.co/))*
scite.ai Toggle
scite Smart Citations*([What are Smart Citations?](https://www.scite.ai/))*
Code, Data, Media
# Code, Data and Media Associated with this Article
alphaXiv Toggle
alphaXiv*([What is alphaXiv?](https://alphaxiv.org/))*
Links to Code Toggle
CatalyzeX Code Finder for Papers*([What is CatalyzeX?](https://www.catalyzex.com))*
DagsHub Toggle
DagsHub*([What is DagsHub?](https://dagshub.com/))*
GotitPub Toggle
Gotit.pub*([What is GotitPub?](http://gotit.pub/faq))*
Huggingface Toggle
Hugging Face*([What is Huggingface?](https://huggingface.co/huggingface))*
Links to Code Toggle
Papers with Code*([What is Papers with Code?](https://paperswithcode.com/))*
ScienceCast Toggle
ScienceCast*([What is ScienceCast?](https://sciencecast.org/welcome))*
Demos
# Demos
Replicate Toggle
Replicate*([What is Replicate?](https://replicate.com/docs/arxiv/about))*
Spaces Toggle
Hugging Face Spaces*([What is Spaces?](https://huggingface.co/docs/hub/spaces))*
Spaces Toggle
TXYZ.AI*([What is TXYZ.AI?](https://txyz.ai))*
Related Papers
# Recommenders and Search Tools
Link to Influence Flower
Influence Flower*([What are Influence Flowers?](https://influencemap.cmlab.dev/))*
Core recommender toggle
CORE Recommender*([What is CORE?](https://core.ac.uk/services/recommender))*
* Author
* Venue
* Institution
* Topic
About arXivLabs
# arXivLabs: experimental projects with community collaborators
arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.
Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.
Have an idea for a project that will add value for arXiv's community?[**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).
[Which authors of this paper are endorsers?](https://arxiv.org/auth/show-endorsers/2412.12119)|[Disable MathJax](javascript:setMathjaxCookie())([What is MathJax?](https://info.arxiv.org/help/mathjax.html))
