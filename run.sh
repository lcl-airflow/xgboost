#!/bin/bash
MAIN_TRAINER_MODULE='xgboost.train'
STAGING_BUCKET='gs://ml-eng-model-staging'
NOW=$(date +%s)
JOB_NAME='xgboosttraining'$NOW
JOB_DIR='gs://ml-eng-model-staging/package'
REGION='us-central1'
TRAINER_PACKAGE_PATH='/home/herman_cheung/xgboost/xgboost/'
ARG1='gs://cloud-samples-data/ai-platform/iris/'
ARG2='iris_data.csv'
ARG3='iris_target.csv'
ARG4='ml-eng-model-staging'
ARG5='iris-staging'

gcloud ai-platform jobs submit training $JOB_NAME \
        --package-path $TRAINER_PACKAGE_PATH \
        --module-name $MAIN_TRAINER_MODULE \
        --job-dir $JOB_DIR \
        --region $REGION \
        --config train_model.yaml \
        -- \
        --input=$ARG1 \
        --data=$ARG2 \
        --target=$ARG3 \
        --staging=$ARG4 \
        --stagedir=$ARG5