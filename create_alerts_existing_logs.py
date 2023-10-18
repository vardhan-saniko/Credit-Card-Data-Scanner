
import boto3
import re
import datetime
from config.config import Config


if __name__ == "__main__":

    config = Config()
    cloudwatch_logs = boto3.client('logs', aws_access_key_id=config.AWS_KEY,
                                   aws_secret_access_key=config.AWS_SECRET)

    # all log groups
    log_groups = cloudwatch_logs.describe_log_groups()

    # Regex to match 13-16 digits with spaces, hyphens in between
    pattern = r'\b(?:\d[ -]*?){13,16}\b'
    # SNS topic ARN, created email subscription in aws console for this topic so that whenever a message in topic is created, email recipient will receive an email
    sns_topic_arn = "arn:aws:sns:us-east-1:297821479512:lambda-alert-email"

    # boto3 sns client
    sns_client = boto3.client('sns', aws_access_key_id=config.AWS_KEY, aws_secret_access_key=config.AWS_SECRET)

    """
    Checking all existing logs and generating alerts if credit card is found.
    Credit card is matched using regex pattern through python re library
    """
    for log_group in log_groups['logGroups']:
        log_group_name = log_group['logGroupName']
        response = cloudwatch_logs.filter_log_events(
            logGroupName=log_group_name,
        )

        for event in response['events']:
            matches = re.findall(pattern, event['message'])
            dt = datetime.datetime.fromtimestamp(event['ingestionTime'] / 1000)
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            message = f"Found Sensitive Data in AWS CloudWatch Logs\n\nLog Stream Name:{event['logStreamName']}\nDatetime:{formatted_time}\nEvent Id: {event['eventId']}"
            if matches:
                response = sns_client.publish(
                    TopicArn=sns_topic_arn,
                    Message=message
                )