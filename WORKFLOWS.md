# Workflow Document

## Preface

This document outlines a series of workflows designed to automate dental administrative tasks using **LangGraph**. The workflows progress from simple to more complex, providing a structured approach to building functionality while adhering to LangGraph best practices. Each workflow is designed to be a cohesive process that can be implemented using LangGraph's stateful, graph-based orchestration capabilities.

---

### **Phase 1: Basic Workflow Implementation**

#### **Workflow 1: Login to a Single Portal**

- **Objective:** Automate the login process to a single dental provider portal (e.g., MoHealthNet).
- **Details:**
  - Use LangGraph to orchestrate the workflow.
  - Securely retrieve credentials using the `CredentialManager`.
  - Navigate to `emomed.com` and perform the login.
  - Handle errors and invalid credentials gracefully.
  - **LangGraph Best Practices:**
    - Use a `StateGraph` to manage the state.
    - Implement nodes for credential retrieval, navigation, login, and error handling.
    - Use conditional edges to handle login success or failure.

##### **Implementation Example:**

```python:pathway/workflows/login_workflow.py
from langgraph.graph import StateGraph, START, END
from pathway.agents.portal_login_agent import PortalLoginAgent
from pathway.credentials.credential_manager import CredentialManager
from typing import TypedDict

class LoginState(TypedDict):
    portal_name: str
    login_successful: bool

workflow = StateGraph(LoginState)

def start(state: LoginState):
    state['login_successful'] = False
    return state

def retrieve_credentials(state: LoginState):
    credentials_manager = CredentialManager()
    state['credentials'] = credentials_manager.get_credentials(state['portal_name'])
    return state

def perform_login(state: LoginState):
    agent = PortalLoginAgent()
    state['login_successful'] = agent.login(state['portal_name'], state['credentials'])
    return state

def handle_login_success(state: LoginState):
    # Proceed with post-login actions
    return state

def handle_login_failure(state: LoginState):
    # Log error and terminate workflow
    return state

workflow.add_node('start', start)
workflow.add_node('RetrieveCredentials', retrieve_credentials)
workflow.add_node('PerformLogin', perform_login)
workflow.add_node('HandleLoginSuccess', handle_login_success)
workflow.add_node('HandleLoginFailure', handle_login_failure)
workflow.add_node('end', lambda state: state)

workflow.add_edge(START, 'start')
workflow.add_edge('start', 'RetrieveCredentials')
workflow.add_edge('RetrieveCredentials', 'PerformLogin')
workflow.add_conditional_edges(
    'PerformLogin',
    condition_func=lambda state: state['login_successful'],
    edges={
        True: 'HandleLoginSuccess',
        False: 'HandleLoginFailure'
    }
)
workflow.add_edge('HandleLoginSuccess', 'end')
workflow.add_edge('HandleLoginFailure', 'end')
workflow.add_edge('end', END)

# Compile the workflow
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

---

### **Phase 2: Data Retrieval Workflows**

#### **Workflow 2: Eligibility Verification**

- **Objective:** Verify Medicaid eligibility for a patient and retrieve coverage details.
- **Details:**
  - After logging into MoHealthNet, navigate to the "Eligibility Verification" section.
  - Input patient details (e.g., John Doe, DOB: May 5, 2010).
  - Retrieve and store the patient's DCN and coverage information.
  - Check for primary insurance and flag if found.
  - **LangGraph Best Practices:**
    - Separate nodes for navigation, data input, data retrieval, and condition checks.
    - Use the shared state to pass patient information and retrieved data.
    - Implement human-in-the-loop mechanisms for cases requiring manual review.

##### **Implementation Example:**

```python:pathway/workflows/eligibility_verification_workflow.py
from langgraph.graph import StateGraph, START, END
from pathway.agents.eligibility_agent import EligibilityAgent
from typing import TypedDict

class EligibilityState(TypedDict):
    patient_info: dict
    eligibility_data: dict
    has_primary_insurance: bool

workflow = StateGraph(EligibilityState)

def start(state: EligibilityState):
    state['has_primary_insurance'] = False
    return state

