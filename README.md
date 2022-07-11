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

## Environment variables
WEBHOOK_URL: Google chat web hook URL.


