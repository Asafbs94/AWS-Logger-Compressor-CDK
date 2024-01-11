from constructs import Construct
from aws_cdk import App, Stack,Duration
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway
import os
import aws_cdk as cdk

from aws_assignment.aws_assignment_stack import AwsAssignmentStack
class LogReceiverStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Lambda function to handle incoming requests
        log_receiver_lambda = _lambda.Function(
            self, "LogReceiverLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler.lambda_handler",  # Correct handler format
            code=_lambda.Code.from_asset(r"C:\Users\asafb\Desktop\AWS_Assignment\lambda"),
            timeout=Duration.seconds(30)
        )

        # Grant necessary permissions to Lambda function
        log_receiver_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            resources=["*"]
        ))

        # API Gateway
        api = apigateway.RestApi(
            self, "LogReceiverApi",
            rest_api_name="LogReceiverApi",
            description="API to receive log file content"
        )

        # Lambda integration with API Gateway
        integration = apigateway.LambdaIntegration(
            log_receiver_lambda,
            proxy=True
        )

        # API Gateway resource and method
        api.root.add_method("POST", integration)

app = cdk.App()
LogReceiverStack(app, "LogReceiverStack")
app.synth()
