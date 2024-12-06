from dotenv import load_dotenv
import argparse
import sys
import os
from workflows.basic_search_workflow import create_workflow
from utils.logging_config import setup_logging

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease create a .env file with the required variables.")
        sys.exit(1)

def main():
    # Setup logging first
    setup_logging()
    
    # Load and check environment variables
    load_dotenv()
    check_environment()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Execute tasks using the Supervisor agent with LLM planning')
    parser.add_argument('query', help='Task or query to execute')
    
    args = parser.parse_args()
    
    # Create and run the workflow
    workflow = create_workflow()
    
    # Initialize state
    initial_state = {
        "query": args.query,
        "search_results": "",
        "error": None,
        "plan": {},
        "reasoning": ""
    }
    
    # Execute workflow
    try:
        final_state = workflow.invoke(initial_state)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing workflow: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 