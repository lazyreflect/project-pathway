from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from agents.basic_search_agent import BasicSearchAgent
from pathway.integration.agent_d_client import AgentDClient

class SearchState(TypedDict):
    """Type definition for the search workflow state."""
    search_results: str

def create_search_workflow():
    """Create and return a compiled search workflow."""
    # Initialize the workflow
    workflow = StateGraph(SearchState)

    # Define the nodes
    def start(state: SearchState) -> SearchState:
        """Initialize the workflow state."""
        return state

    def perform_search(state: SearchState) -> SearchState:
        """Execute the search using BasicSearchAgent."""
        agent_d_client = AgentDClient()
        agent = BasicSearchAgent(agent_d_client)
        return agent.execute(state)

    def end_workflow(state: SearchState) -> SearchState:
        """Process final results."""
        print("Search Results:")
        print(state.get('search_results', 'No results found.'))
        return state

    # Add nodes to the workflow
    workflow.add_node("start", start)
    workflow.add_node("search", perform_search)
    workflow.add_node("end", end_workflow)

    # Define the edges
    workflow.add_edge(START, "start")
    workflow.add_edge("start", "search")
    workflow.add_edge("search", "end")
    workflow.add_edge("end", END)

    # Compile the workflow
    return workflow.compile() 