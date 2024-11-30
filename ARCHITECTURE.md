# Project Pathway Architecture Design

## Introduction

Project Pathway aims to automate complex dental administrative workflows that require secure authentication across multiple platforms. By leveraging **LangGraph** for orchestration and **Agent-D** for web automation, we build a multi-agent system that coordinates specialized agents to handle tasks such as eligibility verification, claims processing, appointment scheduling, and data consolidation.

This document provides an updated architecture design for Project Pathway, integrating LangGraph's best practices and Agent-D integration.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Agent Hierarchy and Design](#agent-hierarchy-and-design)
4. [Agent-D Integration and Command Crafting](#agent-d-integration-and-command-crafting)
5. [LangGraph Orchestration](#langgraph-orchestration)
6. [Credential Management and Security](#credential-management-and-security)
7. [Development Roadmap](#development-roadmap)
8. [Security and Compliance](#security-and-compliance)
9. [Deployment and Monitoring](#deployment-and-monitoring)
10. [Conclusion](#conclusion)
11. [Appendix](#appendix)

---

## Architecture Overview

Project Pathway's architecture is modular and consists of the following primary components:

1. **Supervisor Agent**: Routes tasks based on context and requirements.
2. **Specialist Agents**: Handle domain-specific tasks (e.g., Medicaid Specialist).
3. **Portal Agents**: Interface with specific web portals via Agent-D.
4. **Credential Management**: Securely handles portal credentials.
5. **Human-in-the-Loop Mechanisms**: Facilitates human intervention when needed.

### Key Design Principles

- **Hierarchical Agent Structure**: Agents are organized in a hierarchy from general to specific, promoting modularity and reuse.
- **Stateless Agents with Shared State**: Agents are designed to be stateless, with the workflow state managed by LangGraph's `StateGraph`.
- **Command Encapsulation**: Portal agents encapsulate Agent-D command crafting, following best practices for security and precision.
- **State Management and Persistence**: LangGraph manages workflow state, supporting persistence across sessions for long-running operations.
- **Human-in-the-Loop Integration**: Workflows can pause to await human input, enhancing reliability and compliance.
- **Modularity and Scalability**: Each agent has a single responsibility and clear interfaces, facilitating scalability and maintainability.
- **Security and Compliance**: Credentials are handled securely and separately from commands, adhering to HIPAA and other regulations.

---

## Directory Structure

```
project-pathway/
├── agents/
│   ├── supervisor_agent.py
│   ├── insurance/
│   │   ├── insurance_agent.py
│   │   ├── medicaid/
│   │   │   ├── medicaid_specialist_agent.py
│   │   │   └── portals/
│   │   │       ├── state_medicaid/
│   │   │       │   └── mohealthnet_agent.py
│   │   │       ├── mcos/
│   │   │       │   ├── envolve_dental_agent.py
│   │   │       │   ├── dentaquest_agent.py
│   │   │       │   └── unitedhealthcare_agent.py
│   │   │       └── cdss/
│   │   │           └── cyberaccess_agent.py
│   └── pms/
│       ├── pms_agent.py
│       └── curve/
│           └── curve_dental_agent.py
├── workflows/
│   ├── eligibility_verification_workflow.py
│   ├── claims_processing_workflow.py
│   ├── data_consolidation_workflow.py
│   └── appointment_scheduling_workflow.py
├── config/
│   └── llm_config.py
├── credentials/
│   └── credential_manager.py
├── integration/
│   └── agent_d_client.py
├── utils/
│   └── portal_utils.py
```

---

## Agent Hierarchy and Design

### 1. Supervisor Agent

- **Role**: Routes tasks based on context and requirements.
- **Responsibilities**:
  - Analyze user queries.
  - Determine appropriate specialist agent.
  - Delegate tasks.
  - Aggregate results.
- **Implementation**:
  - Designed to be stateless.
  - Uses LLM for task planning and delegation.
  - Interacts with the shared workflow state managed by LangGraph.

### 2. Specialist Agents

- **Role**: Handle domain-specific tasks.
- **Examples**:
  - `MedicaidSpecialistAgent`
  - `InsuranceAgent`
  - `PMSAgent`
- **Responsibilities**:
  - Coordinate portal agents.
  - Handle business logic.
  - Aggregate portal results.
- **Design Principles**:
  - Stateless agents with single responsibility.
  - Clear interfaces for interaction.

### 3. Portal Agents

- **Role**: Interface with specific web portals.
- **Examples**:
  - `MoHealthNetAgent`
  - `EnvolveDentalAgent`
  - `DentaQuestAgent`
- **Responsibilities**:
  - Craft Agent-D commands following best practices.
  - Handle portal-specific logic.
  - Parse portal responses.
  - Update the shared workflow state.
- **Command Crafting**:
  - Follow guidelines from `COMMAND_BEST_PRACTICES.md`.
  - Ensure security and precision in commands.

---

## Agent-D Integration and Command Crafting

### Command Crafting Best Practices

Portal agents are responsible for crafting commands that Agent-D can execute. Commands should:

- Be specific and detailed.
- Include conditional logic.
- Handle potential errors.
- Follow best practices from `COMMAND_BEST_PRACTICES.md`.

**Example Command Structure:**

```python:agents/portals/mohealthnet_agent.py
command = f"""
Go to {portal_url} and log in using the enter secret credentials tool.
If you cannot log in the first time, terminate and report the error message.
Then, navigate to the 'Eligibility Verification' section.
Enter the patient's information:
- First Name: {patient_info.get('first_name')}
- Last Name: {patient_info.get('last_name')}
- Date of Birth: {patient_info.get('dob')}
Retrieve and report the following information:
- DCN Number
- Benefits/Coverage Details
- Primary Insurance Information
If primary insurance is detected, flag for human verification.
"""
```

### Secure Credential Handling

- **Never include credentials in commands**.
- Use the `CredentialManager` to securely retrieve credentials.
- Set credentials in Agent-D without exposing them to LLMs.

### AgentDClient

The `AgentDClient` class provides methods for:

- Executing commands with streaming support.
- Setting credentials securely.
- Handling responses and errors.

---

## LangGraph Orchestration

### Workflow Definition

Workflows are defined using LangGraph's `StateGraph`, ensuring that agents remain stateless and all state management is handled within the workflow.

**Example:**

```python:workflows/eligibility_verification_workflow.py
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class EligibilityState(TypedDict):
    patient_info: dict
    eligibility_data: dict
    has_primary_insurance: bool
    human_verified: bool

workflow = StateGraph(EligibilityState)
```

### State Management and Persistence

- **Shared State**: All nodes access and modify a common state, defined using `TypedDict`.
- **Persistence**: Utilize LangGraph's checkpointing to persist state across sessions, essential for long-running workflows and human-in-the-loop mechanisms.
- **Human-in-the-Loop**: Implement nodes that pause the workflow, await human input, and resume operations.

### Node Implementation

```python:workflows/eligibility_verification_workflow.py
def retrieve_credentials(state: EligibilityState):
    credentials_manager = CredentialManager()
    state['credentials'] = credentials_manager.get_credentials('MoHealthNet')
    return state

workflow.add_node('RetrieveCredentials', retrieve_credentials)
```

### Error Handling and Retries

- Use exception handling within node functions.
- Implement retry logic with counters to prevent infinite loops.
- Use conditional edges to route to error handling nodes.

---

## Credential Management and Security

### Secure Credential Handling

- Store credentials securely using a vault service or encrypted storage.
- Use the `CredentialManager` for credentials retrieval and management.
- Ensure that credentials are never logged or included in commands to Agent-D.

### Required Environment Variables

```bash
# Portal Credentials (stored securely, not in plaintext)
EMOMED_USERNAME
EMOMED_PASSWORD
ENVOLVE_USERNAME
ENVOLVE_PASSWORD
# ... other credentials ...

# API Configuration
AGENT_D_BASE_URL
API_CLIENT_SECRET
OPENAI_API_KEY
```

---

## Development Roadmap

### Phase 1: Core Implementation

1. **Implement Supervisor Agent** with LLM planning.
2. **Develop Stateless Portal Agents** following LangGraph best practices.
3. **Set Up Agent-D Integration** with secure command crafting.
4. **Create Initial Workflows** using `StateGraph` and shared state.

### Phase 2: Enhanced Functionality

1. **Add More Portal Agents** and specialist agents.
2. **Implement Complex Workflows** with human-in-the-loop mechanisms.
3. **Enhance Error Handling** and introduce retry mechanisms.
4. **Integrate LangGraph Studio** for debugging and visualization.

### Phase 3: Production Readiness

1. **Implement Comprehensive Testing** including unit and integration tests.
2. **Add Monitoring and Logging** using LangGraph's logging capabilities.
3. **Enhance Security Measures** with regular audits and compliance checks.
4. **Deploy to Production** using LangGraph Platform for smooth deployment.

---

## Security and Compliance

### Data Protection and HIPAA Compliance

- **Encryption**: Encrypt sensitive data at rest and in transit.
- **Access Controls**: Implement role-based access control (RBAC) and multi-factor authentication.
- **Audit Logging**: Maintain detailed logs using LangGraph's logging features.
- **Regular Audits**: Conduct security assessments and compliance audits regularly.

### Error Handling and Monitoring

- **Graceful Error Recovery**: Implement try-except blocks and error-handling nodes.
- **Detailed Error Logging**: Use LangGraph's logging system to capture error details.
- **Alerts and Notifications**: Set up alerting mechanisms for critical failures.
- **Human Intervention Triggers**: Automatically notify human operators when required.

---

## Deployment and Monitoring

### LangGraph Studio and Platform

- **LangGraph Studio**: Utilize for visualization, debugging, and testing of workflows.
- **LangGraph Platform**: Deploy workflows in production, benefiting from features like monitoring and scaling.

### Continuous Integration/Continuous Deployment (CI/CD)

- **Automated Testing**: Implement automated tests that run during the CI/CD pipeline.
- **Version Control**: Use Git for version control, ensuring codebase integrity.
- **Environment Management**: Maintain separate configurations for development, testing, and production environments.

### Monitoring and Logging

- **Performance Metrics**: Monitor workflow performance, throughput, and latency.
- **Error Tracking**: Keep track of errors and exceptions for timely resolution.
- **Resource Utilization**: Monitor system resources to optimize performance.

---

## Conclusion

This updated architecture incorporates **LangGraph's** best practices for building a robust, scalable, and secure dental administrative automation system. By emphasizing stateless agent design, secure credential management, and advanced workflow orchestration, Project Pathway can effectively automate complex tasks while maintaining compliance with healthcare regulations.

**Key Enhancements:**

- Integration of LangGraph's state management and human-in-the-loop capabilities.
- Implementation of secure command crafting and credential handling with Agent-D.
- Detailed workflows utilizing LangGraph's features for error handling and persistence.
- Emphasis on security, compliance, and deployment best practices.

---

## Appendix

### Reference Materials

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- `COMMAND_BEST_PRACTICES.md`
- `WORKFLOWS.md`
- `TASKS.md`

### Development Environment Setup

See `README.md` for detailed setup instructions.

---

# Additional Notes

- **Agent Design Principles**: Agents are designed to be stateless, focusing on single responsibilities, which aligns with LangGraph's recommendation for agent architectures.
- **Stateful Workflows**: Workflows manage the state transitions and data passing between agents, utilizing LangGraph's `StateGraph`.
- **Human-in-the-Loop**: Incorporation of human input points enhances reliability, especially for tasks requiring human judgment or verification.

---

By integrating these improvements, the architecture is better aligned with LangGraph's capabilities and best practices, ensuring a more robust and maintainable system.
