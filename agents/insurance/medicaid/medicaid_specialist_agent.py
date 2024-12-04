import logging
from typing import Dict, Any
from agents.insurance.medicaid.portals.mohealthnet_agent import MoHealthNetAgent

class MedicaidSpecialistAgent:
    """Agent specializing in Medicaid-related tasks."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        self.portal_agents = {
            'mohealthnet': MoHealthNetAgent()
            # You can add more portal agents if needed
        }
        self.logger.debug(f"Initialized portal agents: {list(self.portal_agents.keys())}")

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate the task to the appropriate portal agent."""
        self.logger.info("MedicaidSpecialistAgent processing request")
        
        portal_name = state.get('portal_name', 'mohealthnet').lower()
        self.logger.debug(f"Selected portal: {portal_name}")

        if portal_name in self.portal_agents:
            portal_agent = self.portal_agents[portal_name]
            self.logger.info(f"Delegating to {portal_name} portal agent")
            return portal_agent.execute(state)
        else:
            error_msg = f"Unknown portal: {portal_name}"
            state['error'] = error_msg
            self.logger.error(error_msg)
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Handles Medicaid tasks and delegates to portal agents" 