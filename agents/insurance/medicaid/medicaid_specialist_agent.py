import logging
from typing import Dict, Any
from agents.insurance.medicaid.portals.mohealthnet_agent import MoHealthNetAgent
from utils.logging_config import CustomLogger

class MedicaidSpecialistAgent:
    """Agent specializing in Medicaid-related tasks."""

    def __init__(self):
        self.logger = CustomLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        self.portal_agents = {
            'mohealthnet': MoHealthNetAgent()
        }
        self.logger.log_with_metadata(
            logging.DEBUG,
            "Initialized portal agents",
            metadata={'portal_agents': list(self.portal_agents.keys())}
        )

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate the task to the appropriate portal agent."""
        self.logger.log_with_metadata(
            logging.INFO,
            "MedicaidSpecialistAgent processing request",
            metadata={'workflow_step': 'processing_start'}
        )
        
        portal_name = state.get('portal_name', 'mohealthnet').lower()
        self.logger.log_with_metadata(
            logging.DEBUG,
            f"Selected portal: {portal_name}",
            metadata={'portal_name': portal_name}
        )

        if portal_name in self.portal_agents:
            portal_agent = self.portal_agents[portal_name]
            self.logger.log_with_metadata(
                logging.INFO,
                f"Delegating to {portal_name} portal agent",
                metadata={'workflow_step': 'delegation'}
            )
            return portal_agent.execute(state)
        else:
            error_msg = f"Unknown portal: {portal_name}"
            state['error'] = error_msg
            self.logger.log_with_metadata(
                logging.ERROR,
                error_msg,
                metadata={
                    'workflow_step': 'error',
                    'error_type': 'unknown_portal',
                    'available_portals': list(self.portal_agents.keys())
                }
            )
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Handles Medicaid tasks and delegates to portal agents" 