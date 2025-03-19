import requests
import os
import sys

# Add the project root to the Python path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Use relative import
from constants.fhir_api import FHIR_API_URL

class FhirApi:
    # Add FHIR_API_URL as a class attribute for easier access
    FHIR_API_URL = FHIR_API_URL
    """
    API client for interacting with FHIR servers
    Implemented as a singleton
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FhirApi, cls).__new__(cls)
            cls._instance.jwt = None
            cls._instance._login()
        return cls._instance
    
    def __init__(self):
        # Initialization happens in __new__
        pass
    
    def _login(self):
        """
        Authenticate with the FHIR server and get JWT token
        """
        # FIXME: This is only a POC implementation. 
        # Authentication details should be configurable and not hardcoded.
        login_url = f'{FHIR_API_URL}/login'
        login_payload = {
            "username": "admin@heliossoftware.com",
            "password": "admin"
        }
        
        try:
            # Get authentication token
            login_response = requests.post(login_url, json=login_payload)
            login_response.raise_for_status()
            
            # Extract JWT from response
            response_data = login_response.json()
            self.jwt = response_data.get('jwt')
            
            if not self.jwt:
                print("Authentication successful but no JWT token received")
        except requests.exceptions.RequestException as e:
            print(f"Error during authentication: {e}")
    
    def authenticated_request(self, url):
        """
        Makes an authenticated request to the specified FHIR endpoint
        
        Args:
            url (str): The URL to call with authentication
            
        Returns:
            dict: The JSON response from the FHIR server
        """
        try:
            if not self.jwt:
                self._login()
                
            if not self.jwt:
                raise ValueError("Failed to obtain authentication token")
                
            # Make authenticated request to the provided URL
            headers = {
                'Authorization': f'Bearer {self.jwt}'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None
