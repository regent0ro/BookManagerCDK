import os
import boto3
from botocore.exceptions import ClientError

BOOK_TABLE_NAME = os.environ["BOOK_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(BOOK_TABLE_NAME)

def handler(event, context):
    """
    Delete a book to the book table.
    """
    try:
        # Extract book_id from the event
        book_id = event.get("book_id")

        # Validate required field
        if not book_id:
            return {"statusCode": 400, "body": "Missing required field: book_id"}

        # Delete item from the DynamoDB table
        response = table.delete_item(
            Key={
                "book_id": book_id
            },
            ConditionExpression="attribute_exists(book_id)"  # Ensure the item exists before deleting
        )
        return {"statusCode": 200, "body": "Book deleted successfully", "response": response}

    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {"statusCode": 404, "body": "Book not found"}
        return {"statusCode": 500, "body": f"Failed to delete book: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"An unexpected error occurred: {str(e)}"}

