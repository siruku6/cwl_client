import boto3
import datetime
import pandas as pd

def request_logs_from_cloudwatch(start_unix, end_unix):
    client = boto3.client('logs')
    log_group = '/aws/lambda/scheduled_trade'
    return client.filter_log_events(
        logGroupName=log_group,
        startTime=start,
        endTime=end
    )


if __name__ == '__main__':
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(hours=1)
    now_unix = int(today.timestamp() * 1000)
    yesterday_unix = int(yesterday.timestamp() * 1000)

    response = request_logs_from_cloudwatch(start_unix=now_unix, end_unix=yesterday_unix)
    result = pd.DataFrame.from_dict(response['events'])
    # import pdb; pdb.set_trace()
