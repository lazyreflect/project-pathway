from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, Dict, Any
from agents.supervisor_agent import SupervisorAgent
from utils.logging_config import setup_logging
import logging
from datetime import datetime
import uuid

class WorkflowState(TypedDict):
    """Type definition for the workflow state."""
    query: str
    patient_info: Dict[str, Any]
    portal_response: str
    error: Optional[str]
    plan: Dict[str, Any]
    reasoning: str
    timestamp: Optional[str]
    agent_logs: Optional[str]

def create_workflow():
    """Create and return a compiled workflow."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    workflow = StateGraph(WorkflowState)
    supervisor = SupervisorAgent()

    def start(state: WorkflowState) -> WorkflowState:
        """Initialize the workflow state."""
        transaction_id = str(uuid.uuid4())
        logger.log_with_metadata(
            logging.INFO,
            "Workflow started",
            metadata={
                'workflow_step': 'initialization',
                'transaction_id': transaction_id
            }
        )
        
        state['timestamp'] = datetime.now().isoformat()
        state['transaction_id'] = transaction_id
        return state

    def execute_task(state: WorkflowState) -> WorkflowState:
        """Execute the task using SupervisorAgent."""
        logger.log_with_metadata(
            logging.INFO,
            "Executing task",
            metadata={
                'workflow_step': 'execution',
                'transaction_id': state.get('transaction_id')
            }
        )
        
        state = supervisor.execute(state)
        
        logger.log_with_metadata(
            logging.INFO,
            "Task executed",
            metadata={
                'workflow_step': 'completion',
                'transaction_id': state.get('transaction_id'),
                'status': 'success' if not state.get('error') else 'error'
            }
        )
        return state

    def end_workflow(state: WorkflowState) -> WorkflowState:
        """Process final results."""
        if state.get('error'):
            logger.log_with_metadata(
                logging.ERROR,
                f"Workflow ended with error: {state['error']}",
                metadata={
                    'workflow_step': 'completion',
                    'transaction_id': state.get('transaction_id'),
                    'status': 'error'
                }
            )
        else:
            logger.log_with_metadata(
                logging.INFO,
                "Workflow completed successfully",
                metadata={
                    'workflow_step': 'completion',
                    'transaction_id': state.get('transaction_id'),
                    'status': 'success',
                    'execution_time': (
                        datetime.now() - 
                        datetime.fromisoformat(state['timestamp'])
                    ).total_seconds()
                }
            )
            
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