def navigate_to_eligibility(state: EligibilityState):
    agent = EligibilityAgent()
    agent.navigate_to_eligibility_section()
    return state

def input_patient_details(state: EligibilityState):
    agent = EligibilityAgent()
    agent.input_patient_details(state['patient_info'])
    return state

def retrieve_eligibility_data(state: EligibilityState):
    agent = EligibilityAgent()
    state['eligibility_data'] = agent.retrieve_eligibility_data()
    return state

def check_primary_insurance(state: EligibilityState):
    state['has_primary_insurance'] = 'PrimaryInsurance' in state['eligibility_data']
    return state

def handle_primary_insurance(state: EligibilityState):
    # Implement human-in-the-loop if required
    return state

def end(state: EligibilityState):
    return state

workflow.add_node('start', start)
workflow.add_node('NavigateToEligibility', navigate_to_eligibility)
workflow.add_node('InputPatientDetails', input_patient_details)
workflow.add_node('RetrieveEligibilityData', retrieve_eligibility_data)
workflow.add_node('CheckPrimaryInsurance', check_primary_insurance)
workflow.add_node('HandlePrimaryInsurance', handle_primary_insurance)
workflow.add_node('end', end)

workflow.add_edge(START, 'start')
workflow.add_edge('start', 'NavigateToEligibility')
workflow.add_edge('NavigateToEligibility', 'InputPatientDetails')
workflow.add_edge('InputPatientDetails', 'RetrieveEligibilityData')
workflow.add_edge('RetrieveEligibilityData', 'CheckPrimaryInsurance')
workflow.add_conditional_edges(
    'CheckPrimaryInsurance',
    condition_func=lambda state: state['has_primary_insurance'],
    edges={
        True: 'HandlePrimaryInsurance',
        False: 'end'
    }
)
workflow.add_edge('HandlePrimaryInsurance', 'end')
workflow.add_edge('end', END)

# Compile the workflow
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

---

### **Phase 3: Data Entry Workflows**

#### **Workflow 3: Intake Data Processing**

- **Objective:** Extract intake data from an external form (e.g., JotForm) and enter it into the practice management system (Curve Dental).
- **Details:**
  - Access patient's completed form submission.
  - Extract demographic and insurance information.
  - Log into Curve Dental and create a new patient profile.
  - Input all extracted data into the system.
  - **LangGraph Best Practices:**
    - Use nodes to handle data extraction, transformation, and entry.
    - Implement error handling for data inconsistencies.
    - Keep agents stateless and manage data through the workflow's state.

---

### **Phase 4: Claims Preparation Workflows**

#### **Workflow 4: Claims Creation and Adjustment**

- **Objective:** Prepare a claim form and adjust codes for Medicaid compliance.
- **Details:**
  - Input services rendered into the PMS (e.g., procedure codes).
  - Review the claim for non-covered codes.
  - Replace non-covered codes with Medicaid-approved alternatives.
  - Initiate prior authorization if required.
  - **LangGraph Best Practices:**
    - Use conditional logic to handle code adjustments.
    - Modularize steps for claim creation, review, and submission.
    - Integrate with external databases or APIs for code validation.

---

### **Phase 5: Claims Submission Workflows**

#### **Workflow 5: Automated Claim Submission**

- **Objective:** Submit a new claim via a provider portal (e.g., Envolve Dental) and handle responses.
- **Details:**
  - Log into the provider portal.
  - Access the claims submission section.
  - Enter patient and service details.
  - Submit the claim and record confirmation.
  - Check claim status and handle denials.
  - **LangGraph Best Practices:**
    - Implement nodes for each interaction with the portal.
    - Use persistence to track claim status over time.
    - Incorporate human-in-the-loop for denial resolutions.

---

### **Phase 6: Comprehensive Data Workflows**

#### **Workflow 6: Patient Data Consolidation**

- **Objective:** Consolidate patient data from multiple sources into a single summary document.
- **Details:**
  - Retrieve data from portals like MoHealthNet and CyberAccess.
  - Organize data into categories (medical history, medications, etc.).
  - Identify critical health information.
  - Format the summary for clinical use.
  - **LangGraph Best Practices:**
    - Use separate agents for data retrieval from each source.
    - Combine data within the shared state.
    - Ensure data integrity and handle discrepancies.

