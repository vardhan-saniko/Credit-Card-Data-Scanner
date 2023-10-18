import boto3
from config.config import Config
config = Config()
AWS_KEY, AWS_SECRET, AWS_REGION = config.AWS_KEY, config.AWS_SECRET, config.AWS_REGION


class AWSClient:
    def __init__(self, *args):
        for resource in args:
            setattr(self, '%s_client' % (resource,), boto3.client(resource,
                    aws_access_key_id=AWS_KEY,
                    aws_secret_access_key=AWS_SECRET,
                    region_name=AWS_REGION))


