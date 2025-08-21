import requests
import json
import getpass

def authenticate(session, env_info, user_info):
    response = session.post(f"{env_info['BASE_URL']}/api/auth/login", json=user_info)
    if response.status_code == 204:
        print("Authentication successful.")
        return response.headers.get('X-MSTR-AuthToken')
    else:
        print("Authentication failed:", response.json())
        return None

# Define environment information
env_info = {
    'BASE_URL': 'http://localhost:8080/MicroStrategyLibrary',  # Replace with your Strategy server URL
}

# Define user information
user_info = {
    'loginMode': 1,  # This can vary based on your authentication method
    'username': 'administrator',  # Replace with your username
    'password': getpass.getpass(prompt='Password Source ')  # Replace with your password
}

# Create a session
session = requests.Session()

# Authenticate
x_mstr_auth_token = authenticate(session, env_info, user_info)

# Use the token for subsequent requests
headers = {
    'X-MSTR-AuthToken': x_mstr_auth_token,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-MSTR-ProjectID': 'B19DEDCC11D4E0EFC000EB9495D0F44F'  # Replace with your project ID
}

# Load your JSON payload from a local file
with open('C:\\Users\\ajaym\\Desktop\\mstr-rest-api\\ffsqljason.json', 'r') as file:
    json_payload = json.load(file)

# Create the report using the JSON payload
create_report_url = f"{env_info['BASE_URL']}/api/model/reports?showExpressionAs=tree&showAdvancedProperties=true"
response = session.post(create_report_url, headers=headers, json=json_payload)

if response.status_code == 201:
    print("Report created successfully:", response.json())

    report_id = response.json().get('information', {}).get('objectId')
    print("Report ID:", report_id)

    instance_id = response.headers.get('X-MSTR-MS-Instance')
    print("Instance ID:", instance_id)

    save_report_url = f"{env_info['BASE_URL']}/api/model/reports/{report_id}/instances/save"

    # Build save headers with required tokens
    save_headers = {
        'X-MSTR-AuthToken': headers['X-MSTR-AuthToken'],
        'X-MSTR-MS-Instance': instance_id,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    save_payload = {
        "promptOptions": {
            "saveAsWithAnswers": True,
            "saveAsFilterWithPrompts": True,
            "saveAsTemplateWithPrompts": True
        }
    }

    save_response = session.post(save_report_url, headers=save_headers, json=save_payload)

    if save_response.status_code == 201:
        print("Report saved successfully.")
    else:
        print("Failed to save report:", save_response.status_code, save_response.text)
else:
    print("Failed to create report:", response.status_code, response.text)