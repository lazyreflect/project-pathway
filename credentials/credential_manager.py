import os
from typing import Dict

class CredentialManager:
    """Handles retrieval of credentials from environment variables."""
    
    def get_credentials(self, portal_name: str) -> Dict[str, str]:
        """Get credentials for a specific portal from environment variables."""
        username = os.getenv(f'{portal_name.upper()}_USERNAME')
        password = os.getenv(f'{portal_name.upper()}_PASSWORD')

        if not username or not password:
            raise ValueError(f"Missing credentials for {portal_name}")

        return {
            'username': username,
            'password': password
        } 