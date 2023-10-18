import sys
from config.config import Config
from aws_client import AWSClient


# Creates SNS topic and SNS email subscriber
if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception("please provide email to subscribe to existing sns topic: lambda-alert-email")

    email = sys.argv[1]
    print(email)
    config = Config()

    sns_client = AWSClient("sns").sns_client

    topic_name = 'lambda-alert-email'

    # List topics to find the topic ARN
    response = sns_client.list_topics()
    topic_arn = ""
    for topic in response['Topics']:
        if topic_name in topic['TopicArn']:
            topic_arn = topic['TopicArn']
            break

    sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )

