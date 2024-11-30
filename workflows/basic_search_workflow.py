from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, Dict, Any
from agents.supervisor_agent import SupervisorAgent

class WorkflowState(TypedDict):
    """Type definition for the workflow state."""
    query: str
    search_results: str
    error: Optional[str]
    plan: Dict[str, Any]
    reasoning: str

def create_workflow():
    """Create and return a compiled workflow."""
    workflow = StateGraph(WorkflowState)
    supervisor = SupervisorAgent()

    def start(state: WorkflowState) -> WorkflowState:
        """Initialize the workflow state."""
        return state

    def execute_task(state: WorkflowState) -> WorkflowState:
        """Execute the task using SupervisorAgent."""
        return supervisor.execute(state)

    def end_workflow(state: WorkflowState) -> WorkflowState:
        """Process final results."""
        if state.get('error'):
            print(f"Error: {state['error']}")
            return state
            
        print("\nTask Execution Summary:")
        print("----------------------")
        if state.get('plan'):
            print(f"Planning:")
            print(f"- Chosen Agent: {state['plan'].get('agent', 'unknown')}")
            print(f"- Reasoning: {state['plan'].get('reasoning', 'none provided')}")
            
        if state.get('search_results'):
            print("\nResults:")
            print(state['search_results'])
            
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