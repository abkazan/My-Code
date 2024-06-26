# this is example code to get contact properties from a phone number in Hubspot CRM using api

import os
import requests
def get_props_from_number(phone_number):
    api_key = os.environ.get("HUBSPOT_PRIVATE_APP_TOKEN")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.hubspot.com/crm/v3/objects/contacts/search'
    query = {
        'query': f'"{phone_number}"',
        'filterGroups': [
            {
                'filters': [
                    {
                        'propertyName': 'mobilephone',
                        'operator': 'EQ',
                        'value': phone_number
                    }
                ]
            },
            {
                'filters': [
                    {
                        'propertyName': 'phone',
                        'operator': 'EQ',
                        'value': phone_number
                    }
                ]
            }
        ],
        'properties': [ "lastname", 
                        "firstname", 
                        "leadsource", 
                        "case_type", 
                        "hs_lead_status", 
                        "mobilephone", 
                        "phone"]
    }
    try:
        response = requests.post(url, headers=headers, json=query)
        data = response.json()
        returned_properties = data['results'][0]['properties']
        return returned_properties
    except Exception:
        return None
    
def create_association(client_id):
    return [
            {
            "to": {
                "id": client_id
            },
            "types": 
                [
                    {
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId": 16
                    }
                ]
            }, 
        ]
# this is example code to autmate ticket creation in CRM once again using Hubspot API
def create_ticket_from_call(name="default", content="ticket was created for testing purposes", priority="LOW", preferred_contact="text", contact_id=None):
    api_key = "<your-api-key>"
    url = "https://api.hubspot.com/crm/v3/objects/tickets"
    # Headers with API key and content type
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    ticket_data = {
        "properties": {
            "subject": f"{name}, {priority} priority",
            "content": content,
            "hs_pipeline_stage": "1",
            "hs_ticket_priority": priority,
            "source_type": "PHONE",
            "preferredcontact": f"{preferred_contact.upper()}"
    }}
    if contact_id is not None:
        ticket_data["associations"] = create_association(contact_id)
    response = requests.post(url, headers=headers, json=ticket_data)
    if response.status_code == 201:
        print("Ticket created successfully, check hubspot for results")
        return response.json()
    else:
        print(f"Error creating ticket, {response.json()['message']}")
