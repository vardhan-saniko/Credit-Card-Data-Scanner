import sys
import json
from concurrent.futures import ThreadPoolExecutor

from aws_client import AWSClient


def invoke_lambda_function(item):
    try:
        lambda_client = AWSClient("lambda").lambda_client
        lambda_client.invoke(FunctionName=item[1], InvocationType="RequestResponse", Payload=json.dumps({"message": item[0]}))
        return True
    except Exception as exc:
        return False


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise Exception("No Logs file is provided")

    logs_file = sys.argv[1]
    function_name = sys.argv[2]
    with open(logs_file, "r") as f:
        logs = f.readlines()
    num_worker_threads = 4

    items = [(log, function_name) for log in logs]

    # Create a ThreadPoolExecutor with the specified number of worker threads
    with ThreadPoolExecutor(max_workers=num_worker_threads) as executor:

        # Submit each log to the thread pool and collect the results
        results = list(executor.map(invoke_lambda_function, items))

    print(results)
    for index, log in enumerate(logs):
        print(f"Successfully created log {log}") if results[index] else print(f"Failure in creating log {log}")

