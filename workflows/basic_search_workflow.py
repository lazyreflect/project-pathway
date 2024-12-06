from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, Dict, Any
from agents.supervisor_agent import SupervisorAgent
from utils.logging_config import CustomLogger
import logging
from datetime import datetime
import uuid

class WorkflowState(TypedDict):
    """Type definition for the workflow state."""
    query: str
    search_results: str
    error: Optional[str]
    plan: Dict[str, Any]
    reasoning: str
    transaction_id: str
    timestamp: str

def create_workflow():
    """Create and return a compiled workflow."""
    workflow = StateGraph(WorkflowState)
    supervisor = SupervisorAgent()
    logger = CustomLogger("BasicSearchWorkflow")

    def start(state: WorkflowState) -> WorkflowState:
        """Initialize the workflow state."""
        transaction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        logger.log_with_metadata(
            logging.INFO,
            "Starting basic search workflow",
            metadata={
                'workflow_step': 'initialization',
                'transaction_id': transaction_id
            }
        )
        
        state['transaction_id'] = transaction_id
        state['timestamp'] = timestamp
        return state

    def execute_task(state: WorkflowState) -> WorkflowState:
        """Execute the task using SupervisorAgent."""
        logger.log_with_metadata(
            logging.INFO,
            "Executing search task",
            metadata={
                'workflow_step': 'execution',
                'transaction_id': state.get('transaction_id')
            }
        )
        
        return supervisor.execute(state)

    def end_workflow(state: WorkflowState) -> WorkflowState:
        """Process final results."""
        if state.get('error'):
            logger.log_with_metadata(
                logging.ERROR,
                f"Workflow ended with error: {state['error']}",
                metadata={
                    'workflow_step': 'completion',
                    'status': 'error',
                    'transaction_id': state.get('transaction_id')
                }
            )
            print(f"Error: {state['error']}")
        else:
            execution_time = None
            if state.get('timestamp'):
                start_time = datetime.fromisoformat(state['timestamp'])
                execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.log_with_metadata(
                logging.INFO,
                "Workflow completed successfully",
                metadata={
                    'workflow_step': 'completion',
                    'status': 'success',
                    'transaction_id': state.get('transaction_id'),
                    'execution_time_seconds': execution_time,
                    'chosen_agent': state.get('plan', {}).get('agent', 'unknown')
                }
            )
            
            print("\nTask Execution Summary:")
            print("----------------------")
            if state.get('plan'):
                print(f"Planning:")
                print(f"- Chosen Agent: {state['plan'].get('agent', 'unknown')}")
                print(f"- Reasoning: {state['plan'].get('reasoning', 'none provided')}")
                if state['plan'].get('agent') == 'self':
                    print(f"\nResponse:")
                    print(state['plan'].get('instructions', ''))
        
        return state

    # Add nodes to the workflow
    workflow.add_node("start", start)
    workflow.add_node("execute", execute_task)
    workflow.add_node("end", end_workflow)

    # Define the edges
    workflow.add_edge(START, "start")
    workflow.add_edge("start", "execute")
    workflow.add_edge("execute", "end")
    workflow.add_edge("end", END)

    return workflow.compile() 