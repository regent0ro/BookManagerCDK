import os
import boto3
from botocore.exceptions import ClientError

BOOK_TABLE_NAME = os.environ["BOOK_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(BOOK_TABLE_NAME)

def handler(event, context):
    """
    Updates the user_id of a book table to the current_user.
    """
    try:
        book_id = event.get("book_id") # ISBN
        borrow_user_id = event.get("user_id")
        if not book_id:
            return {"statusCode": 400, "body": "Missing required field: book_id"}
        if not borrow_user_id:
            return {"statusCode": 400, "body": "Missing required field: borrow_user_id"}

        # Update the current_user field with the user_id
        response = table.update_item(
            Key={'book_id': book_id},
            UpdateExpression="SET current_user = :user",
            ConditionExpression="attribute_not_exists(current_user) OR current_user = :empty",
            ExpressionAttributeValues={':user': borrow_user_id, ':empty': ""},
            ReturnValues="UPDATED_NEW"
        )
        return {"statusCode": 200, "body": "Book borrowed successfully.", "updatedAttributes": response.get('Attributes')}
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {"statusCode": 409, "body": "Book is already borrowed by another user."}
        elif e.response['Error']['Code'] == "ResourceNotFoundException":
            return {"statusCode": 404, "body": "Book not found."}
        else:
            return {"statusCode": 500, "body": str(e)}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}