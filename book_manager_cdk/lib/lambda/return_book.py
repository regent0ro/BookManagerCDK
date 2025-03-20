import os
import boto3
from botocore.exceptions import ClientError

BOOK_TABLE_NAME = os.environ["BOOK_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(BOOK_TABLE_NAME)

def handler(event, context):
    """
    Deletes the current_user field from the book table to return a book.
    """
    try:
        book_id = event.get("book_id")  # ISBN
        return_user_id = event.get("user_id")
        if not book_id:
            return {"statusCode": 400, "body": "Missing required field: book_id"}
        if not return_user_id:
            return {"statusCode": 400, "body": "Missing required field: return_user_id"}

        # Put empty value(to return) in the current_user field
        response = table.update_item(
            Key={'book_id': book_id},
            UpdateExpression="SET current_user = :empty",
            ConditionExpression="current_user = :user",
            ExpressionAttributeValues={':user': return_user_id, ':empty': ""},
            ReturnValues="UPDATED_NEW"
        )
        return {"statusCode": 200, "body": "Book returned successfully.", "updatedAttributes": response.get('Attributes')}
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {"statusCode": 409, "body": "Book is not borrowed by this user."}
        else:
            return {"statusCode": 500, "body": str(e)}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}