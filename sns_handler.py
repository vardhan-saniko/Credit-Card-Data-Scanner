from config.config import Config
from aws_client import AWSClient


# Creates SNS topic and SNS email subscriber
if __name__ == '__main__':

    config = Config()

    sns = AWSClient("sns").sns_client
    res = sns.create_topic(Name=config.SNS_TOPIC_NAME)
    topic_arn = res['TopicArn']
    print(f"SNS topic : {topic_arn}")

    sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=config.EMAIL
    )