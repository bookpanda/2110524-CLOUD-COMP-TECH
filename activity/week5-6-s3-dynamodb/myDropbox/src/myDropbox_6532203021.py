import json
import os

import boto3

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
users_table = dynamodb.Table("myDropboxUsers")
shares_table = dynamodb.Table("myDropboxShares")

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        command: str = body.get("command")
        key: str = body.get("key", "")
        username: str = body.get("username", "")
        password: str = body.get("password", "")
        currentUser: str = body.get("currentUser", "")

        if command == "put":
            content_type = body.get("content_type")
            presigned_url = generate_presigned_url(
                BUCKET_NAME, key, "put_object", content_type
            )
            return {
                "statusCode": 200,
                "body": json.dumps({"upload_url": presigned_url}),
            }
        elif command == "get":
            presigned_url = generate_presigned_url(BUCKET_NAME, key, "get_object")
            return {
                "statusCode": 200,
                "body": json.dumps({"presigned_url": presigned_url}),
            }
        elif command == "view":
            folder_prefix = body.get("folder_prefix")
            file_list = list_s3_objects(BUCKET_NAME, folder_prefix)
            return {
                "statusCode": 200,
                "body": json.dumps({"files": file_list}, default=str),
            }
        elif command == "share":
            owner = key.split("/")[0]
            if currentUser != owner:
                return {
                    "statusCode": 403,
                    "body": json.dumps(
                        {"error": "Current user is not the owner of the file"}
                    ),
                }

            shares_table.put_item(Item={"objectKey": key, "username": username})
            return {
                "statusCode": 201,
                "body": json.dumps({"message": "File shared successfully"}),
            }

        elif command == "newuser":
            response = users_table.get_item(Key={"username": username})
            if "Item" in response:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "User already exists"}),
                }
            users_table.put_item(Item={"username": username, "password": password})
            return {
                "statusCode": 201,
                "body": json.dumps({"message": "User created successfully"}),
            }
        elif command == "login":
            response = users_table.get_item(Key={"username": username})
            if "Item" not in response:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "User not found"}),
                }
            if response["Item"]["password"] != password:
                return {
                    "statusCode": 401,
                    "body": json.dumps({"error": "Invalid password"}),
                }
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Login successful"}),
            }

        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid command"}),
            }

    except json.JSONDecodeError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Invalid JSON: {str(e)}"}),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def generate_presigned_url(
    bucket_name: str,
    file_key: str,
    purpose: str,
    content_type=None,
    expiration=3600,
):
    """
    Generates a pre-signed URL for accessing/uploading an S3 object.
    """
    try:
        params = {"Bucket": bucket_name, "Key": file_key}
        if content_type:
            params["ContentType"] = content_type

        url = s3.generate_presigned_url(
            purpose,
            Params=params,
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        return f"Error generating presigned URL: {str(e)}"


def list_s3_objects(bucket_name, folder_prefix):
    """
    Lists objects in an S3 bucket and returns their details.
    """
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

        if "Contents" not in response:
            return []

        files = []
        for obj in response["Contents"]:
            filename = obj["Key"].split("/")[-1]
            file_info = {
                "filename": filename,
                "lastModifiedDate": obj[
                    "LastModified"
                ].isoformat(),  # datetime to string
                "size": obj["Size"],
                "owner": folder_prefix,
            }
            files.append(file_info)

        return files
    except Exception as e:
        return [{"error": f"Error listing objects: {str(e)}"}]
