
import json


def lambda_handler(event, context):
    """
    the function received custom log message on invocation and prints it to cloudwatch logs
    """
    print(f"CLOUDWATCH LOG :: {event['message']}")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
