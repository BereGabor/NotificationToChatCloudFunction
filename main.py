import json, base64
from nis import match
import os
from httplib2 import Http
from json import dumps
# Imports the Cloud Logging client library
import google.cloud.logging
# Imports Python standard library logging
import logging
import traceback

# Instantiates a client
client = google.cloud.logging.Client()

webhook = os.getenv('WEBHOOK_URL')
message_type = os.getenv('MSG_TYPE', "TEXT")
logging_level = os.getenv('LOG_LEVEL', logging.INFO)

#CRITICAL = 50
#ERROR = 40
#WARNING = 30
#INFO = 20
#DEBUG = 10


# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.setup_logging(log_level=logging_level)



def main(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    logging.debug('Message :{}'.format(pubsub_message))
    log_data = json.loads(pubsub_message)
    if log_data["incident"]["state"] == "closed" :
        logging.info("The incident has been closed, don't notify")
        return "True"
    else:
        logging.info("Incident alert triggered: " + log_data["incident"]["summary"])

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
    logging.debug('response: {}'.format(response))
    return "True"

def buildMessage(event, msg_type):
    alert_policy = event["incident"]["policy_name"]
    incident_url = event["incident"]["url"]
    project_id = event["incident"]["scoping_project_id"]
    resource_name = ""
    try:
        resource_name = event["incident"]["resource"]["labels"]["container_name"]
    except Exception as e:
        logging.debug("Read resource name failed: " + traceback.format_exc() + " Use incident.resource_name value")
        resource_name = event["incident"]["resource_name"]
    

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
    logging.debug("Chat message request: {}".format(json.dumps(event["incident"]["resource"], indent=4)))
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
