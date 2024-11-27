# Agent-D API Integration Guide

Agent-D provides a FastAPI wrapper, allowing you to send commands via HTTP and receive streaming results. This guide covers the available API endpoints, configuration options, and best practices for using the Agent-D API.

## API Endpoints

### Execute Task

Send POST requests to execute tasks. For example, to execute a task using cURL:

```bash
curl --location 'http://127.0.0.1:8000/execute_task' \
--header 'Content-Type: application/json' \
--data '{
    "command": "go to espn, look for soccer news, report the names of the most recent soccer champs",
    "llm_config": {"planner_agent": {...}, "browser_nav_agent": {...}},
    "planner_max_chat_round": 50,
    "browser_nav_max_chat_round": 10,
    "clientid": "optional-client-id",
    "request_originator": "optional-request-originator"
}'
```

- **command**: The command related to web navigation to execute.
- **llm_config**: Optional. Configuration for planner and browser navigation agents.
- **planner_max_chat_round**: Optional. Maximum chat rounds for the planner agent (default: 50).
- **browser_nav_max_chat_round**: Optional. Maximum chat rounds for the browser navigation agent (default: 10).
- **clientid**: Optional. Client identifier.
- **request_originator**: Optional. ID of the request originator.

### Set Credentials

Before executing tasks that require authentication, you must set credentials using the secure API endpoint:

```http
POST /api/set_credentials
Content-Type: application/json
```

Request body:
```json
{
    "username": "your_username",
    "password": "your_password",
    "client_secret": "your-api-client-secret"
}
```

- **username**: The username credential.
- **password**: The password credential.
- **client_secret**: Required. Client secret for authentication.

## LLM Configuration

Agent-D supports multiple LLM providers and models through a flexible configuration system. The API accepts custom LLM configurations for both the planner and browser navigation agents.

### Supported LLM Providers

1. **OpenAI**
   - Suggested Models: GPT-4o, GPT-4-Turbo
   - Requires OpenAI API key

2. **Anthropic**
   - Suggested Models: Claude-3-Opus, Claude-3-Sonnet, Claude-3-Haiku
   - Requires Anthropic API key

3. **Mistral**
   - Suggested Models: Mistral-Large, Mistral-Medium, Mistral-Small
   - Requires Mistral API key and base URL

4. **Llama (via Groq)**
   - Suggested Models: Llama-3.1-70b-versatile
   - Requires Groq API key

### Configuration Structure

The LLM configuration can be provided in the API request body using the following structure:

```json
{
    "command": "your automation command",
    "llm_config": {
        "planner_agent": {
            "model_name": "string",
            "model_api_key": "string",
            "model_base_url": "string",
            "model_api_type": "string",
            "system_prompt": "string",
            "llm_config_params": {
                "temperature": number,
                "top_p": number,
                "cache_seed": null,
                "seed": number
            }
        },
        "browser_nav_agent": {
            // Same structure as planner_agent
        }
    }
}
```

### Example Configurations

1. **OpenAI GPT-4**
```json
{
    "command": "1. Navigate to the URL https://comfortdentalsid.curvehero.com/#/. 2. Check if redirected to a login page. 3. If on a login page, use the enter secret credentials tool to input the username and password. 4. Verify successful login or capture any error message if login fails.",
    "llm_config": {
        "planner_agent": {
            "model_name": "gpt-4",
            "model_api_key": "sk-...",
            "model_base_url": "https://...",
            "system_prompt": "You are a web automation task planner....",
            "llm_config_params": {
                "temperature": 0.0,
                "top_p": 0.001,
                "seed": 12345
            }
        },
        "browser_nav_agent": {
            "model_name": "gpt-4",
            "model_api_key": "sk-...",
            "model_base_url": "https://...",
            "system_prompt": "You will perform web navigation tasks with the functions that you have...\nOnce a task is completed, confirm completion with ##TERMINATE TASK##.",
            "llm_config_params": {
                "temperature": 0.0,
                "top_p": 0.001,
                "seed": 12345
            }
        }
    }
}
```

## Secure Credential Management

Agent-D provides a secure mechanism for handling automated logins through its credential management system. This is particularly useful for automating tasks that require authentication.

### How Credential Management Works

1. **Storage**: 
   - Credentials are stored securely in environment variables within the server's process memory.
   - Not written to disk or persistent storage.
   - Isolated to the specific server instance.
   - Cleared when the server restarts.

2. **Usage Flow**:
   - When a task requires authentication, the browser navigation agent automatically:
     1. Detects login forms.
     2. Retrieves credentials from environment variables.
     3. Fills in appropriate fields.
     4. Handles form submission.
     - All without exposing credentials in logs or responses.

3. **Security Features**:
   - Client authentication using constant-time comparison.
   - Credentials never included in error messages or logs.
   - Environment variable storage prevents credential exposure in crash dumps.
   - Automatic credential clearing on server restart.

### Limitations

1. **Session Management**:
   - Credentials are valid only for the current server instance.
   - Must be reset after server restarts.
   - No persistent storage of credentials.

2. **Concurrent Usage**:
   - Single set of credentials per server instance.
   - Credentials may need to be reset before giving a command that requires navigating to different sites.

3. **Authentication Methods**:
   - Currently supports basic username/password authentication.
   - No support for:
     - Multi-factor authentication
     - OAuth flows
     - SSO systems
     - Biometric authentication

## Best Practices

1. **Model Selection**
   - Use GPT-4 or Claude-3-Opus for complex navigation tasks.
   - Consider Mistral or Llama for simpler tasks to optimize costs.
   - Test different models to find the best balance for your use case.

2. **Parameter Tuning**
   - Lower temperature (0.0-0.1) for consistent results.
   - Higher temperature (0.2-0.7) for more creative problem-solving.
   - Use seed values for reproducible results.

3. **System Prompts**
   - Keep default system prompts unless you have specific requirements.
   - Custom system prompts should maintain task completion signals (e.g., ##TERMINATE TASK##).
   - Avoid overly complex prompts that might confuse the model.

4. **API Keys**
   - Store API keys securely.
   - Use environment variables when possible.
   - Rotate keys regularly following security best practices.

5. **Environment Configuration**
   - Set environment variables like `API_CLIENT_SECRET`, `HOST`, `PORT`, and `CONTAINER_ID` for proper application configuration.
   - Ensure these variables are securely managed and not exposed in logs or error messages.

This guide should provide a comprehensive overview of the Agent-D API, its features, and best practices for integration and usage.