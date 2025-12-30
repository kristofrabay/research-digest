# MCP

**URL:** https://developers.openai.com/apps-sdk/concepts/mcp-server/
**Published:** 2025-06-18T00:00:00.000Z

---

## Summary

The provided web page describes the **Model Context Protocol (MCP)**, which is an open specification for connecting large language model clients to external tools and resources.

**Key aspects of MCP mentioned on the page:**

*   **Purpose:** An MCP server exposes **tools** that a model can call during a conversation, returning results with specified parameters. It also allows returning metadata, such as inline HTML for rendering interfaces in the Apps SDK.
*   **Role with Apps SDK:** MCP is the backbone that keeps the server, model, and UI in sync, allowing ChatGPT to reason about your app similarly to built-in tools by standardizing wire format, authentication, and metadata.
*   **Protocol Building Blocks:**
    1.  **List tools:** The server advertises supported tools, including their JSON Schema input/output contracts.
    2.  **Call tools:** The model sends a `call_tool` request, the server executes the action, and returns structured content.
    3.  **Return components:** Tools can optionally point to an embedded resource representing the interface to render in the client.
*   **Benefits of using MCP:** Discovery integration, conversation awareness (state flows through the conversation), multiclient support (works across web and mobile), and extensible authentication.

**Regarding your specific query terms:**

The page focuses on **MCP servers**, **tool use**, **function calling** (implied by "Call tools" and structured content), and **structured outputs**. It also mentions **SDKs** (Official SDKs: Python SDK and TypeScript).

However, the page **does not mention or discuss** the following terms from your query: *deep research, agent memory, agentic memory, context compression, agent frameworks, LangChain, LlamaIndex, OpenAI Agents SDK, Anthropic Agents SDK, Google SDK, agent orchestration, agent evaluations, LLM reasoning trace evaluation, prompt engineering, context engineering, long context, supervised fine-tuning, or reinforcement learning.*

**Summary relative to the query:** The page explains what the **MCP server** is and how it facilitates **tool use** and **structured outputs** within the context of the Apps SDK, but it does not cover the majority of the advanced agent infrastructure concepts listed in your query.

---

## Full Content

