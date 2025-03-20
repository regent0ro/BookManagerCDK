from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct


class BookManagerCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB
        book_table = dynamodb.TableV2(
            self,
            "Book",
            partition_key=dynamodb.Attribute(name="book_id", type=dynamodb.AttributeType.STRING),
        )
        user_table = dynamodb.TableV2(
            self,
            "User",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
        )

        # TODO loan_table

        # lambda
        # Books
        add_book_lambda = _lambda.Function(
            self,
            "add_book",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("book_manager_cdk/lib/lambda"),
            handler="add_book.handler",
            environment={"BOOK_TABLE_NAME": book_table.table_name},
        )
        book_table.grant_read_write_data(add_book_lambda)

        delete_book_lambda = _lambda.Function(
            self,
            "delete_book",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("book_manager_cdk/lib/lambda"),
            handler="delete_book.handler",
            environment={"BOOK_TABLE_NAME": book_table.table_name},
        )
        book_table.grant_read_write_data(delete_book_lambda)

        # Users
        add_user_lambda = _lambda.Function(
            self,
            "add_user",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("book_manager_cdk/lib/lambda"),
            handler="add_user.handler",
            environment={"USER_TABLE_NAME": user_table.table_name},
        )
        user_table.grant_read_write_data(add_user_lambda)

        delete_user_lambda = _lambda.Function(
            self,
            "delete_user",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("book_manager_cdk/lib/lambda"),
            handler="delete_user.handler",
            environment={"USER_TABLE_NAME": user_table.table_name},
        )
        user_table.grant_read_write_data(delete_user_lambda)

        # Functions
        borrow_book_lambda = _lambda.Function(
            self,
            "borrow_book",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("book_manager_cdk/lib/lambda"),
            handler="borrow_book.handler",
            environment={"BOOK_TABLE_NAME": book_table.table_name},
        )
        book_table.grant_read_write_data(borrow_book_lambda)

        return_book_lambda = _lambda.Function(
            self,
            "return_book",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("book_manager_cdk/lib/lambda"),
            handler="return_book.handler",
            environment={"BOOK_TABLE_NAME": book_table.table_name},
        )
        book_table.grant_read_write_data(return_book_lambda)

        # TODO rental_list

        # TODO API Gateway
            # book_api = apigateway.RestApi(self, "users-api")

