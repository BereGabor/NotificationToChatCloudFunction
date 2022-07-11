#!/bin/sh

# deploy-Send-Alert-to-MLFF-ChatRoom
#
# This shell script deploys the pubsub_sendmail Google Cloud Function.
# The Cloud Function receives a Cloud Pub/Sub event from Loggin Alert and sends
# a chat message used a webhook.

# Set these variables as appropriate:

# FN_PUBSUB_TOPIC = Cloud Function Pub/Sub topic.
# FN_REGION       = Region to deploy the function.
# FN_SOURCE_DIR   = Source directory for the function code.
# FN_SA           = Service Account to run the function.
# FN_VPC_CONN     = VPC Connector to use.
#

# Enable the services in case they are not enabled
gcloud services enable cloudbuild.googleapis.com cloudfunctions.googleapis.com

FN_PUBSUB_TOPIC="MLFFAlertToChat"
FN_REGION="europe-west1"
FN_SOURCE_DIR="./"
FN_SA="pubsub-sendmail@PROJECTID.iam.gserviceaccount.com"

#creaate topic
gcloud pubsub topics create $FN_PUBSUB_TOPIC

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAAADEXWz9E/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=GaEUBAJ3-LVtPAp4DsuVh_RTyeEV2666QOkw7gzoVIQ%3D"
#MSG_TYPE can be: TEXT, CARD
# TEXT: simple text message
# CARD: Card type message
MSG_TYPE="CARD"

ENVVARS_FILE=/tmp/send_chatmsg_envvars.$$

cat <<EOF >$ENVVARS_FILE
WEBHOOK_URL: "$WEBHOOK_URL"
MSG_TYPE: "$MSG_TYPE"
EOF

echo
echo Here is the environment variables file:
echo
cat $ENVVARS_FILE
echo

#if [ -z "$FN_VPC_CONN" ]
#then
gcloud functions deploy Send-Alert-to-MLFF-ChatRoom \
--region $FN_REGION \
--runtime python38 \
--trigger-topic $FN_PUBSUB_TOPIC \
--env-vars-file $ENVVARS_FILE \
--source $FN_SOURCE_DIR \
--entry-point main

#else
#    gcloud functions deploy Send-Alert-to-MLFF-ChatRoom \
#    --region $FN_REGION \
#    --runtime python38 \
#    --trigger-topic $FN_PUBSUB_TOPIC \
 #   --service-account "$FN_SA" \
#    --env-vars-file $ENVVARS_FILE \
#    --vpc-connector $FN_VPC_CONN \
#    --egress-settings all \
#    --source $FN_SOURCE_DIR
#fi

rm $ENVVARS_FILE
