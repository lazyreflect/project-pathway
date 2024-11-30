from typing import Dict, Any, List
from pathway.integration.agent_d_client import AgentDClient
from .basic_search_agent import BasicSearchAgent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

class SupervisorAgent:
    """Supervisor agent that uses LLM for task planning and delegation."""
    
    def __init__(self):
        # Ensure environment variables are loaded
        load_dotenv()
        
        # Check for required environment variables
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
            
        self.agent_d_client = AgentDClient()
        self.available_agents = {
            'search': BasicSearchAgent(self.agent_d_client)
        }
        
        # Initialize LLM with environment variables
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=openai_api_key
        )
        
        # Define the planning prompt
        self.planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a supervisor agent responsible for planning and delegating tasks.
Available agents and their capabilities:
- search: Can perform Google searches and return results

Analyze the user's request and determine:
1. Which agent is best suited for the task
2. How to break down complex tasks into steps
3. What specific instructions to give to the agent

Output format:
{{
    "agent": "name of the agent to use",
    "reasoning": "brief explanation of why this agent was chosen",
    "instructions": "specific instructions for the agent"
}}"""),
            ("user", "{input}")
        ])
    
    def get_available_agents(self) -> List[str]:
        """Return list of available agents."""
        return list(self.available_agents.keys())
    
    def plan_task(self, query: str) -> Dict[str, Any]:
        """Use LLM to plan the task execution."""
        chain = self.planning_prompt | self.llm
        result = chain.invoke({"input": query})
        
        try:
            # Extract the plan from the LLM response
            response_content = result.content
            # If the response is a string representation of a dict, evaluate it
            if isinstance(response_content, str):
                import ast
                plan = ast.literal_eval(response_content)
            else:
                plan = response_content
                
            return plan
        except Exception as e:
            return {
                "agent": "error",
                "reasoning": f"Failed to parse LLM response: {str(e)}",
                "instructions": ""
            }
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the task using LLM planning and appropriate agent."""
        query = state.get('query', '')
        
        # Get plan from LLM
        plan = self.plan_task(query)
        
        # Store the planning results in state
        state['plan'] = plan
        
        agent_name = plan.get('agent', '').lower()
        if agent_name not in self.available_agents:
            state['error'] = f"Unknown or unsupported agent: {agent_name}. Available agents: {self.get_available_agents()}"
            return state
        
        # Update query with specific instructions from the plan
        state['query'] = plan.get('instructions', query)
        
        # Execute the task with the chosen agent
        agent = self.available_agents[agent_name]
        result_state = agent.execute(state)
        
        # Add reasoning to the results
        result_state['reasoning'] = plan.get('reasoning', '')
        
        return result_state 