import os
import sys

# Add the project root to the Python path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now we can import using relative imports
from api.fhir_api import FhirApi

# Import the nodes we need
from nodes.resource_nodes import get_requested_resource, get_user_question

def main():
    # Get the singleton instance - this will automatically authenticate
    fhir_api = FhirApi()
    
    # Simulate user input
    user_input = "Show me all patients"
    
    # Get the requested resource type
    resource_type = get_requested_resource(user_input)
    
    # Make an authenticated request to a FHIR endpoint
    response = fhir_api.authenticated_request(f"{fhir_api.FHIR_API_URL}/{resource_type}")
    
    # Process the response
    if response:
        print("Successfully retrieved FHIR data:")
        patients = response.get('entry', [])
        if patients:
            for patient in patients:
                print(patient.get('resource', {}).get('name', []))
        else:
            print("No patients found")
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    main()
