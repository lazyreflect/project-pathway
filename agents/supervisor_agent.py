from typing import Dict, Any, List
from pathway.integration.agent_d_client import AgentDClient
from .basic_search_agent import BasicSearchAgent
from .insurance.insurance_agent import InsuranceAgent
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
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. Please check your .env file.")

        self.agent_d_client = AgentDClient()
        self.available_agents = {
            'search': BasicSearchAgent(self.agent_d_client),
            'insurance': InsuranceAgent()
        }

        # Initialize LLM with environment variables
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=openai_api_key
        )

        # Create the agents capability string dynamically
        agents_capabilities = "\n".join([f"- {name}: {agent.get_capabilities()}" for name, agent in self.available_agents.items()])
        agents_list = "\n".join([f"- {name}" for name in self.available_agents.keys()])

        # Define the planning prompt
        self.planning_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a supervisor agent responsible for planning and delegating tasks.
Available agents and their capabilities:
{agents_capabilities}

When the user asks about available agents or capabilities, respond with:
{{{{
    "agent": "self",
    "reasoning": "Providing information about available agents",
    "instructions": "Here are the available agents and their capabilities:\\n{agents_capabilities}"
}}}}

For all other requests, analyze the user's request and determine:
1. Which agent is best suited for the task
2. How to break down complex tasks into steps
3. What specific instructions to give to the agent

Output format:
{{{{
    "agent": "name of the agent to use or 'self' if you will handle it directly",
    "reasoning": "brief explanation of why this agent was chosen",
    "instructions": "specific instructions for the agent or your response to the user"
}}}}\n"""),
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
                "agent": "self",
                "reasoning": "Error occurred during planning, handling directly",
                "instructions": (
                    "I apologize, but I encountered an error while processing your request. "
                    "Here are the available agents and their capabilities:\n"
                    "- search: Can perform Google searches and return results\n"
                    "- insurance: Handles insurance-related tasks and delegates to specialist agents"
                )
            }

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the task using LLM planning and appropriate agent."""
        query = state.get('query', '')

        # Get plan from LLM
        plan = self.plan_task(query)

        # Store the planning results in state
        state['plan'] = plan

        agent_name = plan.get('agent', '').lower()
        if agent_name == 'self':
            # Supervisor handles the response directly
            state['response'] = plan.get('instructions', '')
            return state
        elif agent_name in self.available_agents:
            # Delegate to the chosen agent
            state['query'] = plan.get('instructions', query)
            agent = self.available_agents[agent_name]
            result_state = agent.execute(state)
            result_state['reasoning'] = plan.get('reasoning', '')
            return result_state
        else:
            state['error'] = (
                f"Unknown or unsupported agent: {agent_name}. "
                f"Available agents: {self.get_available_agents()}"
            )
            return state
