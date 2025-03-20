from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
)
from constructs import Construct


class BookManagerCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB
        book_table = dynamodb.TableV2(
            self,
            "Book",
            partition_key=dynamodb.Attribute(
                name="book_id", type=dynamodb.AttributeType.STRING),
        )
        # user_table = dynamodb.TableV2(
        #     self,
        #     "User",
        #     partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
        # )

        # lambda
        # borrow
        # borrow_book_lambda = _lambda.Function(
        #     self,
        #     "borrow_book",
        #     runtime=_lambda.Runtime.Python_3_13,
        #     code=_lambda.Code.from_asset("lambda"),
        #     handler="borrow_book.handler",
        #     environment={},
        # )

        # ## return
        # return_book_lambda = _lambda.Function(
        #     self,
        #     "return_book",
        #     runtime=_lambda.Runtime.Python_3_13,
        #     code=_lambda.Code.from_asset("lambda"),
        #     handler="return_book.handler",
        #     environment={},
        # )

        # # add
        # add_book_lambda = _lambda.Function(
        #     self,
        #     "add_book",
        #     runtime=_lambda.Runtime.PYTHON_3_13,
        #     code=_lambda.Code.from_asset("book_manager_cdk/lib/lambda"),
        #     handler="add_book.handler",
        #     environment={},
        # )

        # ## delete
        # delete_book_lambda = _lambda.Function(
        #     self,
        #     "delete_book",
        #     runtime=_lambda.Runtime.Python_3_13,
        #     code=_lambda.Code.from_asset("lambda"),
        #     handler="delete_book.handler",
        #     environment={},
        # )
