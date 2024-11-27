# Getting Started with Project Pathway: Implementing a Simple LangGraph Agent Communicating with Agent-D

Welcome to the Project Pathway development guide! This step-by-step tutorial will help you set up the codebase and implement a simple **LangGraph** agent that communicates successfully with the **Agent-D** API. Our initial task will be a basic Google search, fulfilling **Task 1** from `TASKS.md`.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Step 1: Set Up the Development Environment](#step-1-set-up-the-development-environment)
4. [Step 2: Install LangGraph and Dependencies](#step-2-install-langgraph-and-dependencies)
5. [Step 3: Review the Agent-D API](#step-3-review-the-agent-d-api)
6. [Step 4: Implement the LangGraph Agent](#step-4-implement-the-langgraph-agent)
7. [Step 5: Integrate the Agent with Agent-D API](#step-5-integrate-the-agent-with-agent-d-api)
8. [Step 6: Test the Agent](#step-6-test-the-agent)
9. [Conclusion](#conclusion)
10. [Appendix](#appendix)

---

## Introduction

**Project Pathway** aims to automate complex workflows by orchestrating agents through **LangGraph** and integrating with **Agent-D** for web automation tasks. This guide focuses on setting up a simple agent that communicates with Agent-D to perform a basic Google search.

---

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed on your system.
- Familiarity with **Python** programming.
- Basic understanding of **LangChain** and **LangGraph** concepts.
- Access to the **Agent-D** API.

---

## Step 1: Set Up the Development Environment

### 1.1. Clone the Repository

First, clone the Project Pathway repository from your version control system:

```bash
git clone https://github.com/your-organization/project-pathway.git
cd project-pathway
```

> Replace `https://github.com/your-organization/project-pathway.git` with the actual repository URL.

### 1.2. Create a Python Virtual Environment

Create and activate a virtual environment to manage project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 1.3. Install Required Python Packages

We will install the necessary packages, including **LangGraph**, **LangChain**, and request libraries:

```bash
pip install -U pip
pip install langgraph langchain requests python-dotenv
```

---

## Step 2: Install LangGraph and Dependencies

### 2.1. Install LangGraph

If LangGraph is not already installed, you can install it using `pip`:

```bash
pip install langgraph
```

> **Note**: LangGraph requires Python 3.8 or higher.

### 2.2. Verify the Installation

Ensure that LangGraph is installed correctly by running:

```bash
python -c "import langgraph; print('LangGraph version:', langgraph.__version__)"
```

---

## Step 3: Review the Agent-D API

Before integrating with Agent-D, familiarize yourself with its API endpoints, especially `/execute_task` and `/api/set_credentials`.

### 3.1. Agent-D API Overview

- **Set Credentials**: Allows you to securely store credentials required for automation tasks.
- **Execute Task**: Sends commands for Agent-D to execute web automation tasks.

### 3.2. API Endpoint Details

Refer to `API_GUIDE.md` for detailed information on how to interact with these endpoints.

---

## Step 4: Implement the LangGraph Agent

We will create a simple **LangGraph** agent that performs a basic Google search by communicating with Agent-D.

### 4.1. Create the Project Structure

Organize your codebase as follows:

```
/
├── agents/
│   └── basic_search_agent.py
├── workflows/
│   └── basic_search_workflow.py
├── credentials/
│   └── credential_manager.py
├── config/
│   └── __init__.py
├── .env.example
└── requirements.txt
```

### 4.2. Implement the Credential Manager

Although we may not need credentials for this basic task, it's good practice to set up the credential manager.

```python:credentials/credential_manager.py
import os
from typing import Dict

class CredentialManager:
    """Handles retrieval of credentials from environment variables."""
    
    def get_credentials(self, portal_name: str) -> Dict[str, str]:
        """Get credentials for a specific portal from environment variables."""
        username = os.getenv(f'{portal_name.upper()}_USERNAME')
        password = os.getenv(f'{portal_name.upper()}_PASSWORD')

        if not username or not password:
            raise ValueError(f"Missing credentials for {portal_name}")

        return {
            'username': username,
            'password': password
        }
```

> **File**: `credentials/credential_manager.py`  
> **Purpose**: Manages credentials securely using environment variables.

### 4.3. Define the Agent

Create an agent that will interact with Agent-D to perform the Google search.

```python:agents/basic_search_agent.py
from pathway.integration.agent_d_client import AgentDClient

class BasicSearchAgent:
    """Agent that performs a basic Google search via Agent-D."""

    def __init__(self, agent_d_client: AgentDClient):
        self.agent_d_client = agent_d_client

    def execute(self, state):
        """Execute the agent's task."""
        command = "Navigate to google.com and search for the latest weather in Kansas City."
        response = self.agent_d_client.execute_command(command)
        state['search_results'] = response
        return state
```

> **File**: `agents/basic_search_agent.py`  
> **Class**: `BasicSearchAgent`  
> **Purpose**: Defines an agent that sends a command to Agent-D to perform a Google search.

### 4.4. Implement the Agent-D Client

Create a client to handle communication with the Agent-D API.

```python:pathway/integration/agent_d_client.py
import requests
import os

class AgentDClient:
    """Client to interact with the Agent-D API."""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv('AGENT_D_BASE_URL', 'http://localhost:8000')
        self.session = requests.Session()

    def execute_command(self, command: str):
        """Send a command to Agent-D for execution."""
        url = f"{self.base_url}/execute_task"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "command": command
        }
        try:
            with self.session.post(url, headers=headers, json=payload, stream=True) as response:
                response.raise_for_status()
                result = ''
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        result += decoded_line + '\n'
                return result
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to execute command: {e}")
```

> **File**: `pathway/integration/agent_d_client.py`  
> **Class**: `AgentDClient`  
> **Purpose**: Handles API requests to Agent-D, including sending commands and processing responses.

---

## Step 5: Integrate the Agent with Agent-D API

Now, we'll create a **LangGraph** workflow that uses the `BasicSearchAgent`.

### 5.1. Define the Workflow

Create a workflow using **StateGraph**.

```python:workflows/basic_search_workflow.py
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from agents.basic_search_agent import BasicSearchAgent
from pathway.integration.agent_d_client import AgentDClient

class SearchState(TypedDict):
    search_results: str

def create_search_workflow():
    """Create and return a compiled search workflow."""
    # Initialize the workflow
    workflow = StateGraph(SearchState)

    # Define the nodes
    def start(state: SearchState) -> SearchState:
        """Initialize the workflow state."""
        return state

    def perform_search(state: SearchState) -> SearchState:
        """Execute the search using BasicSearchAgent."""
        agent_d_client = AgentDClient()
        agent = BasicSearchAgent(agent_d_client)
        return agent.execute(state)

    def end_workflow(state: SearchState) -> SearchState:
        """Process final results."""
        print("Search Results:")
        print(state.get('search_results', 'No results found.'))
        return state

    # Add nodes to the workflow
    workflow.add_node("start", start)
    workflow.add_node("search", perform_search)
    workflow.add_node("end", end_workflow)

    # Define the edges
    workflow.add_edge(START, "start")  # Connect START to first node
    workflow.add_edge("start", "search")
    workflow.add_edge("search", "end")
    workflow.add_edge("end", END)  # Connect last node to END

    # Compile the workflow
    return workflow.compile()

# Create the workflow
app = create_search_workflow()
```

> **File**: `workflows/basic_search_workflow.py`  
> **Purpose**: Defines the workflow that uses `BasicSearchAgent` to perform the search task.

### 5.2. Update Environment Variables

Create a `.env` file in the root directory with the following content:

```
AGENT_D_BASE_URL=http://localhost:8000
```

> **Note**: Ensure the Agent-D server is running at the specified `AGENT_D_BASE_URL`.

---

## Step 6: Test the Agent

### 6.1. Ensure Agent-D is Running

Make sure the Agent-D server is up and accessible. Follow any instructions provided in its documentation to start the server.

### 6.2. Run the Workflow

Execute the `basic_search_workflow.py` script:

```bash
python workflows/basic_search_workflow.py
```

### 6.3. Verify the Output

You should see output similar to:

```
Search Results:
[Agent-D response with the search results]
```

If there are any errors, check the following:

- Agent-D server is running and accessible.
- The `AGENT_D_BASE_URL` is correct.
- There are no typos in the code.

---

## Conclusion

Congratulations! You've successfully set up a simple LangGraph agent that communicates with Agent-D to perform a basic Google search. This foundational work prepares you for further development tasks, such as implementing more complex workflows and integrating additional agents.

---

## Appendix

### A. Relevant Files and Their Purposes

- **`credentials/credential_manager.py`**: Manages credentials securely.
- **`pathway/integration/agent_d_client.py`**: Handles communication with Agent-D API.
- **`agents/basic_search_agent.py`**: Defines the agent that performs the search task.
- **`workflows/basic_search_workflow.py`**: Sets up the LangGraph workflow.

### B. Additional Resources

- **LangGraph Documentation**: [LangGraph Official Docs](https://langchain-ai.github.io/langgraph/)
- **Agent-D API Guide**: Refer to `API_GUIDE.md` in the project root.
- **Project Architecture**: Refer to `ARCHITECTURE.md` for an in-depth understanding of the system.

### C. Environment Variables Cheat Sheet

Create a `.env.example` file to document required environment variables:

```
# .env.example

# Agent-D Configuration
AGENT_D_BASE_URL=http://localhost:8000

# Credentials (if needed in future tasks)
# GOOGLE_USERNAME=your_username
# GOOGLE_PASSWORD=your_password
```

Ensure your `.env` file is **not** checked into version control.

---

## Next Steps

Now that you've completed the initial task:

- **Explore LangGraph Features**: Dive deeper into conditional logic, state persistence, and multi-agent workflows.
- **Implement Additional Agents**: Based on `TASKS.md`, implement more complex agents and workflows.
- **Enhance Error Handling**: Improve robustness by adding exception handling and retries.
- **Secure Credential Management**: For tasks requiring authentication, ensure credentials are handled securely.

---

By following this guide, you've set a solid foundation to build upon the Project Pathway codebase and tackle more advanced automation tasks using LangGraph and Agent-D.