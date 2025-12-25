# 

**URL:** https://openreview.net/pdf?id=pBkTqmhMOj
**Published:** 2025-06-21T00:00:00.000Z

---

## Summary

The webpage describes the **Multiple Automated Finance Integration Agents (MAFIA)** framework, which focuses on building **self-healing, modular agentic AI systems for financial services**.

The system is designed to address concerns about reliability, auditability, and compliance when deploying autonomous AI agents in finance. The core methodology involves a pipeline where a **Financial Lending Assistant Agent** generates responses, which are then continuously monitored and corrected by a **Consumer Compliance Agent** and an **Financial Introspection Agent** that uses a rubric-based scoring system.

Key aspects relevant to your query include:

*   **Multi-agent systems for finance:** The framework explicitly uses multiple specialized agents (Lending Assistant, Compliance Agent, Introspection Agent, Security Agent, etc.) orchestrated to perform complex financial tasks.
*   **Due diligence automation/Investment opportunity analysis/Deal sourcing/Portfolio monitoring:** While the primary *use case* demonstrated is a lending assistant, the architecture is presented as a general framework for integrating agents in financial institutions, suggesting applicability to these areas.
*   **Agents for data analysis, financial report generation:** The system includes a **Knowledge Agent** connected to knowledge graphs and a **Data Interface Agent** for secure data lookup, supporting data-driven tasks.
*   **Integrations:** The framework is designed to interface with various components, including **Foundation Model Interface Modules** (implying integration with various LLMs like GPT, Claude, Llama) and utilizes **RAG (Retrieval-Augmented Generation)** for domain-specific knowledge.

**Note on Specific Tools:** The text mentions the general concept of integrating with external knowledge bases but **does not explicitly list integrations with PitchBook, AlphaSense, Preqin, CapIQ, or Bloomberg.**

---

## Full Content

