import logging
from typing import Dict, Any
from pathway.integration.agent_d_client import AgentDClient
from credentials.credential_manager import CredentialManager
import json
from datetime import datetime

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
                
                # Prepare metadata with all available fields
                metadata = {
                    'current_url': data.get('current_url'),
                    'container_id': data.get('container_id'),
                    'transaction_id': data.get('transaction_id'),
                    'request_originator': data.get('request_originator'),
                    'page_title': data.get('page_title'),
                    'status_code': data.get('status_code'),
                    'error': data.get('error'),
                    'warnings': data.get('warnings'),
                    'element_state': data.get('element_state'),
                    'navigation_state': data.get('navigation_state'),
                    'form_data': data.get('form_data'),
                    'response_headers': data.get('response_headers'),
                    'workflow_step': 'stream_processing'
                }
                
                # Log message with type if present
                if 'message' in data:
                    msg_type = data.get('type', 'info').upper()
                    self.logger.log_with_metadata(
                        logging.INFO,
                        f"[{msg_type}] {data['message']}",
                        metadata=metadata
                    )
                    
                    # Log navigation state changes separately for better visibility
                    if data.get('current_url'):
                        self.logger.log_with_metadata(
                            logging.INFO,
                            f"Navigation update",
                            metadata={
                                'current_url': data['current_url'],
                                'page_title': data.get('page_title'),
                                'workflow_step': 'navigation'
                            }
                        )
                
            except json.JSONDecodeError as e:
                self.logger.log_with_metadata(
                    logging.WARNING,
                    f"Failed to parse JSON response: {line}",
                    metadata={
                        'error': str(e),
                        'raw_data': line,
                        'workflow_step': 'error_parsing'
                    }
                )
        
        try:
            self.logger.log_with_metadata(
                logging.INFO,
                "Starting eMOMED Portal Access",
                metadata={'workflow_step': 'initialization'}
            )
            
            self.logger.log_with_metadata(
                logging.INFO,
                "Retrieving EMOMED credentials",
                metadata={'workflow_step': 'credentials'}
            )
            
            credentials = self.credentials_manager.get_credentials('EMOMED')
            
            # Securely set credentials in Agent-D
            self.logger.log_with_metadata(
                logging.DEBUG,
                "Setting credentials in Agent-D",
                metadata={'workflow_step': 'authentication'}
            )
            
            self.agent_d_client.set_credentials(credentials['username'], credentials['password'])

            patient_info = state.get('patient_info', {})
            if patient_info:
                # Mask sensitive information in logs
                masked_info = {
                    k: '[REDACTED]' if k in ['first_name', 'last_name', 'dob'] else v
                    for k, v in patient_info.items()
                }
                self.logger.log_with_metadata(
                    logging.INFO,
                    "Processing patient information",
                    metadata={'patient_info': masked_info}
                )
            else:
                self.logger.log_with_metadata(
                    logging.WARNING,
                    "No patient information provided",
                    metadata={'workflow_step': 'validation'}
                )

            command = f"""
            1. Navigate to https://www.emomed.com/portal/wps/myportal
            2. Check if need to login by checking the URL. If the URL contains login, you are not logged in.
            3. If you are not logged in, use the enter secrets tool to log in.
            4. If login fails, terminate and report the error message.
            5. Verify successful login by confirming the URL is emomed.com/portal/wps/myportal
            """
            
            self.logger.log_with_metadata(
                logging.DEBUG,
                "Executing command",
                metadata={
                    'workflow_step': 'portal_access',
                    'command': command
                }
            )

            start_time = datetime.now()
            response = self.agent_d_client.execute_command(command, callback=print_stream)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.log_with_metadata(
                logging.INFO,
                "Command execution completed",
                metadata={
                    'workflow_step': 'completion',
                    'execution_time_seconds': execution_time
                }
            )
            
            state['portal_response'] = response
            return state
            
        except Exception as e:
            error_msg = str(e)
            state['error'] = error_msg
            self.logger.log_with_metadata(
                logging.ERROR,
                f"Error during execution: {error_msg}",
                exc_info=True,
                metadata={
                    'workflow_step': 'error',
                    'error_type': e.__class__.__name__
                }
            )
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Interacts with MoHealthNet portal to perform eligibility verification" 