import requests
import os
from typing import Optional

class AgentDClient:
    """Client to interact with the Agent-D API."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv('AGENT_D_BASE_URL', 'http://localhost:8000')
        self.session = requests.Session()

    def execute_command(self, command: str) -> str:
        """Send a command to Agent-D for execution."""
        url = f"{self.base_url}/execute_task"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "command": command
        }
        try:
            with self.session.post(url, headers=headers, json=payload, stream=True) as response:
                response.raise_for_status()
                result = ''
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        result += decoded_line + '\n'
                return result
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to execute command: {e}") 