# Project Pathway Architecture Design

## Introduction

Project Pathway aims to automate complex dental administrative workflows that require secure authentication across multiple platforms. By leveraging **LangGraph** for orchestration, we will build a multi-agent system that coordinates specialized agents to handle tasks such as eligibility verification, claims processing, appointment scheduling, and data consolidation. The system will integrate securely with **Agent-D**, a web automation agent, to perform web-based interactions in compliance with healthcare regulations.

This document provides an updated architecture design for Project Pathway, focusing on practical implementation using LangGraph's capabilities, identifying feasible approaches, and guiding the development team towards a functional prototype quickly.

> **Why LangGraph?**
>
> "LangGraph gives the developer a high degree of control by expressing the flow of the application as a set of nodes and edges. All nodes can access and modify a common state (memory). The control flow of the application can be set using edges that connect nodes, either deterministically or via conditional logic."  
> — [LangGraph Documentation](https://langchain-ai.github.io/langgraph/concepts/high_level/)

---

## Table of Contents

1. [Architecture Components](#architecture-components)
2. [Agent Interaction and Workflow](#agent-interaction-and-workflow)
3. [LangGraph Orchestration](#langgraph-orchestration)
4. [Credential Management](#credential-management)
5. [LLM Configuration](#llm-configuration)
6. [Development Roadmap](#development-roadmap)
7. [Security and Compliance](#security-and-compliance)
8. [Next Steps](#next-steps)
9. [Appendix](#appendix)

---

## Architecture Components

Project Pathway's architecture is modular and consists of the following primary components:

1. **Workflow Orchestrator (Pathway)**
2. **Task-Specific Agents**
3. **Agent-D Integration**
4. **Credential Management**
5. **Human-in-the-Loop Mechanisms**

### 1. Workflow Orchestrator (Pathway)

- **Role**: Manages workflows, task sequencing, error handling, and integration with external systems.
- **Technology**: Built using **LangGraph** and **Python**.
- **Responsibilities**:
  - Define and manage workflows using LangGraph's graph structures.
  - Coordinate interactions between specialized agents.
  - Handle task dependencies and conditional logic.
  - Persist state across sessions using LangGraph's persistence features.

> **Quote from LangGraph Documentation**:
>
> "LangGraph provides a powerful framework for building agentic applications by defining workflows as graphs of nodes and edges. We utilize LangGraph's features to manage complex workflows and state."  
> — [LangGraph Orchestration](https://langchain-ai.github.io/langgraph/concepts/)

### 2. Task-Specific Agents

- **Role**: Handle domain-specific tasks within dental administrative workflows.
- **Technology**: Implemented using LangGraph's **StateGraph** or existing LangChain tools.
- **Examples**:
  - **Eligibility Verification Agent**
  - **Claims Processing Agent**
  - **Data Entry Agent**
- **Implementation Notes**:
  - Agents are designed as reusable components within the LangGraph framework.
  - Leverage LangChain integrations for tool support where applicable.
  - Ensure agents are stateless and rely on the orchestrator for state management.

### 3. Agent-D Integration

- **Role**: Facilitates communication between Pathway and **Agent-D** via API.
- **Technology**: Uses HTTP requests to interact with Agent-D's API endpoints.
- **Responsibilities**:
  - Send automation commands to Agent-D.
  - Receive and process responses from Agent-D.
  - Manage API authentication and request formatting.
- **Implementation Notes**:
  - Since LangGraph can make HTTP requests, we implement Agent-D interactions as tools or functions.

### 4. Credential Management

- **Role**: Securely manages login credentials for various portals.
- **Technology**: Environment variables with proper security practices.
- **Responsibilities**:
  - Store and retrieve credentials securely.
  - Provide credentials to the agents without exposing them to the LLMs.
- **Implementation Notes**:
  - Credentials are stored as environment variables following secure practices.
  - Ensure that credentials are handled outside of the LLM context to prevent leakage.
  - Future enhancement: Consider migration to a secrets manager solution.

### 5. Human-in-the-Loop Mechanisms

- **Role**: Allows human operators to intervene in workflows requiring oversight or complex decision-making.
- **Technology**: Integrated within LangGraph workflows, utilizing its support for human interaction patterns.
- **Responsibilities**:
  - Detect scenarios needing human intervention.
  - Pause workflows and wait for human input.
  - Resume automated workflows after input is received.
- **Implementation Notes**:
  - Use LangGraph's persistence and checkpointing features to implement wait states.
  - Implement interfaces or notification mechanisms for human operators.

> **Quote from LangGraph Documentation**:
>
> "LangGraph gives the developer many options for persisting graph state using short-term or long-term (e.g., via a database) memory. This persistence layer enables several different human-in-the-loop interaction patterns with agents; for example, it's possible to pause an agent, review its state, edit its state, and approve a follow-up step."  
> — [LangGraph Persistence](https://langchain-ai.github.io/langgraph/how-tos/persistence/)

---

## Agent Interaction and Workflow

Pathway employs a multi-agent architecture orchestrated by LangGraph, where specialized agents collaborate to execute complex workflows. Agents communicate via defined interfaces, ensuring modularity and scalability.

### Interaction Flow

1. **Workflow Initiation**: The Workflow Orchestrator triggers a workflow based on a task definition.
2. **Task Assignment**: The orchestrator activates the appropriate Task-Specific Agents.
3. **Agent-D Communication**: Agents requiring web automation interact with Agent-D via its API.
4. **Credential Retrieval**: Agents request necessary credentials securely from the Credential Management system.
5. **Execution and Feedback**: Agents perform actions, process results, and update the workflow state.
6. **Human Intervention**: If necessary, the workflow pauses and prompts for human input.
7. **Workflow Completion**: The orchestrator completes the workflow, handling any post-processing.

### Visual Diagram

*(Refer to the diagram in the project's documentation repository.)*

---

## LangGraph Orchestration

LangGraph provides a powerful framework for building agentic applications by defining workflows as graphs of nodes and edges. We utilize LangGraph's features to manage complex workflows and state.

### Graph Structure

- **StateGraph**: Used to define the workflow, where nodes represent tasks or operations, and edges represent transitions.
- **State**: A shared data structure that persists information throughout the workflow execution.

> **Quote from LangGraph Documentation**:
>
> "All nodes can access and modify a common state (memory). The control flow of the application can be set using edges that connect nodes, either deterministically or via conditional logic."  
> — [LangGraph Core Principles](https://langchain-ai.github.io/langgraph/concepts/high_level/)

### Implementing a Workflow with LangGraph

Below is an example of implementing an **Eligibility Verification Workflow** using LangGraph:

```python:pathway/workflows/eligibility_verification.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from pathway.agents.eligibility_verification_agent import EligibilityVerificationAgent
from typing_extensions import TypedDict

# Define the state structure
class EligibilityState(TypedDict):
    patient_info: dict
    eligibility_data: dict
    has_mco: bool
    next_portal: str

# Define the workflow graph
workflow = StateGraph(EligibilityState)

# Define the nodes
def start_workflow(state: EligibilityState):
    # Initialize state if needed
    return state

def collect_patient_info(state: EligibilityState):
    # Collect patient info from input or external source
    state['patient_info'] = get_patient_info()
    return state

def verify_eligibility(state: EligibilityState):
    agent = EligibilityVerificationAgent()
    state = agent.execute(state)
    return state

def check_for_mco(state: EligibilityState):
    # Analyze eligibility data to check for MCO
    state['has_mco'] = 'MCO' in state.get('eligibility_data', {})
    return state

def determine_next_portal(state: EligibilityState):
    # Determine next steps based on MCO
    state['next_portal'] = get_mco_portal(state['eligibility_data'])
    return state

def end_workflow(state: EligibilityState):
    # Finalize workflow
    return state

# Helper functions
def get_patient_info():
    # Implementation to collect patient info
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'dob': '2010-05-05'
    }

def get_mco_portal(eligibility_data):
    # Determine the portal based on eligibility data
    return 'MCO_Portal_URL'

# Add nodes and edges to the workflow
workflow.add_node("start", start_workflow)
workflow.add_node("CollectPatientInfo", collect_patient_info)
workflow.add_node("VerifyEligibility", verify_eligibility)
workflow.add_node("CheckForMCO", check_for_mco)
workflow.add_node("DetermineNextPortal", determine_next_portal)
workflow.add_node("end", end_workflow)

# Define the edges and conditions
workflow.add_edge(START, "start")
workflow.add_edge("start", "CollectPatientInfo")
workflow.add_edge("CollectPatientInfo", "VerifyEligibility")
workflow.add_edge("VerifyEligibility", "CheckForMCO")
workflow.add_conditional_edges(
    "CheckForMCO",
    condition_func=lambda state: state['has_mco'],
    edges={
        True: "DetermineNextPortal",
        False: "end"
    }
)
workflow.add_edge("DetermineNextPortal", "VerifyEligibility")
workflow.add_edge("end", END)

# Set up persistence with MemorySaver
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

*File: `workflows/eligibility_verification.py` defines the eligibility verification workflow using LangGraph.*

#### Notes:

- **Persistence**: We use `MemorySaver` as the checkpointer to persist the state, enabling us to pause and resume workflows as needed.

  > **Quote from LangGraph Documentation**:
  >
  > "When creating any LangGraph graph, you can set it up to persist its state by adding a checkpointer when compiling the graph:
  >
  > ```python
  > from langgraph.checkpoint.memory import MemorySaver
  > checkpointer = MemorySaver()
  > graph.compile(checkpointer=checkpointer)
  > ```
  > This guide shows how you can add thread-level persistence to your graph."  
  > — [LangGraph Persistence](https://langchain-ai.github.io/langgraph/how-tos/persistence/)

- **Node Functions**: Each node function represents a step in the workflow and can modify the state.

1. **Reserved Node Names**: Don't use START/END as node names, they are reserved([2](https://langchain-ai.github.io/langgraph/how-tos/streaming-from-final-node/))
2. **Edge Connections**: Use START and END for edge connections only
3. **Custom Node Names**: Use descriptive names for actual workflow nodes
4. **Proper Edge Definition**: Ensure all nodes are reachable through proper edge connections

### Implementation Notes:

- START and END are special constants used only for edge connections
- All custom nodes should have unique, descriptive names
- Every node must be reachable through the graph's edges
- The workflow must have a clear path from START to END

### Agent Integration

Implement the **Eligibility Verification Agent** as a standard Python class that interacts with Agent-D:

```python:pathway/agents/eligibility_verification_agent.py
from pathway.integration.agent_d import AgentDClient
from pathway.credentials.credential_manager import CredentialManager

class EligibilityVerificationAgent:
    def __init__(self):
        self.agent_d_client = AgentDClient(base_url='http://agent-d/api')
        self.credentials_manager = CredentialManager()

    def execute(self, state):
        patient_info = state['patient_info']
        credentials = self.credentials_manager.get_credentials('MoHealthNet')

        # Send commands to Agent-D to perform web automation
        self.agent_d_client.login(url='https://www.emomed.com/', credentials=credentials)
        eligibility_data = self.agent_d_client.verify_eligibility(patient_info)

        state['eligibility_data'] = eligibility_data
        return state
```

*File: `agents/eligibility_verification_agent.py` implements the eligibility verification using Agent-D.*

#### Notes:

- **Agent-D Client**: Abstracts the API interactions with Agent-D.
- **Credential Management**: Retrieves credentials securely without exposing them to the LLM.

### Feasibility with LangGraph

- **State Management**: LangGraph's `StateGraph` and state persistence capabilities are well-suited for managing the complex workflows required.
- **Conditional Logic**: We can implement sophisticated control flow using conditional edges and node functions.
- **Human-in-the-Loop**: LangGraph supports pausing workflows and waiting for human input, which is essential for our use case.
- **Multi-Agent Orchestration**: LangGraph enables the coordination of multiple agents within a single workflow.

> **Quote from LangGraph Documentation**:
>
> "LangGraph provides a powerful framework for building agentic applications by defining workflows as graphs of nodes and edges. We assume you have already learned the basics covered in the introduction tutorial and want to deepen your understanding of LangGraph's underlying design and inner workings."  
> — [LangGraph Concepts](https://langchain-ai.github.io/langgraph/concepts/)

---

## Credential Management

Security is paramount when handling sensitive information. Our Credential Management component ensures that all login information is stored and accessed securely.

### Implementation

```python:pathway/credentials/credential_manager.py
import os
from typing import Dict, Optional

class CredentialManager:
    def __init__(self):
        # Map of portal names to their environment variable prefixes
        self.portal_prefixes = {
            'MoHealthNet': 'EMOMED',
            'EnvolveDental': 'ENVOLVE',
            'DentaQuest': 'DENTAQUEST',
            'UnitedHealthcare': 'UHC',
            'CyberAccess': 'CYBER',
            'CurveDental': 'CURVE'
        }

    def get_credentials(self, portal_name: str) -> Dict[str, str]:
        """Get credentials for a specific portal from environment variables."""
        prefix = self.portal_prefixes.get(portal_name)
        if not prefix:
            raise ValueError(f"Unknown portal: {portal_name}")

        username = os.getenv(f'{prefix}_USERNAME')
        password = os.getenv(f'{prefix}_PASSWORD')

        if not username or not password:
            raise ValueError(f"Missing credentials for {portal_name}")

        return {
            'username': username,
            'password': password
        }
```

*File: `credentials/credential_manager.py` handles secure retrieval of credentials from environment variables.*

#### Notes:

- **Environment Variables**: Use environment variables for credential storage.
- **No LLM Exposure**: Ensure that credentials are handled outside of the LLM context to prevent leakage.

---

## LLM Configuration

Project Pathway leverages Language Models (LLMs) for decision-making and natural language understanding.

### Supported LLM Providers

1. **OpenAI**
   - Models: GPT-4, GPT-3.5-Turbo
2. **Anthropic**
   - Models: Claude-2, Claude-Instant
3. **Local Models**
   - Models: Llama-2, Mistral
   - Deployment: Self-hosted or via **Groq**

### Configuration Management

Configure LLMs dynamically based on agent requirements using environment variables or configuration files.

```python:pathway/config/llm_config.py
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def get_llm(agent_name):
    if agent_name == 'EligibilityVerificationAgent':
        model_name = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
        api_key = os.environ['OPENAI_API_KEY']
        return ChatOpenAI(model_name=model_name, api_key=api_key)
    elif agent_name == 'ClaimsProcessingAgent':
        model_name = os.environ.get('ANTHROPIC_MODEL', 'claude-2')
        api_key = os.environ['ANTHROPIC_API_KEY']
        return ChatAnthropic(model_name=model_name, api_key=api_key)
    else:
        # Default LLM
        model_name = os.environ.get('DEFAULT_MODEL', 'gpt-4')
        api_key = os.environ['OPENAI_API_KEY']
        return ChatOpenAI(model_name=model_name, api_key=api_key)
```

*File: `config/llm_config.py` dynamically loads LLM configurations based on agent requirements.*

#### Notes:

- **Flexibility**: Allows us to switch between different LLM providers and models based on the specific agent's needs.
- **Environment Variables**: Keep API keys and sensitive configurations secure.

---

## Development Roadmap

To achieve a functional prototype quickly using LangGraph, we propose the following roadmap:

### Phase 1: Core Workflow Implementation

**Objectives**:

- Implement the Workflow Orchestrator using LangGraph.
- Develop the Eligibility Verification Agent.
- Integrate Agent-D for web automation.
- Implement basic Credential Management.

**Steps**:

1. **Set Up Development Environment**:
   - Install LangGraph and necessary dependencies.
   - Ensure Agent-D is accessible via its API.

2. **Implement Workflow Orchestrator**:
   - Define the eligibility verification workflow using LangGraph's `StateGraph`.
   - Utilize node functions for each step in the workflow.

3. **Develop Eligibility Verification Agent**:
   - Implement the agent to interact with Agent-D's API.
   - Ensure secure handling of credentials.

4. **Integrate Agent-D**:
   - Establish API communication between the orchestrator and Agent-D.
   - Test web automation tasks through Agent-D.

5. **Implement Basic Credential Management**:
   - Set up environment variables for portal credentials
   - Implement CredentialManager class to retrieve credentials
   - Document required environment variables:
     ```
     # Required Environment Variables
     EMOMED_USERNAME=xxx
     EMOMED_PASSWORD=xxx
     ENVOLVE_USERNAME=xxx
     ENVOLVE_PASSWORD=xxx
     DENTAQUEST_USERNAME=xxx
     DENTAQUEST_PASSWORD=xxx
     UHC_USERNAME=xxx
     UHC_PASSWORD=xxx
     CYBER_USERNAME=xxx
     CYBER_PASSWORD=xxx
     CURVE_USERNAME=xxx
     CURVE_PASSWORD=xxx
     ```

6. **Testing and Validation**:
   - Write unit tests for individual components.
   - Perform integration testing of the workflow.

### Phase 2: Expand Functionality

**Objectives**:

- Implement additional Task-Specific Agents.
- Introduce Human-in-the-Loop mechanisms.
- Enhance Credential Management.

**Steps**:

1. **Develop Additional Agents**:
   - Claims Processing Agent
   - Data Entry Agent

2. **Enhance Workflows**:
   - Update LangGraph workflows to include new tasks.
   - Implement error handling and conditional logic.

3. **Implement Human-in-the-Loop Mechanisms**:
   - Use LangGraph's persistence to pause workflows and wait for input.
   - Develop interfaces for human operators to provide input.

4. **Improve Credential Management**:
   - Integrate with secure vault solutions.
   - Implement credential rotation policies.

### Phase 3: Security and Compliance

**Objectives**:

- Implement robust security measures.
- Ensure HIPAA compliance.

**Steps**:

1. **Secure Data Handling**:
   - Implement encryption for data at rest and in transit.

2. **Access Controls**:
   - Enforce Role-Based Access Control (RBAC).

3. **Audit Logging**:
   - Use LangGraph's logging capabilities to maintain detailed logs.

4. **Compliance Audits**:
   - Conduct security assessments and ensure all practices meet regulatory standards.

---

## Security and Compliance

Project Pathway must adhere to strict security protocols to protect patient data and comply with regulations like HIPAA.

### Data Protection

- **Encryption**:
  - Use TLS for all communications.
  - Encrypt sensitive data in storage.

- **Access Control**:
  - Implement RBAC.
  - Use multi-factor authentication for administrative access.

### Audit and Monitoring

- **Logging**:
  - Maintain logs for all actions.

- **Monitoring**:
  - Implement tools for intrusion detection and anomaly detection.

- **Regular Audits**:
  - Schedule security assessments and compliance checks.

> **Quote from LangGraph Documentation**:
>
> "LangGraph Server integrates seamlessly with the LangSmith monitoring platform, providing real-time insights into your application's performance and health."  
> — [LangGraph Key Features](https://langchain-ai.github.io/langgraph/concepts/langgraph_server)

---

## Next Steps

To proceed towards a functional prototype:

1. **Implement the Eligibility Verification Workflow**:
   - Follow the implementation steps outlined in Phase 1.

2. **Set Up Agent-D Integration**:
   - Ensure Agent-D's API is operational and accessible.

3. **Secure the Environment**:
   - Set up required environment variables for portal credentials
   - Document required environment variables
   - Implement proper credential handling practices

4. **Test the Workflow**:
   - Run test cases to validate each part of the workflow.

5. **Iterate Based on Feedback**:
   - Refine the implementation based on test results.

---

## Conclusion

By leveraging LangGraph's capabilities for orchestrating multi-agent systems, we can build a robust and scalable solution for automating dental administrative workflows. Focusing on a phased development approach allows us to achieve a functional prototype quickly, laying the groundwork for further expansion and improvement.

---

## Appendix

### Reference Materials

- **LangGraph Documentation**: [LangGraph Official Docs](https://langchain-ai.github.io/langgraph/)
- **LangChain Documentation**: [LangChain Official Docs](https://python.langchain.com/)
- **Task Definitions**: Refer to `TASKS.md` for detailed task descriptions.
- **Background Information**: See `BACKGROUND.md` for project context.

### Example Workflow: Medicaid Eligibility Verification

We begin by implementing the eligibility verification workflow as detailed in Phase 1.

---

By incorporating these adjustments and focusing on what's feasible with LangGraph, we ensure that the development team is guided effectively towards building a functional prototype of Project Pathway.

### Development Environment Security
- **Credential Storage**:
  - Currently using environment variables for development
  - TODO: Migrate to a secure secrets manager (AWS Secrets Manager, HashiCorp Vault) for production
  - Use `.env.example` to document required credentials without exposing actual values
  - Ensure `.env` is in `.gitignore`