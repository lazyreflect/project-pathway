import logging
from typing import Dict, Any
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager

class MoHealthNetAgent:
    """Agent that interacts with the MoHealthNet (eMOMED) portal."""

    def __init__(self):
        self.agent_d_client = AgentDClient()
        self.credentials_manager = CredentialManager()

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the task of accessing the eMOMED portal."""
        def print_stream(line: str):
            logging.info(line)
            
        try:
            credentials = self.credentials_manager.get_credentials('EMOMED')
            # Securely set credentials in Agent-D
            self.agent_d_client.set_credentials(credentials['username'], credentials['password'])

            patient_info = state.get('patient_info', {})
            logging.info(f"Patient info: {patient_info}")

            # Note this command is condensed for testing purposes. This would be the first portion of the full command.
            command = f"""
            1. Navigate to https://www.emomed.com/portal/wps/myportal
            2. Check if need to login by checking the URL. If the URL contains login, you are not logged in.
            3. If you are not logged in, use the enter secrets tool to log in.
            4. If login fails, terminate and report the error message.
            5. Verify successful login by confirming the URL is emomed.com/portal/wps/myportal
            """

            # This command is the original full command for the agent that we want to break down into smaller steps.
            # command = f"""
            # 1. Navigate to https://www.emomed.com/portal/wps/myportal
            # 2. Check if need to login by checking the URL. If the URL contains login, you are not logged in.
            # 3. If you are not logged in, use the enter secrets tool to log in.
            # 4. If login fails, terminate and report the error message.
            # 5. Verify successful login by confirming the URL is emomed.com/portal/wps/myportal
            # 6. Navigate to 'Participant Eligibility' section.
            # 7. Enter the patient's information:
            # - First Name: {patient_info.get('first_name')}
            # - Last Name: {patient_info.get('last_name')}
            # - Date of Birth: {patient_info.get('dob')}
            # 8. Retrieve and report the following information:
            # - DCN Number
            # - Benefits/Coverage Details
            # - Primary Insurance Information
            # 9. If primary insurance is detected, flag for human verification.
            # """

            response = self.agent_d_client.execute_command(command, callback=print_stream)
            state['portal_response'] = response
            return state
        except Exception as e:
            state['error'] = str(e)
            logging.error(f"Error: {str(e)}")
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Interacts with MoHealthNet portal to perform eligibility verification" 