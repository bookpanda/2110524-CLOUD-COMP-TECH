import json
import os

import boto3

s3 = boto3.client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        command = body.get("command")
        key = body.get("key", "")

        if command == "put":
            file_content = body.get("file_content", "")
            response = s3.put_object(
                Bucket=BUCKET_NAME, Key=key, Body=file_content.encode("utf-8")
            )
            return {
                "statusCode": 200,
                "body": json.dumps({"response": response}),
            }
        elif command == "get":
            presigned_url = generate_presigned_url(BUCKET_NAME, key)
            return {
                "statusCode": 200,
                "body": json.dumps({"presigned_url": presigned_url}),
            }
        elif command == "view":
            file_list = list_s3_objects(BUCKET_NAME)
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"files": file_list}, default=str
                ),  # Convert datetime to string
            }

        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid command"}),
            }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in body"}),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def generate_presigned_url(bucket_name, file_key, expiration=3600):
    """
    Generates a pre-signed URL for accessing an S3 object.
    """
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": file_key},
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        return f"Error generating presigned URL: {str(e)}"


def list_s3_objects(bucket_name):
    """
    Lists objects in an S3 bucket and returns their details.
    """
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        if "Contents" not in response:
            return []

        files = []
        for obj in response["Contents"]:
            file_info = {
                "filename": obj["Key"],
                "lastModifiedDate": obj[
                    "LastModified"
                ].isoformat(),  # datetime to string
                "size": obj["Size"],
                "owner": obj.get("Owner", {}).get("DisplayName")
                or obj.get("Owner", {}).get("ID", "Unknown"),
            }
            files.append(file_info)

        return files
    except Exception as e:
        return [{"error": f"Error listing objects: {str(e)}"}]
