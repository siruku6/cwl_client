import datetime

import boto3
import pandas as pd
import yaml

import cwl_client.interface as i_face


YAML_PATH = './cloudwatch_cnf.yml'
YAML_KEY_LIST = [
    'lambda_function_names',
    'log_stream_name_prefix',
    'white_list',
    'black_list'
]


def request_logs_from_cloudwatch(target_name, start_unix=None, end_unix=None, stream_prefix=None):
    client = boto3.client('logs')

    log_group = '/aws/lambda/{}'.format(target_name)
    if stream_prefix is not None:
        response = client.filter_log_events(
            logGroupName=log_group,
            logStreamNamePrefix=stream_prefix,
        )
    else:
        response = client.filter_log_events(
            logGroupName=log_group,
            startTime=start_unix,
            endTime=end_unix
        )
    return response


def load_from_yml(key_index):
    with open(YAML_PATH, mode='r+') as yml_data:
        data_in_yml = yaml.load(yml_data, Loader=yaml.FullLoader) \
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


def main():
    use_span_filter = i_face.ask_true_or_false('Would you like to filter logs by span ? ... [1] yes, [2] No : ')
    start_unix = end_unix = stream_prefix = None
    if use_span_filter:
        start_unix, end_unix = ask_log_period()
    else:
        stream_prefix = load_from_yml(key_index=YAML_KEY_LIST.index('log_stream_name_prefix'))

    target_names = load_from_yml(key_index=YAML_KEY_LIST.index('lambda_function_names'))
    for name in target_names:
        response = request_logs_from_cloudwatch(
            target_name=name,
            start_unix=start_unix, end_unix=end_unix,
            stream_prefix=stream_prefix
        )
        if response['events'] == []:
            print('response is blank ...')
            exit()
        result = make_response_confortable(response)

        # import pdb; pdb.set_trace()
        written_datetime = datetime.datetime.today().strftime('%Y%m%d_%H%M')
        result.to_csv('./tmp/csvs/{}_cwl_events_{}.csv'.format(written_datetime, name))


if __name__ == '__main__':
    main()
