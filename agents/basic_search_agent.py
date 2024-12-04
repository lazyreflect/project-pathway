from typing import Dict, Any
import logging
from pathway.integration.agent_d_client import AgentDClient

class BasicSearchAgent:
    """Agent that performs a basic Google search via Agent-D."""

    def __init__(self, agent_d_client: AgentDClient):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        self.agent_d_client = agent_d_client
        self.logger.debug("Initialized with AgentDClient")

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's task."""
        def print_stream(line: str):
            self.logger.info(f"Streaming: {line}")

        try:
            query = state.get('query', '')
            self.logger.debug(f"Executing search with query: {query}")
            
            command = f"Navigate to google.com and search for: {query}"
            self.logger.debug(f"Executing command: {command}")
            
            response = self.agent_d_client.execute_command(command, callback=print_stream)
            self.logger.info("Search completed successfully")
            
            state['search_results'] = response
            return state
        except Exception as e:
            error_msg = str(e)
            state['error'] = error_msg
            self.logger.error(f"Error during search execution: {error_msg}")
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Can perform Google searches and return results" 