import json, base64
import os
from httplib2 import Http
from json import dumps

webhook = os.getenv('WEBHOOK_URL')

def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print('Message :{}'.format(pubsub_message))
    log_data = json.loads(pubsub_message)
    if log_data["incident"]["state"] == "closed" :
        print("The incident has been closed, don't notify")
        return "True"

    alert_policy = log_data["incident"]["policy_name"]
    incident_url = log_data["incident"]["url"]
    project_id = log_data["incident"]["scoping_project_id"]
    resource_name = log_data["incident"]["resource_display_name"]

    bot_message = {
            'text' : f'***Incident Opened*** in: {project_id} Alert Policy: {alert_policy} {incident_url} Resource: {resource_name}'}

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=webhook,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print('response: {}'.format(response))
    return "True"