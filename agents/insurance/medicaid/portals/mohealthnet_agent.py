import logging
from typing import Dict, Any
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager
import json

class MoHealthNetAgent:
    """Agent that interacts with the MoHealthNet (eMOMED) portal."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        self.agent_d_client = AgentDClient()
        self.credentials_manager = CredentialManager()
        self.logger.debug("Initialized AgentDClient and CredentialManager")

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the task of accessing the eMOMED portal."""
        def print_stream(line: str):
            try:
                data = json.loads(line.replace('data: ', ''))
                
                # Log message with type if present
                if 'message' in data:
                    msg_type = data.get('type', 'info').upper()
                    self.logger.info(f"[{msg_type}] {data['message']}")
                
                # Log metadata fields
                metadata = {
                    'current_url': data.get('current_url'),
                    'container_id': data.get('container_id'),
                    'transaction_id': data.get('transaction_id'),
                    'request_originator': data.get('request_originator'),
                    'page_title': data.get('page_title'),  # New field to track
                    'status_code': data.get('status_code'),  # HTTP status codes
                    'error': data.get('error'),  # Any error messages
                    'warnings': data.get('warnings'),  # Any warning messages
                    'element_state': data.get('element_state'),  # State of UI elements
                    'navigation_state': data.get('navigation_state'),  # Navigation status
                    'form_data': data.get('form_data'),  # Form field values
                    'response_headers': data.get('response_headers')  # HTTP headers
                }
                
                # Log any non-None metadata
                metadata_str = "\n".join(
                    f"  {key}: {value}" 
                    for key, value in metadata.items() 
                    if value is not None
                )
                if metadata_str:
                    self.logger.info("Metadata:")
                    self.logger.info(metadata_str)
                
            except json.JSONDecodeError:
                self.logger.info(line)
        
        try:
            self.logger.info("-" * 50)
            self.logger.info("Starting eMOMED Portal Access")
            self.logger.info("-" * 50)
            
            self.logger.info("Retrieving EMOMED credentials")
            credentials = self.credentials_manager.get_credentials('EMOMED')
            
            # Securely set credentials in Agent-D
            self.logger.debug("Setting credentials in Agent-D")
            self.agent_d_client.set_credentials(credentials['username'], credentials['password'])

            patient_info = state.get('patient_info', {})
            if patient_info:
                self.logger.info("Patient Information:")
                for key, value in patient_info.items():
                    self.logger.info(f"  {key.replace('_', ' ').title()}: {value}")
            else:
                self.logger.warning("No patient information provided")

            command = f"""
            1. Navigate to https://www.emomed.com/portal/wps/myportal
            2. Check if need to login by checking the URL. If the URL contains login, you are not logged in.
            3. If you are not logged in, use the enter secrets tool to log in.
            4. If login fails, terminate and report the error message.
            5. Verify successful login by confirming the URL is emomed.com/portal/wps/myportal
            """
            self.logger.debug(f"Executing command: {command}")

            response = self.agent_d_client.execute_command(command, callback=print_stream)
            self.logger.info("Command execution completed")
            
            state['portal_response'] = response
            return state
        except Exception as e:
            error_msg = str(e)
            state['error'] = error_msg
            self.logger.error(f"Error during execution: {error_msg}")
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Interacts with MoHealthNet portal to perform eligibility verification" 