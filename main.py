import boto3
import datetime
import pandas as pd
import yaml
import models.interface as i_face


YAML_PATH = './cloudwatch_cnf.yml'
YAML_KEY_LIST = ['lambda_function_names', 'white_list', 'black_list']

def request_logs_from_cloudwatch(start_unix, end_unix):
    client = boto3.client('logs')
    target_names = load_from_yml(key_index=YAML_KEY_LIST.index('lambda_function_names'))

    log_group = '/aws/lambda/{}'.format(target_names[0])
    return client.filter_log_events(
        logGroupName=log_group,
        startTime=start_unix,
        endTime=end_unix
    )


def load_from_yml(key_index):
    with open(YAML_PATH, mode='r+') as yml_data:
        data_in_yml = yaml.load(yml_data) \
                          .get(YAML_KEY_LIST[key_index])
    return data_in_yml


def make_response_confortable(response):
    result = pd.DataFrame.from_dict(response['events'])
    filtered_result = filter_logs(result)
    filtered_result.loc[:, 'ingestionTime'] = convert_unix_column_to_datetime(filtered_result['ingestionTime'])
    filtered_result.loc[:, 'timestamp'] = convert_unix_column_to_datetime(filtered_result['timestamp'])
    return filtered_result


def convert_unix_column_to_datetime(series):
    unix_to_datetime = lambda unix: datetime.datetime.fromtimestamp(unix)
    return (series / 1000).astype(int) \
                          .map(unix_to_datetime) \
                          .astype(str)


def filter_logs(logs):
    tmp_logs = logs.copy()
    whitelist = load_from_yml(key_index=YAML_KEY_LIST.index('white_list'))
    if whitelist is not None:
        tmp_logs = tmp_logs[include(tmp_logs, whitelist)]

    blacklist = load_from_yml(key_index=YAML_KEY_LIST.index('black_list'))
    if blacklist is None:
        return tmp_logs

    return tmp_logs[~include(tmp_logs, blacklist)]


def include(tmp_logs, pattern_list):
    pattern = '|'.join(pattern_list)
    return tmp_logs['eventId'].str.contains(pattern) \
        | tmp_logs['logStreamName'].str.contains(pattern) \
        | tmp_logs['message'].str.contains(pattern)


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
    if response['events'] == []:
        print('response is blank ...')
        exit()
    result = make_response_confortable(response)

    # import pdb; pdb.set_trace()
    result.to_csv('./cwl_events.csv')
