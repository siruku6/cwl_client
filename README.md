# Summary

This is the client for AWS CloudWatch Logs  
(* This application can only request the logs generated by AWS Lambda-function)

# Dependency

## aws-cli  
It is expected to setup aws-cli for your AWS account.
## python3.x  
## pip modules
Execute the following command, then required modules will be installed.
```
$ sudo pip install -r requirments.txt
```
# How to use

## 1. Entry your Lambda-function-name to yml

```bash
$ cp cloudwatch_sample_cnf.yml cloudwatch_cnf.yml
```
```yaml
# Edit cloudwatch_cnf.yml

lambda_function_names:
  - function_name_1
  - function_name_2
  - ...

# Write not '/aws/lambda/function_name_1' but 'function_name_1'
```

## 2. Execute code

```bash
$ python main.py

# input year, month, day, hour and hours of period along to prompt
```

## Option

### Filtering events of ClowdWatch Logs

You can filter the event-logs and exclude unnecessary logs, with following settings.
Filtering target is the column of 'eventId', 'logStreamName' or 'message'.

```yaml
# Edit cloudwatch_cnf.yml

# INFO: the logs, containing any of the strings in this whitelist, only remain
white_list:
  - keyword1
  - keyword2

# INFO: the logs, containing any of the strings in this blacklist, are excluded
black_list:
  - keyword3
  - keyword4
```