---

### **Phase 7: Error Handling and Adaptability Workflows**

#### **Workflow 7: Robust Error Handling and Retry Mechanisms**

- **Objective:** Implement workflows that can handle errors gracefully and retry operations.
- **Details:**
  - Detect failed operations (e.g., login failures).
  - Log errors with detailed information.
  - Retry operations with correct data.
  - Escalate to human intervention if issues persist.
  - **LangGraph Best Practices:**
    - Use exception handling within node functions.
    - Implement retry logic with counters to prevent infinite loops.
    - Utilize conditional edges to route to error handling nodes.

---

### **Phase 8: Human-in-the-Loop Workflows**

#### **Workflow 8: Human Decision Integration**

- **Objective:** Pause workflows to allow for human input when critical decisions are needed.
- **Details:**
  - Detect scenarios requiring human intervention (e.g., primary insurance detected).
  - Pause the workflow and notify a human operator.
  - Allow the operator to provide input or modify the state.
  - Resume the workflow after receiving input.
  - **LangGraph Best Practices:**
    - Use LangGraph's persistence and checkpointing features.
    - Implement nodes that wait for external input.
    - Ensure secure interfaces for human operators to interact with the workflow.

---

### **Phase 9: Advanced Automation Workflows**

#### **Workflow 9: End-to-End Claims Processing Automation**

- **Objective:** Automate the full claims processing workflow, from eligibility verification to claims submission and tracking.
- **Details:**
  - Combine previous workflows into a comprehensive process.
  - Handle multiple patients in batch processing.
  - Optimize performance and resource management.
  - Implement learning mechanisms to adapt based on historical data.
  - **LangGraph Best Practices:**
    - Modularize the workflow into reusable subgraphs.
    - Leverage LangGraph's ability to handle cycles and complex flows.
    - Maintain clear and manageable state throughout the workflow.
    - Monitor and log performance metrics for continuous improvement.

---

### **Phase 10: Deployment Workflows**

#### **Workflow 10: Workflow Deployment and Monitoring**

- **Objective:** Deploy workflows in test and production environments with monitoring capabilities.
- **Details:**
  - Set up environment-specific configurations.
  - Implement secure credential handling for different environments.
  - Provide a user interface or dashboard for monitoring and managing workflows.
  - Conduct user acceptance testing and gather feedback.
  - **LangGraph Best Practices:**
    - Use environment variables and configuration files securely.
    - Employ LangGraph's built-in support for monitoring and integration with tools like LangSmith.
    - Ensure compliance with security and regulatory standards during deployment.

---

## Additional Considerations

- **Security and Compliance:**
  - Ensure all workflows adhere to HIPAA regulations.
  - Implement encryption for data at rest and in transit.
  - Enforce role-based access control (RBAC).
  - Maintain detailed audit logs using LangGraph's logging capabilities.

- **Error Logging and Monitoring:**
  - Utilize LangGraph's streaming and persistence features to monitor workflows in real-time.
  - Implement alerting mechanisms for critical failures or required human interventions.

- **Performance Optimization:**
  - Leverage parallel processing where appropriate.
  - Optimize agents and nodes for efficiency.
  - Continuously profile workflows to identify bottlenecks.

- **Agent Design Principles:**
  - Keep agents stateless; manage state within the workflow.
  - Ensure agents have clear responsibilities and interfaces.
  - Reuse agents across multiple workflows to promote modularity.

---

## Conclusion

By progressively building these workflows and adhering to LangGraph best practices, you can develop a robust and scalable system for automating complex dental administrative tasks. Each workflow serves as a building block towards comprehensive automation, allowing for gradual implementation and continuous improvement.

---

# Full Example of a Workflow Implementation

To illustrate how LangGraph best practices are applied in a workflow, here's a detailed implementation of **Workflow 2: Eligibility Verification**.

