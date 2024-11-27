from dotenv import load_dotenv
from workflows.basic_search_workflow import create_search_workflow

def main():
    # Load environment variables
    load_dotenv()
    
    # Create and run the workflow
    workflow = create_search_workflow()
    
    # Initialize state
    initial_state = {"search_results": ""}
    
    # Execute workflow
    try:
        final_state = workflow.invoke(initial_state)
        print("Workflow completed successfully!")
    except Exception as e:
        print(f"Error executing workflow: {e}")

if __name__ == "__main__":
    main() 