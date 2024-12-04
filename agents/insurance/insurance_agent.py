from typing import Dict, Any
from agents.insurance.medicaid.medicaid_specialist_agent import MedicaidSpecialistAgent

class InsuranceAgent:
    """Agent that handles insurance-related tasks."""

    def __init__(self):
        self.specialists = {
            'medicaid': MedicaidSpecialistAgent()
            # You can add more specialists here (e.g., 'private_insurance': PrivateInsuranceAgent())
        }

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate the task to the appropriate specialist agent."""
        print(f"Streaming: data: {{\"message\": \"InsuranceAgent processing request\", \"type\": \"info\"}}", flush=True)
        
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
            print(f"Streaming: data: {{\"message\": \"Parsed patient info: {state['patient_info']}\", \"type\": \"info\"}}", flush=True)
        
        insurance_type = state.get('insurance_type', 'medicaid').lower()
        if insurance_type in self.specialists:
            specialist = self.specialists[insurance_type]
            return specialist.execute(state)
        else:
            error_msg = f"Unknown insurance type: {insurance_type}"
            state['error'] = error_msg
            print(f"Streaming: data: {{\"message\": \"Error: {error_msg}\", \"type\": \"error\"}}", flush=True)
            return state

    def get_capabilities(self) -> str:
        """Return a description of the agent's capabilities."""
        return "Handles insurance tasks and delegates to appropriate specialists" 