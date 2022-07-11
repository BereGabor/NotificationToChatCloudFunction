import json, base64
import os
from httplib2 import Http
from json import dumps

webhook = os.getenv('WEBHOOK_URL')
message_type = os.getenv('MSG_TYPE', "TEXT")

def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print('Message :{}'.format(pubsub_message))
    log_data = json.loads(pubsub_message)
    if log_data["incident"]["state"] == "closed" :
        print("The incident has been closed, don't notify")
        return "True"
    bot_message = buildMessage(log_data, message_type)    
    
    sendChatMessage(bot_message)
    return "True"

def sendChatMessage(msg):
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=webhook,
        method='POST',
        headers=message_headers,
        body=dumps(msg),
    )
    print('response: {}'.format(response))
    return "True"

def buildMessage(event, msg_type):
    alert_policy = event["incident"]["policy_name"]
    incident_url = event["incident"]["url"]
    project_id = event["incident"]["scoping_project_id"]
    resource_name = event["incident"]["resource_display_name"]

    #build simple text message by default
    bot_message = {
            'text' : f'***Incident Opened*** in: {project_id} Alert Policy: {alert_policy} {incident_url} Resource: {resource_name}'
            }

    
    resource_info = json.dumps(event["incident"]["resource"], indent=4)
    if msg_type == "CARD":
        bot_message = {
            'cards': [
                {
                'header': {
                    'title': f'<b>Log alert fired</b> in: <b>{project_id}</b>',
                    'subtitle': f'{alert_policy}',
                    'imageUrl': 'https://ci6.googleusercontent.com/proxy/MeF0qHCeXoHO6sZdwyDJPW8MrFJukyyLOKW6703wHHC_KcugLRHMcefKAUum3XfVH31VUNn4pizToww9ToKyJh0HZpvYTn2e3vyJ3CAtAp3wf25phkR0zA=s0-d-e1-ft#https://www.gstatic.com/stackdriver/notification/exclamation_mark.png',
                    'imageStyle': 'IMAGE'
                },
                'sections': [
                        {
                        'widgets': [
                                {
                                'keyValue': {
                                        'topLabel':'<b>Resource name</b>',
                                        'content': f'{resource_name}'
                                }
                            },
                        ]
                        },
                        {
                        'widgets': [
                                {
                                'textParagraph':{
                                    'text': f'<b>Resource labels: <br> {resource_info} </b>'
                                },
                                'buttons': [
                                        {
                                        'textButton': {
                                            'text': 'OPEN INCIDENT',
                                            'onClick': {
                                                'openLink': {
                                                    'url': f'{incident_url}'
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    print("Chat message request: {}".format(json.dumps(event["incident"]["resource"], indent=4)))
    return bot_message


# quick test script
#print(buildMessage(
#    {'incident': {
#        'policy_name': 'Test policy name',
#        'url': 'http:\\.....',
#        'scoping_project_id': 'project id in test incident',
#        'resource_display_name': 'component name'
#        }
#    }, "CARD")
#    )
