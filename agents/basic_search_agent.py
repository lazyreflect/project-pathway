from typing import Dict, Any
from pathway.integration.agent_d_client import AgentDClient

class BasicSearchAgent:
    """Agent that performs a basic Google search via Agent-D."""

    def __init__(self, agent_d_client: AgentDClient):
        self.agent_d_client = agent_d_client

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's task."""
        def print_stream(line: str):
            print(f"Streaming: {line}", flush=True)

        query = state.get('query', '')
        command = f"Navigate to google.com and search for: {query}"
        response = self.agent_d_client.execute_command(command, callback=print_stream)
        state['search_results'] = response
        return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Can perform Google searches and return results" 