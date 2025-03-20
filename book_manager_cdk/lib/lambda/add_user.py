import os
import boto3
from botocore.exceptions import ClientError

USER_TABLE_NAME = os.environ["USER_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(USER_TABLE_NAME)

def handler(event, context):
    """
    Add a user to the user table.
    """
    try:
        # Extract user details from the event
        user_id = event.get("user_id")
        first_name = event.get("first_name", user_id)
        last_name = event.get("last_name", user_id)

        # Validate required fields
        if not user_id:
            return {"statusCode": 400, "body": "Missing required field: user_id"}

        # Put item into the DynamoDB table
        response = table.put_item(
            Item={
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
            }
        )
        return {"statusCode": 200, "body": "user added successfully", "response": response}

    except ClientError as e:
        return {"statusCode": 500, "body": f"Failed to add user: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"An unexpected error occurred: {str(e)}"}

