from typing import Dict, Any
from agents.insurance.medicaid.portals.mohealthnet_agent import MoHealthNetAgent

class MedicaidSpecialistAgent:
    """Agent specializing in Medicaid-related tasks."""

    def __init__(self):
        self.portal_agents = {
            'mohealthnet': MoHealthNetAgent()
            # You can add more portal agents if needed
        }

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate the task to the appropriate portal agent."""
        print(f"Streaming: data: {{\"message\": \"MedicaidSpecialistAgent processing request\", \"type\": \"info\"}}", flush=True)
        
        portal_name = state.get('portal_name', 'mohealthnet').lower()
        if portal_name in self.portal_agents:
            portal_agent = self.portal_agents[portal_name]
            return portal_agent.execute(state)
        else:
            error_msg = f"Unknown portal: {portal_name}"
            state['error'] = error_msg
            print(f"Streaming: data: {{\"message\": \"Error: {error_msg}\", \"type\": \"error\"}}", flush=True)
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Handles Medicaid tasks and delegates to portal agents" 