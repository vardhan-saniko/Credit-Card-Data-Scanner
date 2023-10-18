import json
import base64
import gzip
import re
import datetime
import boto3


def lambda_handler(event, context):

    # get cloud watch logs and decrypt
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    log_events, log_group, log_stream = payload['logEvents'], payload['logGroup'], payload['logStream']

    # sns_topic_arn = "arn:aws:sns:us-east-1:297821479512:aws_lambda-alert-email"
    sns_topic_arn = "arn:aws:sns:us-east-1:297821479512:sensitive-info-alerts"
    sns_client = boto3.client('sns')

    "Regex to match 13-16 digits with spaces, hyphens in between"
    regex_pattern = r'\b(?:\d[ -]*?){13,16}\b'

    for event in log_events:
        matches = re.findall(regex_pattern, event['message'])
        if not matches:
            continue

        # Format message to deliver an alert as email
        dt = datetime.datetime.fromtimestamp(event['timestamp'] / 1000)
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        message = f"Found Sensitive Data in AWS CloudWatch Logs\n\n" \
                  f"Log Group: {log_group}\n" \
                  f"Log Stream Name: {log_stream}\n" \
                  f"Datetime: {formatted_time}\n" \
                  f"Event Id: {event['id']}"
        sns_client.publish(TopicArn=sns_topic_arn, Message=message)
    return {
        'statusCode': 200,
        'body': json.dumps('Done executing the script')
    }