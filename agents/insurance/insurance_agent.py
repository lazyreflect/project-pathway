import logging
from typing import Dict, Any
from agents.insurance.medicaid.medicaid_specialist_agent import MedicaidSpecialistAgent
from utils.logging_config import CustomLogger

class InsuranceAgent:
    """Agent that handles insurance-related tasks."""

    def __init__(self):
        self.logger = CustomLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        self.specialists = {
            'medicaid': MedicaidSpecialistAgent()
        }
        self.logger.log_with_metadata(
            logging.DEBUG,
            "Initialized specialists",
            metadata={'specialists': list(self.specialists.keys())}
        )

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate the task to the appropriate specialist agent."""
        self.logger.log_with_metadata(
            logging.INFO,
            "Insurance Agent Processing",
            metadata={'workflow_step': 'processing_start'}
        )
        
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
            
            # Log masked patient information
            masked_info = {
                k: '[REDACTED]' if k in ['first_name', 'last_name', 'dob'] else v
                for k, v in state['patient_info'].items()
            }
            self.logger.log_with_metadata(
                logging.INFO,
                "Parsed Patient Information",
                metadata={'patient_info': masked_info}
            )
        
        insurance_type = state.get('insurance_type', 'medicaid').lower()
        self.logger.log_with_metadata(
            logging.DEBUG,
            f"Selected insurance type: {insurance_type}",
            metadata={'insurance_type': insurance_type}
        )

        if insurance_type in self.specialists:
            specialist = self.specialists[insurance_type]
            self.logger.log_with_metadata(
                logging.INFO,
                f"Delegating to {insurance_type} specialist",
                metadata={'workflow_step': 'delegation'}
            )
            return specialist.execute(state)
        else:
            error_msg = f"Unknown insurance type: {insurance_type}"
            state['error'] = error_msg
            self.logger.log_with_metadata(
                logging.ERROR,
                error_msg,
                metadata={
                    'workflow_step': 'error',
                    'error_type': 'unknown_insurance_type',
                    'available_types': list(self.specialists.keys())
                }
            )
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Handles insurance tasks and delegates to appropriate specialists" 