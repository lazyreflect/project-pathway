import logging
from typing import Dict, Any
from agents.insurance.medicaid.medicaid_specialist_agent import MedicaidSpecialistAgent

class InsuranceAgent:
    """Agent that handles insurance-related tasks."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        self.specialists = {
            'medicaid': MedicaidSpecialistAgent()
            # You can add more specialists here (e.g., 'private_insurance': PrivateInsuranceAgent())
        }
        self.logger.debug(f"Initialized specialists: {list(self.specialists.keys())}")

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate the task to the appropriate specialist agent."""
        self.logger.info("-" * 50)
        self.logger.info("Insurance Agent Processing")
        self.logger.info("-" * 50)
        
        # Parse patient info from the query
        query = state.get('query', '')
        
        # Basic parsing - you might want to make this more robust
        if "DOB:" in query:
            name_part = query.split("DOB:")[0].strip()
            dob_part = query.split("DOB:")[1].strip()
            state['patient_info'] = {
                'first_name': name_part.split()[0],
                'last_name': name_part.split()[-1],
                'dob': dob_part
            }
            self.logger.info("Parsed Patient Information:")
            for key, value in state['patient_info'].items():
                self.logger.info(f"  {key.replace('_', ' ').title()}: {value}")
        
        insurance_type = state.get('insurance_type', 'medicaid').lower()
        self.logger.debug(f"Selected insurance type: {insurance_type}")

        if insurance_type in self.specialists:
            specialist = self.specialists[insurance_type]
            self.logger.info(f"Delegating to {insurance_type} specialist")
            return specialist.execute(state)
        else:
            error_msg = f"Unknown insurance type: {insurance_type}"
            state['error'] = error_msg
            self.logger.error(error_msg)
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Handles insurance tasks and delegates to appropriate specialists" 