Multiple Automated Finance Integration Agents (MAFIA) With Self-Healing
Arya Sarukkai * 1 2 Shaohui Sun * 1 Wei Dai 1
Abstract
The integration of agentic artificial intelligence
(AI) into financial services presents both transformative opportunities and critical challenges.
Agentic systems, autonomous AI agents capable
of goal-directed reasoning, adaptation, and collaboration, are increasingly being deployed in highstakes domains such as lending, compliance, and
audit. However, the autonomous and evolving
nature of these agents raises substantial concerns
about reliability, auditability, adversarial robustness, and regulatory compliance. In this paper, we
propose a framework for constructing self-healing,
modular agentic systems that interoperate within
financial institutions while maintaining correctness and oversight: Multiple Automated Finance
Integrated Agents (MAFIA). In addition, we introduce the notion of self-healing, a framework that
scores and self-corrects based on a rubric scoring technique tailored to finance. We focus on a
representative use case where a lending assistant
agent is continuously monitored and audited by a
consumer compliance agent. Through baseline experiments involving sensitive prompt evaluation
and downstream auditing, we assess the system’s
alignment with institutional constraints. We further propose an advanced self-learning setup in
which agent feedback loops enhance system responses over time, reinforcing accuracy and compliance. Our findings illustrate a path toward trustworthy agentic architectures that combine automation with enforceable safeguards, paving the way
for the secure deployment of AI agents in finance.
1. Introduction
The financial services industry is experiencing a transformative change with the advent of artificial intelligence systems
*Equal contribution 1
Prajna Inc 2Saratoga High School,
Saratoga, CA United States. Correspondence to: Arya Sarukkai
.
Accepted at the ICML 2025 Workshop on Collaborative and
Federated Agentic Workflows (CFAgentic@ICML’25), Vancouver,
Canada. July 19, 2025. Copyright 2025 by the author(s).
(AI), autonomous agents capable of perceiving, reasoning,
acting, and learning with minimal human intervention (Figure1). Unlike traditional AI models that operate under strict
human supervision, agentic AI systems can independently
execute complex tasks, adapt to dynamic environments, and
collaborate with other agents to achieve overarching objectives. This evolution is particularly impactful in financial
companies, where tasks such as lending, compliance monitoring, and risk assessment demand both precision and
adaptability.
Figure 1. Growth of AI adoption in financial businesses worldwide in 2022 and 2025 (Source: https://techreport.com/statistics/aistatistics/)
Recent advances have led to the deployment of agentic AI
systems across financial services, where they are used to
automate workflows, enhance compliance, and improve risk
management—ultimately driving operational efficiency and
innovation (Fosdike, 2025; Kaur, 2025). These systems
can autonomously review financial records, detect anomalies, and generate preliminary audit reports, thereby reducing manual workload and improving accuracy. In addition,
agentic AI’s capacity to process large volumes of data in
real time enables dynamic risk assessment and proactive
compliance monitoring, both of which are crucial in today’s
fast-evolving regulatory environment (Singh, 2025).
Despite these benefits, the integration of agentic AI into
financial workflows introduces significant challenges, particularly around transparency, accountability, and ethical
risk. The autonomous behavior of these systems raises concerns about how decisions are made, potential biases in
their outputs, and the auditability of their reasoning processes. Ensuring that each decision is explainable, compli1
Multiple Automated Finance Integration Agents (MAFIA) With Self-Healing
ant, and traceable is essential. Moreover, an over reliance
on such technologies without appropriate oversight mechanisms could result in unintended consequences, highlighting
the need for governance structures that balance innovation
with rigorous control (Colback, 2025).
In this paper, we present a framework for integrating complementary agentic systems to build robust and auditable
solutions for financial institutions. We specifically demonstrate how a lending assistant agent can be reviewed and corrected by a consumer compliance agent, forming a pipeline
that defends against hallucinations, adversarial inputs, and
regulatory misalignment. Our approach not only addresses
technical integration, but also emphasizes continuous learning and adaptive refinement to ensure sustained accuracy,
robustness, and regulatory compliance over time.
2. Related Work
2.1. Agentic AI Systems
Agentic AI systems represent a recent shift in the development of autonomous software entities that can pursue goals,
decompose tasks, interact with external environments, and
collaborate with other agents (Park et al., 2023). Unlike
conventional machine learning systems, which are typically
static and monolithic, agentic systems are modular and capable of dynamic behavior, making them well-suited to
real-world applications in business, healthcare, and finance.
Notable frameworks such as AutoGPT (Gravitas, 2023),
BabyAGI (Nakajima, 2023), and LangGraph (LangChain,
2024) demonstrate early efforts in chaining and orchestrating agents for complex tasks, though they often lack robust
safety and compliance mechanisms necessary for regulated
environments like finance.
2.2. AI for Financial Compliance and Risk Management
AI applications in finance have traditionally focused on
credit scoring, fraud detection, and algorithmic trading (Li
& Zhang, 2021; Narayanan & Kumar, 2022). More recently,
the need for explainable and auditable AI has driven interest
in regulatory compliance use cases (Barocas & Selbst, 2020;
Brkan, 2021). Tools such as SHAP and LIME have been
employed for post hoc explainability, while domain-specific
rule engines have attempted to inject policy into model outputs. However, most existing systems are not agentic in
nature—they lack the autonomy, inter-agent communication, and self-reflection capabilities required to adapt to new
compliance constraints dynamically.
2.3. Auditable and Self-Learning Architectures
Recent work has explored mechanisms for increasing the
reliability and auditability of AI agents in dynamic contexts. Xu et al. (2025) propose reward modeling via human
feedback in complex agent chains. Yao et al. (2022) introduce a reasoning-and-acting framework to improve transparency and control during task decomposition. In highstakes domains, self-monitoring and inter-agent critique
have emerged as potential tools for risk mitigation (Zhou
et al., 2023). However, these approaches are typically tested
in synthetic or open-domain settings. Our work extends
this line of inquiry by embedding a compliance auditing
agent within a financial decision-making agent loop, and by
enabling self-improvement via constrained fine-tuning and
critique-based adaptation.
2.4. Modular Agentic Architectures
Modular designs in agentic AI facilitate scalability and flexibility, allowing for the decomposition of complex financial
tasks into manageable sub-components. Huang and Tanaka
(Huang & Tanaka, 2021) introduced MSPM, a modular
multi-agent reinforcement learning system tailored for financial portfolio management. Their architecture employs
evolving and strategic agent modules to handle heterogeneous data and decision-making processes. Similarly, Cho
et al. (Cho et al., 2024) proposed FISHNET, an agentic
framework that processes vast regulatory filings through a
swarm of specialized agents, demonstrating improved performance in financial intelligence tasks.
2.5. Self-Learning and Adaptation in Financial Agents
The capacity for self-learning enables agentic systems to
adapt to dynamic financial environments. Yu et al. (Yu et al.,
2024) developed FinCon, a multi-agent system incorporating conceptual verbal reinforcement to enhance financial
decision-making. This architecture mirrors organizational
structures, facilitating effective communication and learning
among agents. Their results indicate superior performance
in tasks such as stock trading and portfolio management
compared to baseline models.
In (Sarukkai, 2025), the notion of a rubric based introspection to improve the responses of LLM agents is introduced.
The focus of that work was on ethical principles. In this
work, we have applied that idea to the financial domain by
defining a financial scoring rubric and evaluating responses
based on that to score and improve.
2.6. Auditability and Compliance in Agentic Systems
Ensuring auditability and compliance is paramount in deploying AI within regulated financial sectors. Recent studies
emphasize the importance of transparent and explainable
agentic systems. For instance, the work by Cho et al. (Cho
et al., 2024) highlights the role of modular agentic architectures in maintaining data integrity and facilitating compli2
Multiple Automated Finance Integration Agents (MAFIA) With Self-Healing
ance through structured processing of regulatory documents.
2.7. Federated Learning in Regulated Environments
Federated learning (FL) enables collaborative model training without centralized data sharing, making it well suited
for regulated sectors like finance. Frameworks such as
PV4AML (Research, 2023) and DPFedBank (Zhou et al.,
2024) apply privacy-preserving techniques, e.g., differential
privacy and homomorphic encryption, to ensure legal compliance during inter-institutional collaboration. Fed-RD (Li
et al., 2024) further demonstrates that secure FL can maintain high utility in financial tasks while satisfying regulatory
constraints.
2.8. Gap in the Literature
To our knowledge, no existing framework addresses the
combined challenge of (1) integrating multiple agentic systems in a regulatory environment, (2) enforcing auditability
through a structured agent oversight loop, and (3) introducing a continuous learning mechanism to improve compliance and response quality. Our work bridges this gap by
introducing an architecture that explicitly connects decisionmaking agents with compliance-oriented agents, framed
within the context of financial institutions, and grounded in
both empirical evaluation and domain relevance. Furthermore, the self-healing methodology incorporates a rubricbased scoring and refinement process, allowing more predictable and explainable results.
3. Methodology
Our methodology is centered on the design and evaluation
of a modular, self-learning agentic framework tailored to
financial enterprise applications. Specifically, we build a
system in which a loan assistant agent is continuously monitored and improved through interaction with a consumer
compliance auditor agent. This section outlines the system
architecture, experiment setup, and learning strategy.
3.1. System Architecture
Firstly, we summarize the overall agentic architecture
for our Multiple Automated Finance Integrated Agents
(MAFIA) System. The overall architecture is shown in
Figure 1 below: At a high level, these are the primary components:
• Orchestration Engine: This engine controls the execution and sequencing of agents, passing data from one
agent to another.
• Identity Agent: The identity agent is responsible for
authenticating and managing user identities. Typically,
Figure 2. MAFIA Architecture
this agent collects, validates customer data and interfaces with an Identity Provider Service (IDP), .
• Security Agent: Security agent is in charge of
multiple things security related including jailbreak
checks/protection, managing/validating that ID tokens
are being enforced,
• Audit Super-Agent Agent: This is the macro agent that
combines results from various audit checks.
• Knowledge Agent: This agent is connected to knowledge graphs, and can help validate/perform consistency
checks.
• Rubric Scoring Agent: This is the agent that uses the
rubric to score the query-response pair.
• Self-Healing Agent: This is the agent that introspects
and adapts/refines responses based on the rubric and
other criteria.
• Custom Function Agents Suite: This represents a suite
of agents such as lending agent, servicing agent, loan
assistant agent, marketing agent and more.
• Data Interface Agent: This Agent is the interface that
allows for translating LLM actions into function calls
to look up data in a protected/secure manner.
• Privacy Checker Agent: This agent is responsible for
ensuring privacy is being implemented across the system including monitoring and stripping of PII data
where ever applicable.
• Foundation Model Interface Modules: This module
provides API interfaces to wide variety of foundation
models.
• Custom Fine-tuned Foundation Models: This represents any custom foundation models that are being
utilized by the multi-agent system.
3
Multiple Automated Finance Integration Agents (MAFIA) With Self-Healing
• RAG Module: This is the RAG layer that is used by
different agents with customized data that is isolated
for each agent.
• Training pipelines, model zoos, and knowledge repositories (not shown) - the overall system includes a number of other components that are not represented in this
architecture including training pipelines/workflows,
quality management systems including human in the
loop feedback, model zoos, and data/knowledge repositories.
For the scope of the presented results, we focus on a smaller
set of primary agentic modules:
• Financial Lending Assistant Agent (Service Agent):
This agent interfaces directly with users or internal
decision-makers, responding to queries related to financial lending products, regulations, and eligibility. It is built on top of a large language model
(LLM) enhanced through domain-specific fine-tuning
and retrieval-augmented generation (RAG), enabling
it to combine general language understanding with access to up-to-date and institution-specific knowledge
bases.
• Consumer Compliance Agent: This agent functions
as an autonomous auditor, evaluating the responses generated by the service agent. It checks for adherence to
institutional policy, regulatory compliance, and ethical
standards. Empowered with both retrieval-based tools
and rule-based constraints, the agent not only identifies
violations or inconsistencies but also proactively generates revised, policy-aligned responses when necessary.
• Financial Introspection Agent (Introspection
Agent): This agent functions as an autonomous
introspection agent, evaluating the responses generated
by the Service Agent using a rubric (Sarukkai,
2025). It checks for adherence to institutional policy,
regulatory compliance, and ethical standards based
on a rubric, scoring this based on the rubric, and then
modifying the results based on various factors that
are incorporated in the rubric. Empowered with both
retrieval-based tools and rule-based constraints, the
agent not only identifies violations or inconsistencies
but also proactively generates revised, policy-aligned
responses when necessary.
The agents operate in a modular pipeline architecture, where
outputs from the lending agent are passed to the compliance
agent for evaluation and potential correction. This handoff
can occur in either streaming or batched mode, enabling
flexible integration within production workflows.
Figure 3. Agentic self-healing framework combining a Service
Agent with an integrated Consumer Compliance Agent, enabling
real-time audit and self-improvement.
Privacy-Preserving Agent Collaboration Although the
agents operate collaboratively to improve response quality and policy alignment, no raw user data or sensitive institutional information is shared between them. Instead,
agents exchange only intermediate representations such as
rubric scores, compliance flags, or anonymized response
metadata. Each agent processes data in its own secure
context, and improvements are propagated through controlled feedback mechanisms—such as scoring-based refinement prompts—rather than direct data or parameter sharing.
This architecture ensures continuous learning and coordination without compromising data privacy or violating access
boundaries.
3.2. Baseline Evaluation Setup
To assess the baseline behavior of our system, we constructed a benchmark dataset of 100 “sensitive or challenging” queries derived from real-world lending scenarios. The
experimental flow is as follows:
1. Generate responses to these 100 prompts using the
Service Agent.
2. Pass these responses to the Compliance Agent, which
reformulates them for external communication.
3. Evaluate the quality, correctness, and compliance of
the marketing outputs using the Consumer Compliance
Agent and human reviewers.
Metrics include fluency, factual correctness, compliance
alignment, and adversarial robustness.
3.3. Rubric for Financial Lending Assistants
In this section, we describe the rubric used for evaluating
and scoring financial lending assistants. At a high level,
4
Multiple Automated Finance Integration Agents (MAFIA) With Self-Healing
the main dimensions of focus include consumer protection,
lending compliance, privacy, ethics, user experience and
operational risks. This is summarized in table 1, while
table 2 shows how the score range is interpreted by the
self-healing system.
The intent is to balance all the different factors related to
the functional and practical aspects of how a AI lending
assistant will interact with end consumers.
3.4. Guardrails and Safety Mechanisms
To ensure robustness and reliability, we incorporate multiple safety layers designed to mitigate hallucinations, adversarial attacks, and compliance risks: Red Teaming: We
systematically introduce adversarial queries to probe the
system’s boundaries and evaluate its resilience under stress
conditions.Reject Mechanism: The Compliance Agent is
empowered to flag, withhold, or revise outputs that violate
regulatory or institutional guidelines before dissemination.
Audit Traceability: All decision pathways are logged with
timestamped, interpretable rationales, enabling transparent,
post-hoc audits and regulatory reviews.
3.5. Implementation Details
Our framework is implemented in Python and interfaces
with agentic services over a RESTful API. The system is
designed to operate in two primary stages: response generation and compliance verification with self-improvement.
Each component is modular, supporting reproducibility, auditability, and future extension.
Stage 1: Response Generation. We begin by ingesting
a curated set of domain-specific queries—such as those
related to mortgage eligibility, product disclosure, and marketing language—stored in a structured Excel file. These
questions are programmatically submitted to the Service
Agent, a domain-aligned language agent built atop a large
language model (LLM) enhanced with retrieval-augmented
generation (RAG). The agent synthesizes responses conditioned on relevant institutional documents and regulatory
guidance retrieved in real time. The results are captured in
a JSONL log containing the original question, generated
answer, and a timestamp. To increase robustness, we implement a retry mechanism with a configurable delay to handle
transient API errors.
Stage 2: Compliance Verification and Self-healing All
outputs from the Service Agent are passed to the Compliance Agent, which shares the same foundation but is further
specialized for regulatory interpretation and policy alignment. The Compliance Agent performs a two-step evaluation using a technique we term critical prompting. First, it
is asked to explicitly assess the generated answer: “Check
Table 1. Financial Lending Assistant AI Scoring Rubric
Category Focus Areas Total
Points
Consumer ProtectionProtected classes, fair
treatment, transparency,
clear language, vulnerability accommodation,
dispute resolution
25
Lending ComplianceLicense boundaries,
CFPB regulations,
FAIR lending laws,
TILA/RESPA, steering
prevention, disclosure
timing
25
Privacy/Data ProtectionPII handling, consent
management, data minimization, security protocols, retention practices, third-party sharing
20
Ethics/Responsible
AI
AI transparency, human
oversight, manipulation
avoidance, financial literacy, accountability
15
User Experience Information accuracy,
consistency, error handling, timeliness, appropriate referrals
10
Operational Risk Inappropriate request
handling, documentation, version control,
crisis protocols
5
TOTAL 100
Table 2. Scoring Guide
Score Range Interpretation
90-100 Exceptional - Exceeds compliance and quality requirements
80-89 Strong - Fully compliant with
minor improvement opportunities
70-79 Satisfactory - Generally compliant with notable improvement areas
60-69 Needs Improvement - Some
compliance concerns requiring attention
Below 60 Unacceptable - Significant
compliance risks requiring immediate remediation
5
Multiple Automated Finance Integration Agents (MAFIA) With Self-Healing
the answer for whether it may be in violation of marketing
compliance”. This prompt encourages the model to reflect
on the response through a regulatory lens.
If the agent determines the original response to be potentially non-compliant—based on heuristic keywords such as
“violation,” “misleading,” or “non-conforming”—a followup prompt is issued: “Generate a compliant version of this
mortgage marketing answer that avoids violations”. This
triggers a second-generation step aimed at rewriting the response in a legally defensible manner. The revised answer
is then re-submitted to the Compliance Agent for a final
verification pass using the same critical assessment prompt.
This is further enhanced with the rubric-based self-healing
technique as well.
4. Results and Analysis
We evaluated the effectiveness of our agentic self-learning
pipeline on a curated benchmark of 100 mortgage-related
prompts. These prompts were representative of typical
queries posed by end-users or internal stakeholders, including eligibility criteria, product descriptions, and promotional
language. We conducted experiments with several LLMs,
including GPT, Claude, and Llama. GPT-4o was used as
the foundation model for custom agents, while the Claude
3.5 Sonnet model was used for rubric scoring as well as
self-healing. The table below summarizes the results:
Table 3. Summary of self-healing experimental results
Method RScore %Violation %Gain
Baseline 74.08 22 % -
SH - 11 % 50 %
SH-R 93.55 1 % 95.45 %
4.1. Compliance Violation Detection
Out of the 100 responses generated by the Service Agent,
22 were flagged by the Compliance Agent as potentially in
violation of marketing or consumer compliance regulations.
Violations included the use of ambiguous terms such as
’guaranteed approval’, the omission of required disclaimers,
or language that could be interpreted as misleading by regulatory standards (e.g., Truth in Lending Act or RESPA
guidelines). This yields an initial violation rate of 22%,
highlighting the importance of independent compliance assessment even for enhanced LLMs via retrieval.
4.2. Refinement and Post-Verification Outcomes
For each of the 22 flagged responses, a second-stage of
agents were applied to evaluate and refine the responses.
Two techniques were evaluated - self-healing with and without a formal rubric. These techniques are labelled as SH
and SH-R in the experimental results Table 3.
In the SH method, the responses were evaluated with the
Compliance agent and self-healing used to improve responses. Using this method, of the 22 revised responses, 11
passed the subsequent compliance check without further violations, resulting in a 50% refinement success rate. In the
SH-R method, additionally a rubric was used to score the response from a compliance perspective, and used to improve
responses for low scoring outputs. With this approach, the
system was able to extract and improve further as well, only
one response left is still in violation. This demonstrates the
potential of agentic self-refinement loops to correct for regulatory misalignment when initial generations fall short. The
remaining 11 cases exhibited minor residual issues such as
insufficient specificity or vague language—highlighting the
need for additional tools (e.g., symbolic rule-based validators or human-in-the-loop auditing) in high-stakes domains.
4.3. Discussion
The improvement trajectory underscores the effectiveness
of critical prompting and iterative refinement for highreliability applications. It also surfaces limitations inherent
in current LLM-based compliance agents: Partial Comprehension of Legal Nuance: Some violations were missed
due to subtle regulatory requirements that are not well captured in the training corpus.Inconsistent Judgments: The
Compliance Agent occasionally showed variability in detecting or confirming violations across similar answers. Need
for Multi-agent Consensus: Introducing secondary agents
or external rule-checkers could help address variance and
edge-case misjudgments.
5. Future Work
Future work will explore reinforcement learning with human
feedback (RLHF), multi-agent debate, and deeper retrieval
pipelines to further improve both compliance accuracy and
self-correction efficacy.
Federated Extension for Multi-Institution Collaboration
To enable cross-institutional collaboration without compromising proprietary data or customer privacy, the MAFIA
framework can be extended through federated learning. In
this setup, each financial institution hosts its own set of
agents (e.g., lending, compliance, introspection) that learn
from local data. Model updates, rather than raw data, are
securely shared with a central coordinator, who aggregates
these updates to improve a shared global model. This allows
institutions to collectively benefit from broader patterns and
regulatory intelligence while maintaining strict data boundaries and compliance with privacy regulations. These findings confirm that modularity and reward-based refinement
are critical to system performance.
6
Multiple Automated Finance Integration Agents (MAFIA) With Self-Healing
Impact Statement
This paper presents work whose goal is to advance the field
of Machine Learning. There are many potential societal
consequences of our work, none which we feel must be
specifically highlighted here.
References
Barocas, S. and Selbst, A. D. The hidden assumptions
behind ai explanations. Harvard Journal of Law & Technology, 33(1):1–34, 2020.
Brkan, M. Transparency obligations in the age of ai. European Law Journal, 27(1-3):1–15, 2021.
Cho, N., Srishankar, N., Cecchi, L., and Watson, W. Fishnet:
Financial intelligence from sub-querying, harmonizing,
neural-conditioning, expert swarms, and task planning.
arXiv preprint arXiv:2410.19727, 2024.
Colback, L. Ai agents: from co-pilot to autopilot,
2025. URL https://www.ft.com/content/
3e862e23-6e2c-4670-a68c-e204379fe01f.
Fosdike, H. 9 essential benefits of agentic ai in financial services, 2025. URL
https://www.symphonyai.com/
resources/blog/financial-services/
benefits-agentic-ai/.
Gravitas, S. Autogpt: Build, deploy, and
run ai agents. https://github.com/
Significant-Gravitas/AutoGPT, 2023.
Accessed: 2025-05-09.
Huang, Z. and Tanaka, F. Mspm: A modularized and
scalable multi-agent reinforcement learning-based system for financial portfolio management. arXiv preprint
arXiv:2102.03502, 2021.
Kaur, J. Agentic ai for risk management, 2025.
URL https://www.xenonstack.com/blog/
agentic-ai-risk-management.
LangChain. Langgraph: Stateful orchestration framework
for agentic applications. https://www.langchain.
com/langgraph, 2024. Accessed: 2025-05-09.
Li, W. and Zhang, H. Ai-enhanced credit scoring systems.
Journal of Financial Technology, 12(3):45–58, 2021.
Li, Y., Zhang, J., and Liu, W. Fed-rd: Privacy-preserving
federated learning for financial transactions. arXiv
preprint arXiv:2408.01609, 2024.
Nakajima, Y. Babyagi: An experimental framework for a
self-building autonomous agent. https://github.
com/yoheinakajima/babyagi, 2023. Accessed:
2025-05-09.
Narayanan, A. and Kumar, S. Ai fraud detection in banking.
International Journal of Financial Security, 15(2):89–
102, 2022.
Park, J. S., O’Brien, J. C., Cai, C. J., Morris, M. R.,
Liang, P., and Bernstein, M. S. Generative agents: Interactive simulacra of human behavior. arXiv preprint
arXiv:2304.03442, 2023. URL https://arxiv.
org/abs/2304.03442.
Research, I. Privacy-preserving federated learning in finance with pv4aml. Online, 2023.
https://research.ibm.com/blog/
privacy-preserving-federated-learning-finance.
Sarukkai, A. Ethical introspection for improving child llm interactions. https:
//spring-symposia-proceedings.aaai.
org/preprints/CHLD6153.pdf, 2025.
Singh, B. Rethinking compliance and governance with agentic process automation, 2025.
URL https://www.linkedin.com/pulse/
rethinking-compliance-governance-agentic-process-
Xu, Y., Zhang, W., Li, M., Chen, H., and Wang, L.
Agentic reward modeling: Integrating human preferences with verifiable correctness signals. arXiv preprint
arXiv:2502.19328, 2025. URL https://arxiv.
org/abs/2502.19328.
Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
K., and Cao, Y. React: Synergizing reasoning and acting
in language models. arXiv preprint arXiv:2210.03629,
2022. URL https://arxiv.org/abs/2210.
03629.
Yu, Y., Yao, Z., Li, H., Deng, Z., Cao, Y., Chen, Z., Suchow,
J. W., Liu, R., Cui, Z., Xu, Z., Zhang, D., Subbalakshmi, K., Xiong, G., He, Y., Huang, J., Li, D., and Xie,
Q. Fincon: A synthesized llm multi-agent system with
conceptual verbal reinforcement for enhanced financial
decision making. arXiv preprint arXiv:2407.06567, 2024.
Zhou, L., Wang, M., and Chen, X. Critique-based risk
mitigation in ai systems. Journal of AI Safety Research,
5(2):123–137, 2023.
Zhou, X., Wang, L., and Yang, Q. Dpfedbank: A policycompliant framework for federated learning in finance.
arXiv preprint arXiv:2410.13753, 2024.
7
