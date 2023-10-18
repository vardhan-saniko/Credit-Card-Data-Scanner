from config.config import Config
from aws_client import AWSClient

from aws_lambda import cw_logs_handler


def create_role(role, policies):

    # Create the IAM role
    res = iam_client.create_role(
        RoleName=role,
        AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
    )

    # Attach policies to the IAM role
    for policy in policies:
        iam_client.attach_role_policy(
            RoleName=role,
            PolicyArn=f'arn:aws:iam::aws:policy/{policy}'
        )

    return res


if __name__ == "__main__":
    config = Config()

    aws_client = AWSClient("lambda", "logs", "iam")
    iam_client, lambda_client, logs_client = aws_client.iam_client, aws_client.lambda_client, aws_client.logs_client

    # create role for Lambda function which will create logs
    basic_lambda_role = create_role("aws-basic-lambda-role", ["service-role/AWSLambdaBasicExecutionRole"])
    # role = iam_client.get_role(RoleName='AWSLambdaBasicExecutionRole')

    with open(config.LAMBDA_CREATE_LOGS_ZIP_PATH, 'rb') as f:
        zipped_code = f.read()

    # create Lambda function for the creation of logs
    response = lambda_client.create_function(
        FunctionName=config.LAMBDA_FUNCTION_CREATE_LOGS,
        Runtime='python3.9',
        Role=basic_lambda_role['Role']['Arn'],
        Handler='cw_logs_handler.lambda_handler',
        Code=dict(ZipFile=zipped_code),
        Timeout=300,
    )

    custom_lambda_role = create_role("aws-lambda-custom-role-strac", ['AmazonSNSFullAccess', 'service-role/AWSLambdaBasicExecutionRole', 'CloudWatchLogsFullAccess'])

    with open(config.LAMBDA_CREATE_ALERTS_ZIP_PATH, 'rb') as f:
        zipped_code = f.read()

    # create Lambda function for finding if credit card information is present in the logs and generate alert
    response = lambda_client.create_function(
        FunctionName=config.LAMBDA_FUNCTION_CREATE_ALERTS,
        Runtime='python3.9',
        Role=custom_lambda_role['Role']['Arn'],
        Handler='cw_logs_handler.lambda_handler',
        Code=dict(ZipFile=zipped_code),
        Timeout=300,
    )

    # Get cloud watch log group from lambda function
    cloud_watch_log_group = lambda_client.get_function_configuration(FunctionName=config.LAMBDA_FUNCTION_CREATE_LOGS)['FunctionName']

    # Retrieve the Log Group ARN
    response = logs_client.describe_log_groups(logGroupNamePrefix=cloud_watch_log_group)
    log_group_arn = response['logGroups'][0]['arn']

    # Add a CloudWatch Logs trigger to the Lambda function
    response = lambda_client.create_event_source_mapping(
        EventSourceArn=log_group_arn,
        FunctionName=config.LAMBDA_FUNCTION_CREATE_ALERTS,
        Enabled=True
    )


