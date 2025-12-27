# Workflows and agents

**URL:** https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/
**Published:** 2025-01-01T00:00:00.000Z

---

## Summary

The webpage, titled "Workflows and agents" from LangChain Docs, discusses common patterns for building systems using LangChain and LangGraph, specifically focusing on **Workflows** and **Agents**.

Here is a summary of the content relevant to your query:

*   **Agent Frameworks:** The page is part of the **LangChain** documentation and heavily features **LangGraph** for building these systems.
*   **Tool Use/Function Calling:** Agents are described as LLMs performing actions using **tools**. The "Using tools" section provides an example of defining tools (like `multiply`, `add`, `divide`) and augmenting an LLM to use them, which is equivalent to **function calling**.
*   **Structured Outputs:** The setup section mentions that workflows and agents can use any chat model that supports **structured outputs** and tool calling. Examples throughout the document demonstrate using Pydantic models for structured output (e.g., `SearchQuery`, `Route`, `Feedback`).
*   **Agent Orchestration:** The **Orchestrator-worker** pattern explicitly describes an orchestrator breaking down tasks, delegating to workers, and synthesizing results.
*   **Agent Memory:** The navigation sidebar lists **Memory** as a capability of LangGraph, though the main body of the text focuses more on workflows and agents' immediate actions rather than deep dives into agentic memory concepts.
*   **MCP Servers, Agent Memory, Agentic Memory, OpenAI Agents SDK, Anthropic Agents SDK, Google SDK:** These specific terms are **not explicitly detailed** in the main body of the text provided. The text mentions using Anthropic models in the setup example, but does not discuss the specific SDKs for OpenAI, Anthropic, or Google, nor does it detail MCP servers or the distinction between agent memory and agentic memory.

**In summary:** The page covers **agent frameworks (LangGraph/LangChain)**, **tool use/function calling**, **structured outputs**, and **agent orchestration** patterns. It does not provide specific information on **MCP servers, OpenAI Agents SDK, Anthropic Agents SDK, Google SDK, agent memory, or agentic memory**.

---

## Full Content

