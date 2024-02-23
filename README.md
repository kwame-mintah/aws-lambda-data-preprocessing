# AWS Lambda Data Preprocessing

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3121/)
[![🚧 Bump version](https://github.com/kwame-mintah/aws-lambda-data-preprocessing/actions/workflows/bump-repository-version.yml/badge.svg)](https://github.com/kwame-mintah/aws-lambda-data-preprocessing/actions/workflows/bump-repository-version.yml)
[![🚀 Push Docker image to AWS ECR](https://github.com/kwame-mintah/aws-lambda-data-preprocessing/actions/workflows/push-docker-image-to-aws-ecr.yml/badge.svg)](https://github.com/kwame-mintah/aws-lambda-data-preprocessing/actions/workflows/push-docker-image-to-aws-ecr.yml)
[![🧹 Run linter](https://github.com/kwame-mintah/aws-lambda-data-preprocessing/actions/workflows/run-linter.yml/badge.svg)](https://github.com/kwame-mintah/aws-lambda-data-preprocessing/actions/workflows/run-linter.yml)

A lambda to perform data pre-processing on new data put into an S3 bucket. An assumption has been made that new data
uploaded will be of the same format e.g. same features, data schema etc. Actions performed not limited to removing missing
data, imputing numerical values and/or categorical values etc.

This repository does not create the S3 Bucket, this is created via Terraform found here [terraform-aws-machine-learning-pipeline](https://github.com/kwame-mintah/terraform-aws-machine-learning-pipeline).
Data uploaded into these buckets can be found here [ml-data-copy-to-aws-s3](https://github.com/kwame-mintah/ml-data-copy-to-aws-s3). Additionally, data preparation is
specific to a specific set of data found within the GitHub repository.

## Development

### Dependencies

- [Python](https://www.python.org/downloads/release/python-3120/)
- [Docker for Desktop](https://www.docker.com/products/docker-desktop/)
- [Amazon Web Services](https://aws.amazon.com/?nc2=h_lg)

## Usage

1. Build the docker image locally:

   ```commandline
   docker build --no-cache -t data-preprocessing:local .
   ```

2. Run the docker image built:

   ```commandline
   docker run --platform linux/amd64 -p 9000:8080 data-preprocessing:local
   ```

3. Send an event to the lambda via curl:
   ```commandline
   curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{<REPLACE_WITH_JSON_BELOW>}'
   ```
   ```json
   {
     "Records": [
       {
         "eventVersion": "2.1",
         "eventSource": "aws:s3",
         "awsRegion": "eu-west-2",
         "eventTime": "2023-12-01T21:48:58.339Z",
         "eventName": "ObjectCreated:Put",
         "userIdentity": { "principalId": "AWS:ABCDEFGHIJKLMNOPKQRST" },
         "requestParameters": { "sourceIPAddress": "127.0.0.1" },
         "responseElements": {
           "x-amz-request-id": "BY65CG6WZD6HBVX2",
           "x-amz-id-2": "c2La85nMEE2WBGPHBXDc5a8fd28kEpGt/QsP8n/xmbLv0ZAJeqsK/XmNcCCS+phWuVz8KP3/gn3Ql3/z7RPyC3n176rqpzvZ"
         },
         "s3": {
           "s3SchemaVersion": "1.0",
           "configurationId": "huh",
           "bucket": {
             "name": "test-noverycool-2139",
             "ownerIdentity": { "principalId": "ABCDEFGHIJKLMN" },
             "arn": "arn:aws:s3:::test-noverycool-2139"
           },
           "object": {
             "key": "data/bank-additional.csv",
             "size": 515246,
             "eTag": "0e29c0d99c654bbe83c42097c97743ed",
             "sequencer": "00656A54CA3D69362D"
           }
         }
       }
     ]
   }
   ```
