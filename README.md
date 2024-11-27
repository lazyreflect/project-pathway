# Project Pathfinder

Pathfinder is an enterprise-focused automation system designed to streamline complex web-based workflows that require secure authentication across multiple platforms.

Goals:

- Automate multi-step verification processes across different portals and databases
- Handle secure login and authentication across multiple business platforms
- Extract and compile information from various authenticated sources
- Navigate complex form submissions and data entry tasks
- Perform eligibility checks and status verifications across multiple systems
- Manage and track claims or case status across different provider portals
- Automate routine administrative tasks that require secure access.

Example use case:

Architecture:

Pathfinder is composed of two main components:

1. The enterprise workflow orchestrator (Pathfinder), built using LangGraph. This component is responsible for managing the overall workflow, including task scheduling, error handling, and integration with external systems. This repository contains the code for this component. This component will use API endpoints to interact with the web automation agent (Agent-D).

2. The web automation agent (Agent-D), based on a fork of [Agent-E](https://github.com/EmergenceAI/Agent-E) that adds secure credential management features for automated login handling. Like its parent project, Agent-D is an agent-based system that automates actions on the user's computer, with a current focus on browser automation using the [AutoGen agent framework](https://github.com/microsoft/autogen). A seperate repository contains the code for this component.

Agent-D extends the capabilities of Agent-E by adding enterprise-grade credential management features:

- Secure handling of multiple login credentials
- Automated authentication across different platforms
- Enhanced security features for business compliance
- Support for complex multi-step verification workflows
- Credential isolation and secure environment variable storage

What is Agent-E?

Agent-E is an agent based system that aims to automate actions on the user's computer. At the moment it focuses on automation within the browser. The system is based on on [AutoGen agent framework](https://github.com/microsoft/autogen).

This provides a natural language way to interacting with a web browser:
- Fill out forms (web forms not PDF yet) using information about you or from another site
- Search and sort products on e-commerce sites like Amazon based on various criteria, such as bestsellers or price.
- Locate specific content and details on websites, from sports scores on ESPN to contact information on university pages.
- Navigate to and interact with web-based media, including playing YouTube videos and managing playback settings like full-screen and mute.
- Perform comprehensive web searches to gather information on a wide array of topics, from historical sites to top local restaurants.
- Manage and automate tasks on project management platforms (like JIRA) by filtering issues, easing the workflow for users.
- Provide personal shopping assistance, suggesting products based on the user's needs, such as storage options for game cards.

What is new in Agent-D?

Agent-D adds secure credential management features for automated login handling.


#### Using Secret Credentials

Once credentials are set, the Agent-D can automatically handle login forms using a special skill. The skill:

- Securely retrieves credentials from environment variables
- Enters username and password into specified form fields
- Handles login button submission
- Waits for navigation completion

#### Security Considerations

- Credentials are stored only in environment variables, not in files
- API authentication uses constant-time comparison to prevent timing attacks
- The client secret should be a secure random string
- Credentials are never logged or exposed in error messages

