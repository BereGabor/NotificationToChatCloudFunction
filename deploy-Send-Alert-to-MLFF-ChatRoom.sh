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
FN_REGION="us-central1"
FN_SOURCE_DIR="./"
FN_SA="pubsub-sendmail@PROJECTID.iam.gserviceaccount.com"
#FN_VPC_CONN="pubsub-sendmail"

ENVVARS_FILE=/tmp/send_mail_envvars.$$

cat <<EOF >$ENVVARS_FILE
WEBHOOK_URL: "$MAIL_FROM"
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
#    --service-account "$FN_SA" \
--env-vars-file $ENVVARS_FILE \
--source $FN_SOURCE_DIR
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
