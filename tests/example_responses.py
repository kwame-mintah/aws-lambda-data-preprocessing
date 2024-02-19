from datetime import datetime


def example_tag_set_without_processed_time() -> dict:
    return {
        "VersionId": "string",
        "TagSet": [
            {"Key": "string", "Value": "string"},
        ],
    }


def example_empty_tag_set() -> dict:
    return {
        "TagSet": [],
    }


def example_tag_set_with_processed_time():
    return {
        "VersionId": "string",
        "TagSet": [
            {"Key": "ProcessedTime", "Value": "2024-01-14 15:29:22"},
        ],
    }


def example_get_object():
    return {
        "Body": "example-bank-file.csv",
        "DeleteMarker": True,
        "AcceptRanges": "string",
        "Expiration": "string",
        "Restore": "string",
        "LastModified": datetime(2015, 1, 1),
        "ContentLength": 123,
        "ETag": "string",
        "ChecksumCRC32": "string",
        "ChecksumCRC32C": "string",
        "ChecksumSHA1": "string",
        "ChecksumSHA256": "string",
        "MissingMeta": 123,
        "VersionId": "string",
        "CacheControl": "string",
        "ContentDisposition": "string",
        "ContentEncoding": "string",
        "ContentLanguage": "string",
        "ContentRange": "string",
        "ContentType": "string",
        "Expires": datetime(2015, 1, 1),
        "WebsiteRedirectLocation": "string",
        "ServerSideEncryption": "AES256",
        "Metadata": {"string": "string"},
        "SSECustomerAlgorithm": "string",
        "SSECustomerKeyMD5": "string",
        "SSEKMSKeyId": "string",
        "BucketKeyEnabled": True | False,
        "StorageClass": "STANDARD",
        "RequestCharged": "requester",
        "ReplicationStatus": "COMPLETE",
        "PartsCount": 123,
        "TagCount": 123,
        "ObjectLockMode": "GOVERNANCE",
        "ObjectLockRetainUntilDate": datetime(2015, 1, 1),
        "ObjectLockLegalHoldStatus": "ON",
    }


def example_get_put_object():
    return {
        "Expiration": "string",
        "ETag": "string",
        "ChecksumCRC32": "string",
        "ChecksumCRC32C": "string",
        "ChecksumSHA1": "string",
        "ChecksumSHA256": "string",
        "ServerSideEncryption": "AES256",
        "VersionId": "string",
        "SSECustomerAlgorithm": "string",
        "SSECustomerKeyMD5": "string",
        "SSEKMSKeyId": "string",
        "SSEKMSEncryptionContext": "string",
        "BucketKeyEnabled": True,
        "RequestCharged": "requester",
    }


def example_event():
    return {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "eu-west-2",
                "eventTime": "2023-12-01T21:48:58.339Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {"principalId": "AWS:ABCDEFGHIJKLMNOPKQRST"},
                "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                "responseElements": {
                    "x-amz-request-id": "BY65CG6WZD6HBVX2",
                    "x-amz-id-2": "c2La85nMEE2WBGPHBXDc5a8fd28kEpGt/QsP8n/xmbLv0ZAJeqsK/XmNcCCS+phWuVz8KP3/gn3Ql3/z7RPyC3n176rqpzvZ",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "huh",
                    "bucket": {
                        "name": "test-noverycool-2139",
                        "ownerIdentity": {"principalId": "ABCDEFGHIJKLMN"},
                        "arn": "arn:aws:s3:::test-noverycool-2139",
                    },
                    "object": {
                        "key": "example-bank-file.csv",
                        "size": 515246,
                        "eTag": "0e29c0d99c654bbe83c42097c97743ed",
                        "sequencer": "00656A54CA3D69362D",
                    },
                },
            }
        ]
    }