MCP
[![OpenAI Developers](https://developers.openai.com/OpenAI_Developers.svg)](https://developers.openai.com/)
## Search the ChatGPT docs
Close
Clear
Primary navigation
ChatGPT
ResourcesCodexChatGPTBlog
Clear
* [Home](https://developers.openai.com/resources)
* [Changelog](https://developers.openai.com/changelog)
### Categories
* [Code](https://developers.openai.com/resources/code)
* [Cookbooks](https://developers.openai.com/resources/cookbooks)
* [Guides](https://developers.openai.com/resources/guides)
* [Videos](https://developers.openai.com/resources/videos)
### Topics
* [Agents](https://developers.openai.com/resources/agents)
* [Audio &amp; Voice](https://developers.openai.com/resources/audio)
* [Image generation](https://developers.openai.com/resources/imagegen)
* [Video generation](https://developers.openai.com/resources/videogen)
* [Tools](https://developers.openai.com/resources/tools)
* [Computer use](https://developers.openai.com/resources/cua)
* [Fine-tuning](https://developers.openai.com/resources/fine-tuning)
* [Scaling](https://developers.openai.com/resources/scaling)
### Getting Started
* [Overview](https://developers.openai.com/codex)
* [Quickstart](https://developers.openai.com/codex/quickstart)
* [Pricing](https://developers.openai.com/codex/pricing)
* Concepts
* [Prompting](https://developers.openai.com/codex/prompting)
* [Workflows](https://developers.openai.com/codex/workflows)
* [Models](https://developers.openai.com/codex/models)
* [AI-Native Teams](https://developers.openai.com/codex/guides/build-ai-native-engineering-team)
### Using Codex
* IDE Extension
* [Overview](https://developers.openai.com/codex/ide)
* [Features](https://developers.openai.com/codex/ide/features)
* [Settings](https://developers.openai.com/codex/ide/settings)
* [IDE Commands](https://developers.openai.com/codex/ide/commands)
* [Slash commands](https://developers.openai.com/codex/ide/slash-commands)
* CLI
* [Overview](https://developers.openai.com/codex/cli)
* [Features](https://developers.openai.com/codex/cli/features)
* [Command Line Options](https://developers.openai.com/codex/cli/reference)
* [Slash commands](https://developers.openai.com/codex/cli/slash-commands)
* Web
* [Overview](https://developers.openai.com/codex/cloud)
* [Environments](https://developers.openai.com/codex/cloud/environments)
* [Internet Access](https://developers.openai.com/codex/cloud/internet-access)
* Integrations
* [GitHub](https://developers.openai.com/codex/integrations/github)
* [Slack](https://developers.openai.com/codex/integrations/slack)
* [Linear](https://developers.openai.com/codex/integrations/linear)
### Configuration
* Config File
* [Basic Config](https://developers.openai.com/codex/config-basic)
* [Advanced Config](https://developers.openai.com/codex/config-advanced)
* [Config Reference](https://developers.openai.com/codex/config-reference)
* [Sample Config](https://developers.openai.com/codex/config-sample)
* [Execution Policy](https://developers.openai.com/codex/exec-policy)
* [AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
* [MCP](https://developers.openai.com/codex/mcp)
* Skills
* [Overview](https://developers.openai.com/codex/skills)
* [Create skills](https://developers.openai.com/codex/skills/create-skill)
### Administration
* [Authentication](https://developers.openai.com/codex/auth)
* [Security](https://developers.openai.com/codex/security)
* [Enterprise](https://developers.openai.com/codex/enterprise)
* [Windows](https://developers.openai.com/codex/windows)
### Automation
* [Non-interactive Mode](https://developers.openai.com/codex/noninteractive)
* [Codex SDK](https://developers.openai.com/codex/sdk)
* [MCP Server](https://developers.openai.com/codex/guides/agents-sdk)
* [GitHub Action](https://developers.openai.com/codex/github-action)
### Releases
* [Changelog](https://developers.openai.com/codex/changelog)
* [Feature Maturity](https://developers.openai.com/codex/feature-maturity)
* [Open Source](https://developers.openai.com/codex/open-source)
* [Home](https://developers.openai.com/apps-sdk)
* [Quickstart](https://developers.openai.com/apps-sdk/quickstart)
### Core Concepts
* [MCP Server](https://developers.openai.com/apps-sdk/concepts/mcp-server)
* [UX principles](https://developers.openai.com/apps-sdk/concepts/ux-principles)
* [UI guidelines](https://developers.openai.com/apps-sdk/concepts/ui-guidelines)
### Plan
* [Research use cases](https://developers.openai.com/apps-sdk/plan/use-case)
* [Define tools](https://developers.openai.com/apps-sdk/plan/tools)
* [Design components](https://developers.openai.com/apps-sdk/plan/components)
### Build
* [Set up your server](https://developers.openai.com/apps-sdk/build/mcp-server)
* [Build your ChatGPT UI](https://developers.openai.com/apps-sdk/build/chatgpt-ui)
* [Authenticate users](https://developers.openai.com/apps-sdk/build/auth)
* [Manage state](https://developers.openai.com/apps-sdk/build/state-management)
* [Monetize your app](https://developers.openai.com/apps-sdk/build/monetization)
* [Examples](https://developers.openai.com/apps-sdk/build/examples)
### Deploy
* [Deploy your app](https://developers.openai.com/apps-sdk/deploy)
* [Connect from ChatGPT](https://developers.openai.com/apps-sdk/deploy/connect-chatgpt)
* [Test your integration](https://developers.openai.com/apps-sdk/deploy/testing)
* [Submit your app](https://developers.openai.com/apps-sdk/deploy/submission)
### Guides
* [Optimize Metadata](https://developers.openai.com/apps-sdk/guides/optimize-metadata)
* [Security &amp; Privacy](https://developers.openai.com/apps-sdk/guides/security-privacy)
* [Troubleshooting](https://developers.openai.com/apps-sdk/deploy/troubleshooting)
### Resources
* [App submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)
* [Reference](https://developers.openai.com/apps-sdk/reference)
* [All posts](https://developers.openai.com/blog)
### Recent
* [OpenAI for Developers in 2025](https://developers.openai.com/blog/openai-for-developers-2025)
* [Updates for developers building with voice](https://developers.openai.com/blog/updates-audio-models)
* [What makes a great ChatGPT app](https://developers.openai.com/blog/what-makes-a-great-chatgpt-app)
* [Using Codex for education at Dagster Labs](https://developers.openai.com/blog/codex-for-documentation-dagster)
* [How Codex ran OpenAI DevDay 2025](https://developers.openai.com/blog/codex-at-devday)
Search⌘K
Copy PageMore page actions
Copy PageMore page actions
# MCP
Understand how the Model Context Protocol works with Apps SDK.
## What is MCP?
The[Model Context Protocol](https://modelcontextprotocol.io/)(MCP) is an open specification for connecting large language model clients to external tools and resources. An MCP server exposes**tools**that a model can call during a conversation, and return results given specified parameters.
Other resources (metadata) can be returned along with tool results, including the inline html that we can use in the Apps SDK to render an interface.
With Apps SDK, MCP is the backbone that keeps server, model, and UI in sync. By standardising the wire format, authentication, and metadata, it lets ChatGPT reason about your app the same way it reasons about built-in tools.
## Protocol building blocks
A minimal MCP server for Apps SDK implements three capabilities:
1. **List tools**– your server advertises the tools it supports, including their JSON Schema input and output contracts and optional annotations.
2. **Call tools**– when a model selects a tool to use, it sends a`call\_tool`request with the arguments corresponding to the user intent. Your server executes the action and returns structured content the model can parse.
3. **Return components**– in addition to structured content returned by the tool, each tool (in its metadata) can optionally point to an[embedded resource](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#embedded-resources)that represents the interface to render in the ChatGPT client.
The protocol is transport agnostic, you can host the server over Server-Sent Events or Streamable HTTP. Apps SDK supports both options, but we recommend Streamable HTTP.
## Why Apps SDK standardises on MCP
Working through MCP gives you several benefits out of the box:
* **Discovery integration**– the model consumes your tool metadata and surface descriptions the same way it does for first-party connectors, enabling natural-language discovery and launcher ranking. See[Discovery](https://developers.openai.com/apps-sdk/concepts/user-interaction)for details.
* **Conversation awareness**– structured content and component state flow through the conversation. The model can inspect the JSON result, refer to IDs in follow-up turns, or render the component again later.
* **Multiclient support**– MCP is self-describing, so your connector works across ChatGPT web and mobile without custom client code.
* **Extensible auth**– the specification includes protected resource metadata, OAuth 2.1 flows, and dynamic client registration so you can control access without inventing a proprietary handshake.## Next steps
If you’re new to MCP, we recommend starting with the following resources:
* [Model Context Protocol specification](https://modelcontextprotocol.io/specification)
* Official SDKs:[Python SDK (official; includes FastMCP module)](https://github.com/modelcontextprotocol/python-sdk)and[TypeScript](https://github.com/modelcontextprotocol/typescript-sdk)
* [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)for local debugging
Once you are comfortable with the MCP primitives, you can move on to the[Set up your server](https://developers.openai.com/apps-sdk/build/mcp-server)guide for implementation details.
