from typing import Dict, Any
from pathway.integration.agent_d_client import AgentDClient

class BasicSearchAgent:
    """Agent that performs a basic Google search via Agent-D."""

    def __init__(self, agent_d_client: AgentDClient):
        self.agent_d_client = agent_d_client

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's task."""
        command = "Navigate to google.com and search for the latest weather in Kansas City."
        response = self.agent_d_client.execute_command(command)
        state['search_results'] = response
        return state 