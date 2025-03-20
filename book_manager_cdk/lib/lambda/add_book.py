import os
import boto3
from botocore.exceptions import ClientError

BOOK_TABLE_NAME = os.environ["BOOK_TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(BOOK_TABLE_NAME)

def handler(event, context):
    """
    Add a book to the book table.
    """
    try:
        # Extract book details from the event
        book_id = event.get("book_id") # ISBN
        title = event.get("title", "Unknown Title")
        author = event.get("author", "Unknown Author")
        publisher = event.get("publisher", "Unknown Publisher")
        description = event.get("description", "")
        toc = event.get("toc", "") # table of contents
        current_user = event.get("current_user", "")

        # Validate required fields
        if not book_id:
            return {"statusCode": 400, "body": "Missing required field: book_id"}

        # Put item into the DynamoDB table
        response = table.put_item(
            Item={
                "book_id": book_id,
                "title": title,
                "author": author,
                "publisher": publisher,
                "description": description,
                "toc": toc,
                "current_user": current_user,
            }
        )
        return {"statusCode": 200, "body": "Book added successfully", "response": response}

    except ClientError as e:
        return {"statusCode": 500, "body": f"Failed to add book: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"An unexpected error occurred: {str(e)}"}

