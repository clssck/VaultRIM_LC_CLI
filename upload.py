import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from auth import authenticate

# Load configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

api_info = config["api_info"]
vault_domain = api_info["vault_domain"]
api_version = api_info["api_version"]
upload_endpoint = f"{vault_domain}/api/{api_version}/services/file_staging/items"

# Function to upload file to staging server
def upload_to_staging(file_path):
    session_id = authenticate()
    m = MultipartEncoder(
        fields={
            "file": (file_path, open(file_path, 'rb'), "text/csv"),
            "kind": "file",
            "path": f"/u13063421/upload/{file_path}",
            "overwrite": "true"
        }
    )
    headers = {
        "Authorization": f"Bearer {session_id}",
        "Content-Type": m.content_type,
        "Accept": "application/json"
    }
    response = requests.post(upload_endpoint, headers=headers, data=m)
    print("Response content:", response.content)  # Debugging line to print response content
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("responseStatus") == "SUCCESS":
            print("Upload to staging successful. Response:", response_json)
            return response_json.get("data").get("name")
        else:
            print("Upload to staging failed. Response:", response_json)
            raise Exception(f"Failed to upload to staging: {response_json}")
    else:
        print("Failed to upload to staging. Response:", response.text)
        raise Exception(f"Failed to upload to staging: {response.text}")