```python:pathway/workflows/eligibility_verification_workflow.py
from langgraph.graph import StateGraph, START, END
from pathway.agents.navigation_agent import NavigationAgent
from pathway.agents.eligibility_agent import EligibilityAgent
from pathway.agents.human_in_the_loop_agent import HumanInTheLoopAgent
from pathway.credentials.credential_manager import CredentialManager
from typing import TypedDict

class EligibilityState(TypedDict):
    portal_name: str
    patient_info: dict
    credentials: dict
    eligibility_data: dict
    has_primary_insurance: bool
    human_verified: bool

workflow = StateGraph(EligibilityState)

def start(state: EligibilityState):
    state['portal_name'] = 'MoHealthNet'
    state['has_primary_insurance'] = False
    state['human_verified'] = False
    return state

def retrieve_credentials(state: EligibilityState):
    credentials_manager = CredentialManager()
    state['credentials'] = credentials_manager.get_credentials(state['portal_name'])
    return state

def perform_login(state: EligibilityState):
    agent = NavigationAgent()
    login_successful = agent.login(state['portal_name'], state['credentials'])
    if not login_successful:
        raise Exception('Login failed')
    return state

def navigate_to_eligibility(state: EligibilityState):
    agent = EligibilityAgent()
    agent.navigate_to_eligibility_section()
    return state

def input_patient_details(state: EligibilityState):
    agent = EligibilityAgent()
    agent.input_patient_details(state['patient_info'])
    return state

def retrieve_eligibility_data(state: EligibilityState):
    agent = EligibilityAgent()
    state['eligibility_data'] = agent.retrieve_eligibility_data()
    return state

def check_primary_insurance(state: EligibilityState):
    state['has_primary_insurance'] = 'PrimaryInsurance' in state['eligibility_data']
    return state

def handle_primary_insurance(state: EligibilityState):
    if state['has_primary_insurance'] and not state['human_verified']:
        agent = HumanInTheLoopAgent()
        state = agent.verify_primary_insurance(state)
    return state

def end(state: EligibilityState):
    return state

# Add nodes
workflow.add_node('start', start)
workflow.add_node('RetrieveCredentials', retrieve_credentials)
workflow.add_node('PerformLogin', perform_login)
workflow.add_node('NavigateToEligibility', navigate_to_eligibility)
workflow.add_node('InputPatientDetails', input_patient_details)
workflow.add_node('RetrieveEligibilityData', retrieve_eligibility_data)
workflow.add_node('CheckPrimaryInsurance', check_primary_insurance)
workflow.add_node('HandlePrimaryInsurance', handle_primary_insurance)
workflow.add_node('end', end)

# Add edges
workflow.add_edge(START, 'start')
workflow.add_edge('start', 'RetrieveCredentials')
workflow.add_edge('RetrieveCredentials', 'PerformLogin')
workflow.add_edge('PerformLogin', 'NavigateToEligibility')
workflow.add_edge('NavigateToEligibility', 'InputPatientDetails')
workflow.add_edge('InputPatientDetails', 'RetrieveEligibilityData')
workflow.add_edge('RetrieveEligibilityData', 'CheckPrimaryInsurance')
workflow.add_edge('CheckPrimaryInsurance', 'HandlePrimaryInsurance')
workflow.add_edge('HandlePrimaryInsurance', 'end')
workflow.add_edge('end', END)

# Compile the workflow with persistence
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

### **Key Points:**

- **Node Functions:** Each function represents a distinct action in the workflow, maintaining single responsibility.
- **Error Handling:** Exceptions are raised for critical failures (e.g., login failure), which can be caught and managed by the workflow or external systems.
- **Conditional Logic:** The `handle_primary_insurance` function uses a condition to determine if human verification is needed.
- **Human-in-the-Loop Integration:** The `HumanInTheLoopAgent` is used to pause the workflow and await human input.
- **State Management:** The `EligibilityState` TypedDict defines all the data passed through the workflow.

---

This detailed example demonstrates how to implement a workflow in LangGraph while adhering to best practices. By structuring workflows in this way, you can build scalable, maintainable, and reliable automation processes.
