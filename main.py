import boto3
import datetime
import pandas as pd
import yaml


YAML_PATH = './cloudwatch_cnf.yml'

def request_logs_from_cloudwatch(start_unix, end_unix):
    client = boto3.client('logs')
    with open(YAML_PATH, mode='r+') as yaml_data:
        lambda_function_names = yaml.load(yaml_data)['lambda_function_names']

    log_group = '/aws/lambda/{}'.format(lambda_function_names[0])
    return client.filter_log_events(
        logGroupName=log_group,
        startTime=start_unix,
        endTime=end_unix
    )


if __name__ == '__main__':
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(hours=24)
    now_unix = int(now.timestamp() * 1000)
    yesterday_unix = int(yesterday.timestamp() * 1000)

    response = request_logs_from_cloudwatch(start_unix=yesterday_unix, end_unix=now_unix)
    result = pd.DataFrame.from_dict(response['events'])
    # import pdb; pdb.set_trace()
