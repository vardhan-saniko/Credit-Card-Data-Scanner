# Introduction

AWS Credit Card Data Scanner and Alert System for CloudWatch Logs

- Author: Vishnu Vardhan Reddy Sanikommu
- Email: vrsaniko@asu.edu

# Getting Started

Follow the below instructions to get started with this project.

## Software Dependencies

- Python
- boto3

## Questions asked in project

1. what does your program do
   - Program will go through all cloudwatch logs, find if credit card information is present though regex pattern matching and raise an alert to email with cloudwatch stream details
2. how to execute it
   - listed below for different scenarios
3. explain the logic behind the pattern recognition and its reliability
   - all credit cards(VISA, Master card etc) are 13-16 digits long with or without spaces, hyphens in the middle, so the regex pattern is quite reliable in finding if the text has credit card or not
4. discuss security precautions
   - All the cloud watch logs are by default encrypted with base64. In addition to it, I am using AWS lambda below which uses AWS IAM roles with policies attached to it, so the data is secure. The client has to consider using IAM roles to prevent others to not read cloudwatch logs
5. suggest how this script could scale in a full-fledged application, considering high-volume data.
   - We can add triggers from log groups to AWS lambda function, Lambda functions are invoked parallelly and the code within it will process and create alerts. I implemented it as well

## Implementation without scalability

1. Wrote a python script using boto3 library and aws credentials to go through all cloudwatch logs.
2. Check if the log contains credit card information through regex matching and send an alert using AWS SNS by creating SNS Topic and creating subscribers to created topic

## Implementation for scalability

1. Created two Lambda Functions `gen-sensitve-sensitive-info-cloudwatch-logs` and `cloudwatch-sensitive-info-alert`
   - **gen-sensitve-sensitive-info-cloudwatch-logs** for creating logs with sensitive information
   - **cloudwatch-sensitive-info-alert** for processing logs, finding if credit card information is present and send an alert
2. Created cloud watch trigger from cloudwatch logs to lambda function `cloudwatch-sensitive-info-alert` so that Logs that store credit card information generated through lambda function `gen-sensitve-sensitive-info-cloudwatch-logs` will be sent in real time in the event param to lambda function cloudwatch-sensitive-info-alert
3. Created AWS SNS (Simple Notification Service) to send email whenever credit card information is found in the logs


## Steps to run the Code Once without scalability

1. Subscribe your email to the existing sns topic that was created
```sh
python subscribe_to_sns.py <email>
Ex:
python subscribe_to_sns.py vrsaniko@asu.edu 
```

2. Run the command to receive alerts for all existing cloud watch logs contains in all cloudwatch groups
```sh
python create_alerts_existing_logs.py
```



## Steps to run the Code for Real Time

1. Edit the config.json file at strac/config/config.json
   - AWS_KEY: your aws key
   - AWS_SECRET: your aws secret
   - AWS_REGION: aws region in which all services need to be created
   - SNS_TOPIC_NAME: SNS topic name
   - EMAIL: email to where notifications are sent
   - LAMBDA_FUNCTION_CREATE_LOGS: lambda func to create logs
   - LAMBDA_FUNCTION_CREATE_ALERTS: lambda func to process logs, create alerts if credit card is found
   - LAMBDA_CREATE_LOGS_ZIP_PATH: path of zip file in which logs generating lambda function code is present
   - LAMBDA_CREATE_ALERTS_ZIP_PATH: path of zip file in which alerts generating lambda function code is present


2. Run the below command to create logs. Once the script is executed, email recipient will receive notifications for all logs that contain credit card information. For the below command, only aws key, secret, region and email needs to be set in config.json file

```sh
python create_logs.py <absolute path of logs.txt> <logs creating lambda function name>

Ex:
python create_logs.py /Users/vishnuvardhan/PycharmProjects/strac/logs.txt gen-sensitve-sensitive-info-cloudwatch-logs
```

## Video Link


## References:

https://www.regular-expressions.info/creditcard.html

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/index.html

https://chat.openai.com/

https://stackoverflow.com/

https://docs.aws.amazon.com/