Workflows and agents - Docs by LangChain
[Skip to main content](#content-area)
[Docs by LangChainhome page![light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&amp;auto=format&amp;n=Xbr8HuVd9jPi6qTU&amp;q=85&amp;s=16111530672bf976cb54ef2143478342)![dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&amp;auto=format&amp;n=Xbr8HuVd9jPi6qTU&amp;q=85&amp;s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)
LangChain + LangGraph
Search...
⌘K
Search...
Navigation
Get started
Workflows and agents
[LangChain
](https://docs.langchain.com/oss/python/langchain/overview)[LangGraph
](https://docs.langchain.com/oss/python/langgraph/overview)[Deep Agents
](https://docs.langchain.com/oss/python/deepagents/overview)[Integrations
](https://docs.langchain.com/oss/python/integrations/providers/overview)[Learn
](https://docs.langchain.com/oss/python/learn)[Reference
](https://docs.langchain.com/oss/python/reference/overview)[Contribute
](https://docs.langchain.com/oss/python/contributing/overview)
Python
* [
Overview
](https://docs.langchain.com/oss/python/langgraph/overview)
##### Get started
* [
Install
](https://docs.langchain.com/oss/python/langgraph/install)
* [
Quickstart
](https://docs.langchain.com/oss/python/langgraph/quickstart)
* [
Local server
](https://docs.langchain.com/oss/python/langgraph/local-server)
* [
Changelog
](https://docs.langchain.com/oss/python/releases/changelog)
* [
Thinking in LangGraph
](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
* [
Workflows + agents
](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
##### Capabilities
* [
Persistence
](https://docs.langchain.com/oss/python/langgraph/persistence)
* [
Durable execution
](https://docs.langchain.com/oss/python/langgraph/durable-execution)
* [
Streaming
](https://docs.langchain.com/oss/python/langgraph/streaming)
* [
Interrupts
](https://docs.langchain.com/oss/python/langgraph/interrupts)
* [
Time travel
](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
* [
Memory
](https://docs.langchain.com/oss/python/langgraph/add-memory)
* [
Subgraphs
](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)
##### Production
* [
Application structure
](https://docs.langchain.com/oss/python/langgraph/application-structure)
* [
Test
](https://docs.langchain.com/oss/python/langgraph/test)
* [
LangSmith Studio
](https://docs.langchain.com/oss/python/langgraph/studio)
* [
Agent Chat UI
](https://docs.langchain.com/oss/python/langgraph/ui)
* [
LangSmith Deployment
](https://docs.langchain.com/oss/python/langgraph/deploy)
* [
LangSmith Observability
](https://docs.langchain.com/oss/python/langgraph/observability)
##### LangGraph APIs
* Graph API
* Functional API
* [
Runtime
](https://docs.langchain.com/oss/python/langgraph/pregel)
On this page
* [Setup](#setup)
* [LLMs and augmentations](#llms-and-augmentations)
* [Prompt chaining](#prompt-chaining)
* [Parallelization](#parallelization)
* [Routing](#routing)
* [Orchestrator-worker](#orchestrator-worker)
* [Creating workers in LangGraph](#creating-workers-in-langgraph)
* [Evaluator-optimizer](#evaluator-optimizer)
* [Agents](#agents)
[Get started](https://docs.langchain.com/oss/python/langgraph/install)
# Workflows and agents
Copy page
Copy page
This guide reviews common workflow and agent patterns.
* Workflows have predetermined code paths and are designed to operate in a certain order.
* Agents are dynamic and define their own processes and tool usage.![Agent Workflow](https://mintcdn.com/langchain-5e9cc07a/-_xGPoyjhyiDWTPJ/oss/images/agent_workflow.png?fit=max&amp;auto=format&amp;n=-_xGPoyjhyiDWTPJ&amp;q=85&amp;s=c217c9ef517ee556cae3fc928a21dc55)LangGraph offers several benefits when building agents and workflows, including[persistence](https://docs.langchain.com/oss/python/langgraph/persistence),[streaming](https://docs.langchain.com/oss/python/langgraph/streaming), and support for debugging as well as[deployment](https://docs.langchain.com/oss/python/langgraph/deploy).## [​
](#setup)
Setup
To build a workflow or agent, you can use[any chat model](https://docs.langchain.com/oss/python/integrations/chat)that supports structured outputs and tool calling. The following example uses Anthropic:
1. Install dependencies:
Copy
```
`pipinstalllangchain\_corelangchain-anthropiclanggraph`
```
1. Initialize the LLM:
Copy
```
`importosimportgetpassfromlangchain\_anthropicimportChatAnthropicdef\_set\_env(var:str):ifnotos.environ.get(var):os.environ[var]=getpass.getpass(f"{var}: ")\_set\_env("ANTHROPIC\_API\_KEY")llm=ChatAnthropic(model="claude-sonnet-4-5-20250929")`
```
## [​
](#llms-and-augmentations)
LLMs and augmentations
Workflows and agentic systems are based on LLMs and the various augmentations you add to them.[Tool calling](https://docs.langchain.com/oss/python/langchain/tools),[structured outputs](https://docs.langchain.com/oss/python/langchain/structured-output), and[short term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)are a few options for tailoring LLMs to your needs.![LLM augmentations](https://mintcdn.com/langchain-5e9cc07a/-_xGPoyjhyiDWTPJ/oss/images/augmented_llm.png?fit=max&amp;auto=format&amp;n=-_xGPoyjhyiDWTPJ&amp;q=85&amp;s=7ea9656f46649b3ebac19e8309ae9006)
Copy
```
`# Schema for structured outputfrompydanticimportBaseModel, FieldclassSearchQuery(BaseModel):search\_query:str=Field(None,description="Query that is optimized web search.")justification:str=Field(None,description="Why this query is relevant to the user's request.")# Augment the LLM with schema for structured outputstructured\_llm=llm.with\_structured\_output(SearchQuery)# Invoke the augmented LLMoutput=structured\_llm.invoke("How does Calcium CT score relate to high cholesterol?")# Define a tooldefmultiply(a:int,b:int) -&gt;int:returna\*b# Augment the LLM with toolsllm\_with\_tools=llm.bind\_tools([multiply])# Invoke the LLM with input that triggers the tool callmsg=llm\_with\_tools.invoke("What is 2 times 3?")# Get the tool callmsg.tool\_calls`
```
## [​
](#prompt-chaining)
Prompt chaining
Prompt chaining is when each LLM call processes the output of the previous call. It’s often used for performing well-defined tasks that can be broken down into smaller, verifiable steps. Some examples include:
* Translating documents into different languages
* Verifying generated content for consistency![Prompt chaining](https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/prompt_chain.png?fit=max&amp;auto=format&amp;n=dL5Sn6Cmy9pwtY0V&amp;q=85&amp;s=762dec147c31b8dc6ebb0857e236fc1f)
Graph API
Functional API
Copy
```
`fromtyping\_extensionsimportTypedDictfromlanggraph.graphimportStateGraph,START,ENDfromIPython.displayimportImage, display# Graph stateclassState(TypedDict):topic:strjoke:strimproved\_joke:strfinal\_joke:str# Nodesdefgenerate\_joke(state: State):"""First LLM call to generate initial joke"""msg=llm.invoke(f"Write a short joke about{state['topic']}")return{"joke": msg.content}defcheck\_punchline(state: State):"""Gate function to check if the joke has a punchline"""# Simple check - does the joke contain "?" or "!"if"?"instate["joke"]or"!"instate["joke"]:return"Pass"return"Fail"defimprove\_joke(state: State):"""Second LLM call to improve the joke"""msg=llm.invoke(f"Make this joke funnier by adding wordplay:{state['joke']}")return{"improved\_joke": msg.content}defpolish\_joke(state: State):"""Third LLM call for final polish"""msg=llm.invoke(f"Add a surprising twist to this joke:{state['improved\_joke']}")return{"final\_joke": msg.content}# Build workflowworkflow=StateGraph(State)# Add nodesworkflow.add\_node("generate\_joke", generate\_joke)workflow.add\_node("improve\_joke", improve\_joke)workflow.add\_node("polish\_joke", polish\_joke)# Add edges to connect nodesworkflow.add\_edge(START,"generate\_joke")workflow.add\_conditional\_edges("generate\_joke", check\_punchline, {"Fail":"improve\_joke","Pass":END})workflow.add\_edge("improve\_joke","polish\_joke")workflow.add\_edge("polish\_joke",END)# Compilechain=workflow.compile()# Show workflowdisplay(Image(chain.get\_graph().draw\_mermaid\_png()))# Invokestate=chain.invoke({"topic":"cats"})print("Initial joke:")print(state["joke"])print("\\n--- --- ---\\n")if"improved\_joke"instate:print("Improved joke:")print(state["improved\_joke"])print("\\n--- --- ---\\n")print("Final joke:")print(state["final\_joke"])else:print("Final joke:")print(state["joke"])`
```
## [​
](#parallelization)
Parallelization
With parallelization, LLMs work simultaneously on a task. This is either done by running multiple independent subtasks at the same time, or running the same task multiple times to check for different outputs. Parallelization is commonly used to:
* Split up subtasks and run them in parallel, which increases speed
* Run tasks multiple times to check for different outputs, which increases confidenceSome examples include:
* Running one subtask that processes a document for keywords, and a second subtask to check for formatting errors
* Running a task multiple times that scores a document for accuracy based on different criteria, like the number of citations, the number of sources used, and the quality of the sources![parallelization.png](https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/parallelization.png?fit=max&amp;auto=format&amp;n=dL5Sn6Cmy9pwtY0V&amp;q=85&amp;s=8afe3c427d8cede6fed1e4b2a5107b71)
Graph API
Functional API
Copy
```
`# Graph stateclassState(TypedDict):topic:strjoke:strstory:strpoem:strcombined\_output:str# Nodesdefcall\_llm\_1(state: State):"""First LLM call to generate initial joke"""msg=llm.invoke(f"Write a joke about{state['topic']}")return{"joke": msg.content}defcall\_llm\_2(state: State):"""Second LLM call to generate story"""msg=llm.invoke(f"Write a story about{state['topic']}")return{"story": msg.content}defcall\_llm\_3(state: State):"""Third LLM call to generate poem"""msg=llm.invoke(f"Write a poem about{state['topic']}")return{"poem": msg.content}defaggregator(state: State):"""Combine the joke and story into a single output"""combined=f"Here's a story, joke, and poem about{state['topic']}!\\n\\n"combined+=f"STORY:\\n{state['story']}\\n\\n"combined+=f"JOKE:\\n{state['joke']}\\n\\n"combined+=f"POEM:\\n{state['poem']}"return{"combined\_output": combined}# Build workflowparallel\_builder=StateGraph(State)# Add nodesparallel\_builder.add\_node("call\_llm\_1", call\_llm\_1)parallel\_builder.add\_node("call\_llm\_2", call\_llm\_2)parallel\_builder.add\_node("call\_llm\_3", call\_llm\_3)parallel\_builder.add\_node("aggregator", aggregator)# Add edges to connect nodesparallel\_builder.add\_edge(START,"call\_llm\_1")parallel\_builder.add\_edge(START,"call\_llm\_2")parallel\_builder.add\_edge(START,"call\_llm\_3")parallel\_builder.add\_edge("call\_llm\_1","aggregator")parallel\_builder.add\_edge("call\_llm\_2","aggregator")parallel\_builder.add\_edge("call\_llm\_3","aggregator")parallel\_builder.add\_edge("aggregator",END)parallel\_workflow=parallel\_builder.compile()# Show workflowdisplay(Image(parallel\_workflow.get\_graph().draw\_mermaid\_png()))# Invokestate=parallel\_workflow.invoke({"topic":"cats"})print(state["combined\_output"])`
```
## [​
](#routing)
Routing
Routing workflows process inputs and then directs them to context-specific tasks. This allows you to define specialized flows for complex tasks. For example, a workflow built to answer product related questions might process the type of question first, and then route the request to specific processes for pricing, refunds, returns, etc.![routing.png](https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/routing.png?fit=max&amp;auto=format&amp;n=dL5Sn6Cmy9pwtY0V&amp;q=85&amp;s=272e0e9b681b89cd7d35d5c812c50ee6)
Graph API
Functional API
Copy
```
`fromtyping\_extensionsimportLiteralfromlangchain.messagesimportHumanMessage, SystemMessage# Schema for structured output to use as routing logicclassRoute(BaseModel):step: Literal["poem","story","joke"]=Field(None,description="The next step in the routing process")# Augment the LLM with schema for structured outputrouter=llm.with\_structured\_output(Route)# StateclassState(TypedDict):input:strdecision:stroutput:str# Nodesdefllm\_call\_1(state: State):"""Write a story"""result=llm.invoke(state["input"])return{"output": result.content}defllm\_call\_2(state: State):"""Write a joke"""result=llm.invoke(state["input"])return{"output": result.content}defllm\_call\_3(state: State):"""Write a poem"""result=llm.invoke(state["input"])return{"output": result.content}defllm\_call\_router(state: State):"""Route the input to the appropriate node"""# Run the augmented LLM with structured output to serve as routing logicdecision=router.invoke([SystemMessage(content="Route the input to story, joke, or poem based on the user's request."),HumanMessage(content=state["input"]),])return{"decision": decision.step}# Conditional edge function to route to the appropriate nodedefroute\_decision(state: State):# Return the node name you want to visit nextifstate["decision"]=="story":return"llm\_call\_1"elifstate["decision"]=="joke":return"llm\_call\_2"elifstate["decision"]=="poem":return"llm\_call\_3"# Build workflowrouter\_builder=StateGraph(State)# Add nodesrouter\_builder.add\_node("llm\_call\_1", llm\_call\_1)router\_builder.add\_node("llm\_call\_2", llm\_call\_2)router\_builder.add\_node("llm\_call\_3", llm\_call\_3)router\_builder.add\_node("llm\_call\_router", llm\_call\_router)# Add edges to connect nodesrouter\_builder.add\_edge(START,"llm\_call\_router")router\_builder.add\_conditional\_edges("llm\_call\_router",route\_decision,{# Name returned by route\_decision : Name of next node to visit"llm\_call\_1":"llm\_call\_1","llm\_call\_2":"llm\_call\_2","llm\_call\_3":"llm\_call\_3",},)router\_builder.add\_edge("llm\_call\_1",END)router\_builder.add\_edge("llm\_call\_2",END)router\_builder.add\_edge("llm\_call\_3",END)# Compile workflowrouter\_workflow=router\_builder.compile()# Show the workflowdisplay(Image(router\_workflow.get\_graph().draw\_mermaid\_png()))# Invokestate=router\_workflow.invoke({"input":"Write me a joke about cats"})print(state["output"])`
```
## [​
](#orchestrator-worker)
Orchestrator-worker
In an orchestrator-worker configuration, the orchestrator:
* Breaks down tasks into subtasks
* Delegates subtasks to workers
* Synthesizes worker outputs into a final result![worker.png](https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/worker.png?fit=max&amp;auto=format&amp;n=ybiAaBfoBvFquMDz&amp;q=85&amp;s=2e423c67cd4f12e049cea9c169ff0676)Orchestrator-worker workflows provide more flexibility and are often used when subtasks cannot be predefined the way they can with[parallelization](#parallelization). This is common with workflows that write code or need to update content across multiple files. For example, a workflow that needs to update installation instructions for multiple Python libraries across an unknown number of documents might use this pattern.
Graph API
Functional API
Copy
```
`fromtypingimportAnnotated, Listimportoperator# Schema for structured output to use in planningclassSection(BaseModel):name:str=Field(description="Name for this section of the report.",)description:str=Field(description="Brief overview of the main topics and concepts to be covered in this section.",)classSections(BaseModel):sections: List[Section]=Field(description="Sections of the report.",)# Augment the LLM with schema for structured outputplanner=llm.with\_structured\_output(Sections)`
```
### [​
](#creating-workers-in-langgraph)
Creating workers in LangGraph
Orchestrator-worker workflows are common and LangGraph has built-in support for them. The`Send`API lets you dynamically create worker nodes and send them specific inputs. Each worker has its own state, and all worker outputs are written to a shared state key that is accessible to the orchestrator graph. This gives the orchestrator access to all worker output and allows it to synthesize them into a final output. The example below iterates over a list of sections and uses the`Send`API to send a section to each worker.
Copy
```
`fromlanggraph.typesimportSend# Graph stateclassState(TypedDict):topic:str# Report topicsections: list[Section]# List of report sectionscompleted\_sections: Annotated[list, operator.add]# All workers write to this key in parallelfinal\_report:str# Final report# Worker stateclassWorkerState(TypedDict):section: Sectioncompleted\_sections: Annotated[list, operator.add]# Nodesdeforchestrator(state: State):"""Orchestrator that generates a plan for the report"""# Generate queriesreport\_sections=planner.invoke([SystemMessage(content="Generate a plan for the report."),HumanMessage(content=f"Here is the report topic:{state['topic']}"),])return{"sections": report\_sections.sections}defllm\_call(state: WorkerState):"""Worker writes a section of the report"""# Generate sectionsection=llm.invoke([SystemMessage(content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."),HumanMessage(content=f"Here is the section name:{state['section'].name}and description:{state['section'].description}"),])# Write the updated section to completed sectionsreturn{"completed\_sections": [section.content]}defsynthesizer(state: State):"""Synthesize full report from sections"""# List of completed sectionscompleted\_sections=state["completed\_sections"]# Format completed section to str to use as context for final sectionscompleted\_report\_sections="\\n\\n---\\n\\n".join(completed\_sections)return{"final\_report": completed\_report\_sections}# Conditional edge function to create llm\_call workers that each write a section of the reportdefassign\_workers(state: State):"""Assign a worker to each section in the plan"""# Kick off section writing in parallel via Send() APIreturn[Send("llm\_call", {"section": s})forsinstate["sections"]]# Build workfloworchestrator\_worker\_builder=StateGraph(State)# Add the nodesorchestrator\_worker\_builder.add\_node("orchestrator", orchestrator)orchestrator\_worker\_builder.add\_node("llm\_call", llm\_call)orchestrator\_worker\_builder.add\_node("synthesizer", synthesizer)# Add edges to connect nodesorchestrator\_worker\_builder.add\_edge(START,"orchestrator")orchestrator\_worker\_builder.add\_conditional\_edges("orchestrator", assign\_workers, ["llm\_call"])orchestrator\_worker\_builder.add\_edge("llm\_call","synthesizer")orchestrator\_worker\_builder.add\_edge("synthesizer",END)# Compile the workfloworchestrator\_worker=orchestrator\_worker\_builder.compile()# Show the workflowdisplay(Image(orchestrator\_worker.get\_graph().draw\_mermaid\_png()))# Invokestate=orchestrator\_worker.invoke({"topic":"Create a report on LLM scaling laws"})fromIPython.displayimportMarkdownMarkdown(state["final\_report"])`
```
## [​
](#evaluator-optimizer)
Evaluator-optimizer
In evaluator-optimizer workflows, one LLM call creates a response and the other evaluates that response. If the evaluator or a[human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/interrupts)determines the response needs refinement, feedback is provided and the response is recreated. This loop continues until an acceptable response is generated.Evaluator-optimizer workflows are commonly used when there’s particular success criteria for a task, but iteration is required to meet that criteria. For example, there’s not always a perfect match when translating text between two languages. It might take a few iterations to generate a translation with the same meaning across the two languages.![evaluator_optimizer.png](https://mintcdn.com/langchain-5e9cc07a/-_xGPoyjhyiDWTPJ/oss/images/evaluator_optimizer.png?fit=max&amp;auto=format&amp;n=-_xGPoyjhyiDWTPJ&amp;q=85&amp;s=9bd0474f42b6040b14ed6968a9ab4e3c)
Graph API
Functional API
Copy
```
`# Graph stateclassState(TypedDict):joke:strtopic:strfeedback:strfunny\_or\_not:str# Schema for structured output to use in evaluationclassFeedback(BaseModel):grade: Literal["funny","not funny"]=Field(description="Decide if the joke is funny or not.",)feedback:str=Field(description="If the joke is not funny, provide feedback on how to improve it.",)# Augment the LLM with schema for structured outputevaluator=llm.with\_structured\_output(Feedback)# Nodesdefllm\_call\_generator(state: State):"""LLM generates a joke"""ifstate.get("feedback"):msg=llm.invoke(f"Write a joke about{state['topic']}but take into account the feedback:{state['feedback']}")else:msg=llm.invoke(f"Write a joke about{state['topic']}")return{"joke": msg.content}defllm\_call\_evaluator(state: State):"""LLM evaluates the joke"""grade=evaluator.invoke(f"Grade the joke{state['joke']}")return{"funny\_or\_not": grade.grade,"feedback": grade.feedback}# Conditional edge function to route back to joke generator or end based upon feedback from the evaluatordefroute\_joke(state: State):"""Route back to joke generator or end based upon feedback from the evaluator"""ifstate["funny\_or\_not"]=="funny":return"Accepted"elifstate["funny\_or\_not"]=="not funny":return"Rejected + Feedback"# Build workflowoptimizer\_builder=StateGraph(State)# Add the nodesoptimizer\_builder.add\_node("llm\_call\_generator", llm\_call\_generator)optimizer\_builder.add\_node("llm\_call\_evaluator", llm\_call\_evaluator)# Add edges to connect nodesoptimizer\_builder.add\_edge(START,"llm\_call\_generator")optimizer\_builder.add\_edge("llm\_call\_generator","llm\_call\_evaluator")optimizer\_builder.add\_conditional\_edges("llm\_call\_evaluator",route\_joke,{# Name returned by route\_joke : Name of next node to visit"Accepted":END,"Rejected + Feedback":"llm\_call\_generator",},)# Compile the workflowoptimizer\_workflow=optimizer\_builder.compile()# Show the workflowdisplay(Image(optimizer\_workflow.get\_graph().draw\_mermaid\_png()))# Invokestate=optimizer\_workflow.invoke({"topic":"Cats"})print(state["joke"])`
```
## [​
](#agents)
Agents
Agents are typically implemented as an LLM performing actions using[tools](https://docs.langchain.com/oss/python/langchain/tools). They operate in continuous feedback loops, and are used in situations where problems and solutions are unpredictable. Agents have more autonomy than workflows, and can make decisions about the tools they use and how to solve problems. You can still define the available toolset and guidelines for how agents behave.![agent.png](https://mintcdn.com/langchain-5e9cc07a/-_xGPoyjhyiDWTPJ/oss/images/agent.png?fit=max&amp;auto=format&amp;n=-_xGPoyjhyiDWTPJ&amp;q=85&amp;s=bd8da41dbf8b5e6fc9ea6bb10cb63e38)
To get started with agents, see the[quickstart](https://docs.langchain.com/oss/python/langchain/quickstart)or read more about[how they work](https://docs.langchain.com/oss/python/langchain/agents)in LangChain.
Using tools
Copy
```
`fromlangchain.toolsimporttool# Define tools@tooldefmultiply(a:int,b:int) -&gt;int:"""Multiply `a` and `b`.Args:a: First intb: Second int"""returna\*b@tooldefadd(a:int,b:int) -&gt;int:"""Adds `a` and `b`.Args:a: First intb: Second int"""returna+b@tooldefdivide(a:int,b:int) -&gt;float:"""Divide `a` and `b`.Args:a: First intb: Second int"""returna/b# Augment the LLM with toolstools=[add, multiply, divide]tools\_by\_name={tool.name: toolfortoolintools}llm\_with\_tools=llm.bind\_tools(tools)`
```
Graph API
Functional API
Copy
```
`fromlanggraph.graphimportMessagesStatefromlangchain.messagesimportSystemMessage, HumanMessage, ToolMessage# Nodesdefllm\_call(state: MessagesState):"""LLM decides whether to call a tool or not"""return{"messages": [llm\_with\_tools.invoke([SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")]+state["messages"])]}deftool\_node(state:dict):"""Performs the tool call"""result=[]fortool\_callinstate["messages"][-1].tool\_calls:tool=tools\_by\_name[tool\_call["name"]]observation=tool.invoke(tool\_call["args"])result.append(ToolMessage(content=observation,tool\_call\_id=tool\_call["id"]))return{"messages": result}# Conditional edge function to route to the tool node or end based upon whether the LLM made a tool calldefshould\_continue(state: MessagesState) -&gt; Literal["tool\_node",END]:"""Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""messages=state["messages"]last\_message=messages[-1]# If the LLM makes a tool call, then perform an actioniflast\_message.tool\_calls:return"tool\_node"# Otherwise, we stop (reply to the user)returnEND# Build workflowagent\_builder=StateGraph(MessagesState)# Add nodesagent\_builder.add\_node("llm\_call", llm\_call)agent\_builder.add\_node("tool\_node", tool\_node)# Add edges to connect nodesagent\_builder.add\_edge(START,"llm\_call")agent\_builder.add\_conditional\_edges("llm\_call",should\_continue,["tool\_node",END])agent\_builder.add\_edge("tool\_node","llm\_call")# Compile the agentagent=agent\_builder.compile()# Show the agentdisplay(Image(agent.get\_graph(xray=True).draw\_mermaid\_png()))# Invokemessages=[HumanMessage(content="Add 3 and 4.")]messages=agent.invoke({"messages": messages})forminmessages["messages"]:m.pretty\_print()`
```
[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/workflows-agents.mdx)or[file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
[Connect these docs](https://docs.langchain.com/use-these-docs)to Claude, VSCode, and more via MCP for real-time answers.
Was this page helpful?
YesNo
[
Thinking in LangGraph
Previous
](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)[
Persistence
Next
](https://docs.langchain.com/oss/python/langgraph/persistence)
⌘I
