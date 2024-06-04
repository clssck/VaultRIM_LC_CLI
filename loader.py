import json
import requests
from auth import authenticate

# Load configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

api_info = config["api_info"]
vault_domain = api_info["vault_domain"]
api_version = api_info["api_version"]
loader_endpoint = f"{vault_domain}/api/{api_version}/services/loader/load"

# Function to create loader job
def create_loader_job(file_name, object_type):
    session_id = authenticate()
    headers = {
        "Authorization": f"Bearer {session_id}",
        "Content-Type": "application/json"
    }
    payload = [
        {
            "object_type": "vobjects__v",
            "object": object_type,
            "action": "update",
            "file": f"/u13063421/upload/{file_name}",
            "recordmigrationmode": True,
            "order": 1
        }
    ]
    response = requests.post(loader_endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("responseStatus") == "SUCCESS":
            print("Loader job created successfully. Response:", response_json)
        else:
            print("Failed to create loader job. Response:", response_json)
            raise Exception(f"Failed to create loader job: {response_json}")
    else:
        raise Exception(f"Failed to create loader job: {response.text}")