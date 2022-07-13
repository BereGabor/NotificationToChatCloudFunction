# Notification To Chat CloudFunction
Simple cloud function, to send chat message (to Google Chat room) based on Logging Alert event.
This code and solution inspired by this article: https://medium.com/cts-technologies/gcp-operations-suite-alerts-into-google-chat-1a3c39f84187

You can change GCP config (region, zone, topic) in deploy script.

Have to create webhook url in google chat application. 
It will be something like this: https://chat.googleapis.com/v1/spaces/ASDFSADFSDF/messages?key=AIzaSyDdI0hCZtE6vySjMm

## Python code - main.py
Only one realy simple main function is in the main.py. 

## Deploy
Deploy sh: deploy-Send-Alert-to-MLFF-ChatRoom.sh 

The deploy run the next main commands: 
- Enable cloud build and Cloud functions api in GCP 
- Try to create the topic for cloud function 
- Deploy cloud function 

The cloud function use environment variables to configuration.

## Notification channnel and permission
Have to add pub/sub publisher role for the topic to monitorinng service account. 
You can find the exact service account name on notification channel detail page. You can send test messages from this page too. 

## Environment variables
WEBHOOK_URL: Google chat web hook URL. mandatory!  
MSG_TYPE: [TEXT,CARD] optional, default: TEXT   
    values:
    - TEXT: Simple text message  
    - CARD: Card formated message  

LOG_LEVEL: [50,40,30,20,10] optional, default: 20  
    Values:
    - CRITICAL = 50  
    - ERROR = 40  
    - WARNING = 30  
    - INFO = 20  
    - DEBUG = 10  

## Usefull links
Chat message structure documentation and examples: https://developers.google.com/chat/api/guides/message-formats/cards  
Google chat webhook: https://developers.google.com/chat/how-tos/webhooks  

Sample alert event structure is in the gcp_alert_json_example.json.  
https://github.com/BereGabor/NotificationToChatCloudFunction/blob/605d7d8a03d2b25a21d43dc6dc9acf89de6dbd16/gcp_alert_json_example.json#L1-L60
