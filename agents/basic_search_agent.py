from typing import Dict, Any
from pathway.integration.agent_d_client import AgentDClient
from utils.logging_config import CustomLogger
import logging
from datetime import datetime
import json

class BasicSearchAgent:
    """Agent that performs a basic Google search via Agent-D."""

    def __init__(self, agent_d_client: AgentDClient):
        self.logger = CustomLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        self.agent_d_client = agent_d_client
        self.logger.log_with_metadata(
            logging.DEBUG,
            "Initialized with AgentDClient",
            metadata={'workflow_step': 'initialization'}
        )

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's task."""
        # Initialize an empty list to collect results
        state['search_results'] = []
        
        def print_stream(line: str):
            try:
                # Try to parse as JSON first
                data = json.loads(line.replace('data: ', ''))
                
                # Add the streamed result to the state
                if 'message' in data:
                    state['search_results'].append(data['message'])
                    
                # Prepare metadata with all available fields
                metadata = {
                    'current_url': data.get('current_url'),
                    'container_id': data.get('container_id'),
                    'transaction_id': data.get('transaction_id'),
                    'page_title': data.get('page_title'),
                    'status_code': data.get('status_code'),
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
                    # Print the streamed result immediately
                    print(f"[{msg_type}] {data['message']}")
                    
                # Log navigation state changes separately
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
                    
            except json.JSONDecodeError:
                # If not JSON, log as plain text
                self.logger.log_with_metadata(
                    logging.INFO,
                    f"Streaming: {line}",
                    metadata={
                        'workflow_step': 'streaming',
                        'stream_data': line
                    }
                )

        try:
            query = state.get('query', '')
            self.logger.log_with_metadata(
                logging.DEBUG,
                "Executing search",
                metadata={
                    'workflow_step': 'search_start',
                    'query': query
                }
            )
            
            command = f"Navigate to google.com and search for: {query}"
            self.logger.log_with_metadata(
                logging.DEBUG,
                "Executing command",
                metadata={
                    'workflow_step': 'command_execution',
                    'command': command
                }
            )
            
            start_time = datetime.now()
            response = self.agent_d_client.execute_command(command, callback=print_stream)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.log_with_metadata(
                logging.INFO,
                "Search completed successfully",
                metadata={
                    'workflow_step': 'search_complete',
                    'execution_time_seconds': execution_time
                }
            )
            
            state['search_results'] = response
            return state
            
        except Exception as e:
            error_msg = str(e)
            state['error'] = error_msg
            self.logger.log_with_metadata(
                logging.ERROR,
                f"Error during search execution: {error_msg}",
                exc_info=True,
                metadata={
                    'workflow_step': 'error',
                    'error_type': e.__class__.__name__
                }
            )
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Can perform Google searches and return results" 