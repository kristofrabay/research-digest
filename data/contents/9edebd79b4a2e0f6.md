# MCP

**URL:** https://developers.openai.com/apps-sdk/concepts/mcp-server/
**Published:** 2025-06-18T00:00:00.000Z

---

## Summary

The provided webpage describes the **Model Context Protocol (MCP)**, which is an open specification for connecting large language model clients (like ChatGPT) to external tools and resources.

Here is a summary of the key concepts mentioned in the text that relate to your query:

*   **MCP Servers:** An MCP server exposes **tools** that a model can call during a conversation.
*   **Tool Use:** The protocol supports listing tools (with JSON Schema contracts), calling tools with arguments, and returning structured content/results.
*   **Structured Outputs:** Tool execution returns structured content that the model can parse.
*   **Agent Frameworks/SDKs:** The text specifically mentions the **Apps SDK** (which uses MCP as its backbone) and references official SDKs for **Python** and **TypeScript**.
*   **Agent Orchestration/Memory:** While the text doesn't explicitly use the terms "agent memory" or "agent orchestration," it describes how MCP enables **Conversation awareness** (structured content and component state flow through the conversation) and **Discovery integration** (the model reasons about the app like built-in tools), which are core components of agentic systems.
*   **Function Calling:** This is directly supported by the "Call tools" capability of the protocol.

**Missing Information:** The text **does not** mention: `agent_infrastructure`, `agent memory`, `agentic memory`, `LangChain`, `LlamaIndex`, `OpenAI Agents SDK`, `Anthropic Agents SDK`, `Google SDK`, or `inline html` (though it mentions returning components/embedded resources).

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
* [Home](https://developers.openai.com/codex)
* [Quickstart](https://developers.openai.com/codex/quickstart)
* [Pricing](https://developers.openai.com/codex/pricing)
* Concepts
* [Tasks &amp; Prompts](https://developers.openai.com/codex/concepts)
* [Models](https://developers.openai.com/codex/models)
* [Sandboxing](https://developers.openai.com/codex/sandbox)
* [Build AI-Native Teams](https://developers.openai.com/codex/guides/build-ai-native-engineering-team)
### Using Codex
* IDE Extension
* [Overview](https://developers.openai.com/codex/ide)
* [Features](https://developers.openai.com/codex/ide/features)
* CLI
* [Overview](https://developers.openai.com/codex/cli)
* [Features](https://developers.openai.com/codex/cli/features)
* [Command Line Options](https://developers.openai.com/codex/cli/reference)
* [Slash commands](https://developers.openai.com/codex/guides/slash-commands)
* Web
* [Overview](https://developers.openai.com/codex/cloud)
* [Environments](https://developers.openai.com/codex/cloud/environments)
* [Internet Access](https://developers.openai.com/codex/cloud/internet-access)
* Integrations
* [GitHub](https://developers.openai.com/codex/integrations/github)
* [Slack](https://developers.openai.com/codex/integrations/slack)
* [Linear](https://developers.openai.com/codex/integrations/linear)
### Configuration
* [Config File](https://developers.openai.com/codex/local-config)
* [Instructions](https://developers.openai.com/codex/guides/agents-md)
* [MCP](https://developers.openai.com/codex/mcp)
* Skills
* [Overview](https://developers.openai.com/codex/skills)
* [Create skills](https://developers.openai.com/codex/skills/create-skill)
### Deployment &amp; Admin
* [Administration](https://developers.openai.com/codex/enterprise)
* [Authentication](https://developers.openai.com/codex/guides/api-key)
* [Security](https://developers.openai.com/codex/security)
* [Windows](https://developers.openai.com/codex/windows)
### Automation
* [Codex SDK](https://developers.openai.com/codex/sdk)
* [MCP Server](https://developers.openai.com/codex/guides/agents-sdk)
* [GitHub Action](https://developers.openai.com/codex/github-action)
### Releases
* [Changelog](https://developers.openai.com/codex/changelog)
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
* [Updates for developers building with voice](https://developers.openai.com/blog/updates-audio-models)
* [What makes a great ChatGPT app](https://developers.openai.com/blog/what-makes-a-great-chatgpt-app)
* [Using Codex for education at Dagster Labs](https://developers.openai.com/blog/codex-for-documentation-dagster)
* [How Codex ran OpenAI DevDay 2025](https://developers.openai.com/blog/codex-at-devday)
* [Why we built the Responses API](https://developers.openai.com/blog/responses-api)
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
