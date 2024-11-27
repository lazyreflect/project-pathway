# Implementing Phase 1: Basic Navigation and Authentication with LangGraph and Agent-D

Welcome back to the Project Pathway development guide! In this phase, we will extend our application to handle more complex tasks involving navigation and authentication across multiple healthcare portals. We will also address the implementation of a **Two-Factor Authentication (2FA)** solution to handle scenarios where verification codes are sent via email.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Step 1: Extend Credential Management](#step-1-extend-credential-management)
4. [Step 2: Implement Portal Login Agents](#step-2-implement-portal-login-agents)
    - [2.1. MoHealthNet Portal Login](#21-mohealthnet-portal-login)
    - [2.2. Envolve Dental Login](#22-envolve-dental-login)
    - [2.3. DentaQuest Login with 2FA Handling](#23-dentaquest-login-with-2fa-handling)
    - [2.4. UnitedHealthcare Dental Login](#24-unitedhealthcare-dental-login)
    - [2.5. CyberAccess Login with License Agreement Handling](#25-cyberaccess-login-with-license-agreement-handling)
    - [2.6. Curve Dental Login](#26-curve-dental-login)
5. [Step 3: Implement 2FA Handling via Email](#step-3-implement-2fa-handling-via-email)
6. [Step 4: Update the LangGraph Workflows](#step-4-update-the-langgraph-workflows)
7. [Step 5: Test the Agents](#step-5-test-the-agents)
8. [Conclusion](#conclusion)
9. [Appendix](#appendix)

---

## Introduction

In **Phase 1**, we focus on implementing agents that can navigate to specific healthcare portals, handle login procedures, and manage any additional steps such as accepting license agreements or handling multi-factor authentication (MFA). We will build upon the foundations laid in Phase 0 and assume that the development environment is already set up as per `GET_STARTED.md`.

---

## Prerequisites

- Completion of **Phase 0**, including a working development environment.
- Updated `TASKS.md` outlining Phase 1 tasks.
- API access to **Agent-D** and necessary credentials for the healthcare portals.
- Access to a **Gmail account** configured for receiving verification codes.

---

## Step 1: Extend Credential Management

Enhance the `CredentialManager` to support credentials for all the portals involved in Phase 1.

### 1.1. Update the Credential Manager

```python:credentials/credential_manager.py
import os
from typing import Dict

class CredentialManager:
    """Handles retrieval of credentials from environment variables."""

    def __init__(self):
        self.portal_prefixes = {
            'MoHealthNet': 'EMOMED',
            'EnvolveDental': 'ENVOLVE',
            'DentaQuest': 'DENTAQUEST',
            'UnitedHealthcare': 'UHC',
            'CyberAccess': 'CYBER',
            'CurveDental': 'CURVE',
            'Gmail': 'GMAIL'  # For 2FA email retrieval
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

> **File**: `credentials/credential_manager.py`  
> **Purpose**: Extended to include credentials for all portals and Gmail for 2FA handling.

### 1.2. Document Required Environment Variables

Update your `.env.example` file to include placeholders for all necessary credentials:

```
# MoHealthNet Portal (eMOMED) Credentials
EMOMED_USERNAME=your_username
EMOMED_PASSWORD=your_password

# Envolve Dental Credentials
ENVOLVE_USERNAME=your_username
ENVOLVE_PASSWORD=your_password

# DentaQuest Credentials
DENTAQUEST_USERNAME=your_username
DENTAQUEST_PASSWORD=your_password

# UnitedHealthcare Dental (DentalHub) Credentials
UHC_USERNAME=your_username
UHC_PASSWORD=your_password

# CyberAccess Credentials
CYBER_USERNAME=your_username
CYBER_PASSWORD=your_password

# Curve Dental Credentials
CURVE_USERNAME=your_username
CURVE_PASSWORD=your_password

# Gmail Credentials for 2FA Handling
GMAIL_USERNAME=your_email@gmail.com
GMAIL_PASSWORD=your_email_app_password  # Use an App Password if 2FA is enabled
```

> **Security Note**: Ensure your `.env` file is included in `.gitignore` and never committed to version control.

---

## Step 2: Implement Portal Login Agents

We will create individual agents for each portal, each capable of handling the specific login procedures and any additional steps required.

### 2.1. MoHealthNet Portal Login

#### 2.1.1. Create the Agent

```python:agents/mohealthnet_login_agent.py
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager

class MoHealthNetLoginAgent:
    """Agent to log into the MoHealthNet provider portal."""

    def __init__(self):
        self.agent_d_client = AgentDClient()
        self.credential_manager = CredentialManager()

    def execute(self, state):
        credentials = self.credential_manager.get_credentials('MoHealthNet')
        command = f"""
        Navigate to https://www.emomed.com/
        Use the login form to enter the username and password.
        If login fails, terminate and report the error message.
        Verify successful login by checking if the URL is https://www.emomed.com/portal/wps/myportal
        """
        response = self.agent_d_client.execute_command(command, credentials)
        state['login_status'] = response
        return state
```

> **File**: `agents/mohealthnet_login_agent.py`

#### 2.1.2. Notes

- The agent constructs a command detailing the steps.
- Credentials are securely retrieved and passed to Agent-D.
- Agent-D handles the web automation.

### 2.2. Envolve Dental Login

Follow a similar pattern as above to create `envolve_dental_login_agent.py`.

#### 2.2.1. Create the Agent

```python:agents/envolve_dental_login_agent.py
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager

class EnvolveDentalLoginAgent:
    """Agent to log into the Envolve Dental provider portal."""

    def __init__(self):
        self.agent_d_client = AgentDClient()
        self.credential_manager = CredentialManager()

    def execute(self, state):
        credentials = self.credential_manager.get_credentials('EnvolveDental')
        command = f"""
        Navigate to https://pwp.envolvedental.com/
        Use the login form to enter the username and password.
        If login fails, terminate and report the error message.
        Verify successful login by checking if the URL is https://pwp.envolvedental.com/PWP/Dental
        """
        response = self.agent_d_client.execute_command(command, credentials)
        state['login_status'] = response
        return state
```

> **File**: `agents/envolve_dental_login_agent.py`

### 2.3. DentaQuest Login with 2FA Handling

#### 2.3.1. Create the Agent

```python:agents/dentaquest_login_agent.py
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager

class DentaQuestLoginAgent:
    """Agent to log into the DentaQuest provider portal with 2FA handling."""

    def __init__(self):
        self.agent_d_client = AgentDClient()
        self.credential_manager = CredentialManager()

    def execute(self, state):
        credentials = self.credential_manager.get_credentials('DentaQuest')
        command = f"""
        Navigate to https://providers.dentaquest.com/
        Use the login form to enter the username and password.
        Handle any email verification code if prompted.
        If login fails, terminate and report the error message.
        Verify successful login by checking if the URL is https://providers.dentaquest.com/dashboard/
        """
        response = self.agent_d_client.execute_command(command, credentials)
        if 'verification code' in response.lower():
            state = self.handle_2fa(state)
        state['login_status'] = response
        return state

    def handle_2fa(self, state):
        """Retrieve verification code from email and pass it to Agent-D."""
        from pathway.integration.gmail_client import GmailClient

        gmail_client = GmailClient()
        verification_code = gmail_client.get_latest_verification_code()
        command = f"""
        Enter the verification code: {verification_code}
        """
        response = self.agent_d_client.execute_command(command)
        state['2fa_status'] = response
        return state
```

> **File**: `agents/dentaquest_login_agent.py`

#### 2.3.2. Notes

- Handles 2FA by retrieving the verification code from Gmail.
- We will implement `GmailClient` in Step 3.

### 2.4. UnitedHealthcare Dental Login

Create `unitedhealthcare_login_agent.py` following the same pattern.

```python:agents/unitedhealthcare_login_agent.py
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager

class UnitedHealthcareLoginAgent:
    """Agent to log into the UnitedHealthcare Dental portal."""

    def __init__(self):
        self.agent_d_client = AgentDClient()
        self.credential_manager = CredentialManager()

    def execute(self, state):
        credentials = self.credential_manager.get_credentials('UnitedHealthcare')
        command = f"""
        Navigate to https://app.dentalhub.com/
        If redirected to a login page, click the login button.
        Use the login form to enter the username and password.
        If login fails, terminate and report the error message.
        Verify successful login by checking if the URL is https://app.dentalhub.com/app/dashboard
        """
        response = self.agent_d_client.execute_command(command, credentials)
        state['login_status'] = response
        return state
```

> **File**: `agents/unitedhealthcare_login_agent.py`

### 2.5. CyberAccess Login with License Agreement Handling

Create `cyberaccess_login_agent.py`.

```python:agents/cyberaccess_login_agent.py
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager

class CyberAccessLoginAgent:
    """Agent to log into CyberAccess with license agreement handling."""

    def __init__(self):
        self.agent_d_client = AgentDClient()
        self.credential_manager = CredentialManager()

    def execute(self, state):
        credentials = self.credential_manager.get_credentials('CyberAccess')
        command = f"""
        Navigate to https://www.cyberaccessonline.net/
        Use the login form to enter the username and password.
        When prompted, read and click "I Agree" on the license agreement.
        Wait for the final loading screen to complete.
        If login fails, terminate and report the error message.
        Verify successful login by checking if the URL is https://www.cyberaccessonline.net/CyberAccess/ProviderPortal.aspx
        """
        response = self.agent_d_client.execute_command(command, credentials)
        state['login_status'] = response
        return state
```

> **File**: `agents/cyberaccess_login_agent.py`

### 2.6. Curve Dental Login

Create `curve_dental_login_agent.py`.

```python:agents/curve_dental_login_agent.py
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager

class CurveDentalLoginAgent:
    """Agent to log into Curve Dental for Comfort Dental South Independence."""

    def __init__(self):
        self.agent_d_client = AgentDClient()
        self.credential_manager = CredentialManager()

    def execute(self, state):
        credentials = self.credential_manager.get_credentials('CurveDental')
        command = f"""
        Navigate to https://comfortdentalsid.curvehero.com/#/
        Check if redirected to a login page.
        Use the login form to enter the username and password.
        If login fails, terminate and report the error message.
        Verify successful login by checking if the URL is https://comfortdentalsid.curvehero.com/#/
        """
        response = self.agent_d_client.execute_command(command, credentials)
        state['login_status'] = response
        return state
```

> **File**: `agents/curve_dental_login_agent.py`

---

## Step 3: Implement 2FA Handling via Email

For portals requiring 2FA, such as DentaQuest, we need to retrieve verification codes sent via email.

### 3.1. Implement the Gmail Client

```python:pathway/integration/gmail_client.py
import imaplib
import email
from email.header import decode_header
import os

class GmailClient:
    """Client to interact with Gmail for retrieving verification codes."""

    def __init__(self):
        self.username = os.getenv('GMAIL_USERNAME')
        self.password = os.getenv('GMAIL_PASSWORD')
        self.server = 'imap.gmail.com'

    def get_latest_verification_code(self):
        """Fetch the latest verification code from the inbox."""
        mail = imaplib.IMAP4_SSL(self.server)
        mail.login(self.username, self.password)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        for email_id in reversed(email_ids):
            res, msg = mail.fetch(email_id, "(RFC822)")
            if res != 'OK':
                continue

            email_message = email.message_from_bytes(msg[0][1])
            subject = decode_header(email_message["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            if "Your Verification Code" in subject:
                # Extract the verification code from the email body
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        verification_code = self.extract_code(body)
                        return verification_code
        return None

    def extract_code(self, body):
        """Extract the verification code from the email body."""
        # Implement the logic to extract the code, possibly using regex
        import re
        match = re.search(r'Verification Code:\s*([0-9]+)', body)
        if match:
            return match.group(1)
        return None
```

> **File**: `pathway/integration/gmail_client.py`  
> **Purpose**: Retrieves verification codes from Gmail to handle 2FA.

### 3.2. Security Considerations

- Use an **App Password** if your Gmail account has 2FA enabled.
- Ensure Gmail credentials are stored securely and not exposed.

---

## Step 4: Update the LangGraph Workflows

Create workflows for each agent using **LangGraph**.

### 4.1. Create the Workflow for DentaQuest Login

```python:workflows/dentaquest_login_workflow.py
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from agents.dentaquest_login_agent import DentaQuestLoginAgent

class DentaQuestLoginState(TypedDict):
    login_status: str
    2fa_status: str

def create_dentaquest_login_workflow():
    """Create and return a compiled DentaQuest login workflow."""
    workflow = StateGraph(DentaQuestLoginState)

    def start(state: DentaQuestLoginState) -> DentaQuestLoginState:
        return state

    def login(state: DentaQuestLoginState) -> DentaQuestLoginState:
        agent = DentaQuestLoginAgent()
        return agent.execute(state)

    def end_workflow(state: DentaQuestLoginState) -> DentaQuestLoginState:
        print("Login Status:", state.get('login_status', 'Unknown'))
        print("2FA Status:", state.get('2fa_status', 'No 2FA required'))
        return state

    workflow.add_node("start", start)
    workflow.add_node("login", login)
    workflow.add_node("end", end_workflow)

    workflow.add_edge(START, "start")
    workflow.add_edge("start", "login")
    workflow.add_edge("login", "end")
    workflow.add_edge("end", END)

    return workflow.compile()

# Create the workflow
app = create_dentaquest_login_workflow()

if __name__ == "__main__":
    app.invoke({})
```

> **File**: `workflows/dentaquest_login_workflow.py`

### 4.2. Create Workflows for Other Portals

Repeat similar steps to create workflows for each portal.

---

## Step 5: Test the Agents

### 5.1. Ensure Agent-D is Running

Make sure the Agent-D server is up and accessible.

### 5.2. Run the Workflows

Execute the workflow scripts:

```bash
python workflows/dentaquest_login_workflow.py
```

### 5.3. Verify the Output

Check the console output for login and 2FA statuses.

### 5.4. Troubleshooting

- **Connection Errors**: Ensure that Agent-D and Gmail services are reachable.
- **Credential Errors**: Verify that all credentials are correctly set in your `.env` file.
- **2FA Issues**: Ensure that the Gmail client is correctly fetching the verification codes.

---

## Conclusion

You've successfully implemented agents to automate login procedures across multiple healthcare portals, including handling 2FA via email. By leveraging **LangGraph** and **Agent-D**, you've created a scalable solution for complex web automation tasks.

---

## Appendix

### A. Updated Project Structure

```
/
├── agents/
│   ├── mohealthnet_login_agent.py
│   ├── envolve_dental_login_agent.py
│   ├── dentaquest_login_agent.py
│   ├── unitedhealthcare_login_agent.py
│   ├── cyberaccess_login_agent.py
│   └── curve_dental_login_agent.py
├── workflows/
│   ├── mohealthnet_login_workflow.py
│   ├── envolve_dental_login_workflow.py
│   ├── dentaquest_login_workflow.py
│   ├── unitedhealthcare_login_workflow.py
│   ├── cyberaccess_login_workflow.py
│   └── curve_dental_login_workflow.py
├── credentials/
│   └── credential_manager.py
├── pathway/
│   └── integration/
│       ├── agent_d_client.py
│       └── gmail_client.py
├── config/
│   └── __init__.py
├── .env.example
└── requirements.txt
```

### B. Additional Dependencies

Add the following to your `requirements.txt`:

```
langgraph
langchain
requests
python-dotenv
imaplib2  # For Gmail client
```

### C. Environment Variables Cheat Sheet

Ensure your `.env` file includes all necessary environment variables as documented in Step 1.2.

### D. Security Best Practices

- **Credentials**: Never commit your `.env` file to version control.
- **Gmail Access**: Use OAuth2 for Gmail access in production environments.
- **Error Handling**: Implement robust error handling and logging for real-world applications.

---

## Next Steps

- **Implement Remaining Tasks**: Complete workflows for all portals.
- **Enhance Error Handling**: Add more robust exception handling and retries.
- **Integrate with a Database**: Store session data and credentials securely.
- **Implement Advanced Features**: Explore automating other administrative tasks within the portals.
- **Secure the Application**: Consider integrating a secrets management system for credentials.

---

By completing **Phase 1**, you've advanced Project Pathway's capabilities significantly, moving closer to a fully automated solution for dental administrative workflows.

---