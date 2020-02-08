import boto3
import datetime
import pandas as pd
import yaml
import models.interface as i_face


YAML_PATH = './cloudwatch_cnf.yml'

def request_logs_from_cloudwatch(start_unix, end_unix):
    client = boto3.client('logs')
    target_names = load_target_names()

    log_group = '/aws/lambda/{}'.format(target_names[0])
    return client.filter_log_events(
        logGroupName=log_group,
        startTime=start_unix,
        endTime=end_unix
    )


def load_target_names():
    with open(YAML_PATH, mode='r+') as yaml_data:
        lambda_function_names = yaml.load(yaml_data)['lambda_function_names']
    return lambda_function_names


def convert_unix_column_to_datetime(series):
    unix_to_datetime = lambda unix: datetime.datetime.fromtimestamp(unix)
    return (series / 1000).astype(int) \
                          .map(unix_to_datetime) \
                          .astype(str)


if __name__ == '__main__':
    def ask_log_period():
        print('[prompt] 取得したいログの開始日時を入力...')
        year = i_face.ask_number('  1. 何年？', 9999)
        month = i_face.ask_number('  2. 何月？', 12)
        day = i_face.ask_number('  3. 何日？', 31)
        hour = i_face.ask_number('  4. 何時？', 23)
        print('[prompt] 取得したいログの期間を入力...')
        hours = i_face.ask_number('  5. 何時間？', 9999)

        start_datetime = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end_datetime = start_datetime + datetime.timedelta(hours=hours)
        start_unix = int(start_datetime.timestamp() * 1000)
        end_unix = int(end_datetime.timestamp() * 1000)

        return start_unix, end_unix

    start_unix, end_unix = ask_log_period()
    response = request_logs_from_cloudwatch(start_unix=start_unix, end_unix=end_unix)
    result = pd.DataFrame.from_dict(response['events'])

    result['ingestionTime'] = convert_unix_column_to_datetime(result['ingestionTime'])
    result['timestamp'] = convert_unix_column_to_datetime(result['timestamp'])

    # import pdb; pdb.set_trace()
    # result.to_csv('./cwl_events.csv')
