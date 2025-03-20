import os
import boto3
from botocore.exceptions import ClientError

USER_TABLE_NAME = os.environ["USER_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(USER_TABLE_NAME)

def handler(event, context):
    """
    Delete a user to the user table.
    """
    try:
        # Extract user_id from the event
        user_id = event.get("user_id")

        # Validate required field
        if not user_id:
            return {"statusCode": 400, "body": "Missing required field: user_id"}

        # Delete item from the DynamoDB table
        response = table.delete_item(
            Key={
                "user_id": user_id
            },
            ConditionExpression="attribute_exists(user_id)"  # Ensure the item exists before deleting
        )
        return {"statusCode": 200, "body": "user deleted successfully", "response": response}

    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {"statusCode": 404, "body": "user not found"}
        return {"statusCode": 500, "body": f"Failed to delete user: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"An unexpected error occurred: {str(e)}"}

