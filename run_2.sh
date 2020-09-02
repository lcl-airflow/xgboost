#!/bin/bash
MAIN_TRAINER_MODULE='trainer.train'
STAGING_BUCKET='gs://ml-eng-model-staging'
NOW=$(date +%s)
JOB_NAME='xgboosttraining'$NOW
JOB_DIR='gs://ml-eng-model-staging/'
REGION='us-central1'
TRAINER_PACKAGE_PATH='/home/herman_cheung/xgboost/trainer/'

gcloud ai-platform jobs submit training $JOB_NAME \
        --package-path $TRAINER_PACKAGE_PATH \
        --module-name $MAIN_TRAINER_MODULE \
        --job-dir $JOB_DIR \
        --region $REGION \
        --config train_model.yaml 