import aws_cdk as core
import aws_cdk.assertions as assertions

from book_manager_cdk.book_manager_cdk_stack import BookManagerCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in book_manager_cdk/book_manager_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BookManagerCdkStack(app, "book-manager-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
