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
            owner = key.split("/")[0]
            if currentUser == owner:
                # user is the owner of the file
                presigned_url = generate_presigned_url(BUCKET_NAME, key, "get_object")
                return {
                    "statusCode": 200,
                    "body": json.dumps({"presigned_url": presigned_url}),
                }

            # check if current user is authorized to access the file
            response = shares_table.query(
                KeyConditionExpression="username = :pk AND objectKey = :sk",
                ExpressionAttributeValues={
                    ":pk": currentUser,
                    ":sk": key,
                },
            )
            if not response["Items"]:
                return {
                    "statusCode": 403,
                    "body": json.dumps(
                        {"error": "Current user is not authorized to access the file"}
                    ),
                }

            presigned_url = generate_presigned_url(BUCKET_NAME, key, "get_object")
            return {
                "statusCode": 200,
                "body": json.dumps({"presigned_url": presigned_url}),
            }
        elif command == "view":
            current_user = body.get("folder_prefix")
            # list files in the user's folder
            file_list = list_s3_objects(BUCKET_NAME, current_user)

            # list files shared with the user
            shared_files = shares_table.query(
                KeyConditionExpression="username = :pk",
                ExpressionAttributeValues={":pk": current_user},
            )
            for item in shared_files["Items"]:
                shared_key = item["objectKey"]
                file_info = get_s3_object_info(BUCKET_NAME, shared_key)
                file_list.append(file_info)

            return {
                "statusCode": 200,
                "body": json.dumps({"files": file_list}, default=str),
            }
        elif command == "share":
            # check file exists
            response = s3.head_object(Bucket=BUCKET_NAME, Key=key)
            if "ResponseMetadata" not in response:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "File not found"}),
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


def get_s3_object_info(bucket_name, file_key):
    """
    Retrieves details of an S3 object.
    """
    try:
        response = s3.head_object(Bucket=bucket_name, Key=file_key)
        return {
            "filename": file_key.split("/")[-1],
            "lastModifiedDate": response["LastModified"].isoformat(),
            "size": response["ContentLength"],
            "owner": file_key.split("/")[0],
        }
    except Exception as e:
        return {"error": f"Error getting object info: {str(e)}"}
