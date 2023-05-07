import os
import boto3
import requests
import time
import json

client = boto3.client('logs')

SLACK_WEBHOOK_URL = 'https://SLACK_WEBHOOK_URL_HERE'

def send_slack_message(text):
    payload = {'text': text}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        raise ValueError(f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}')

def lambda_handler(event, context):
    log_group_name = 'LOG GROUP NAME HERE'
    current_time = int(round(time.time() * 1000))
    start_time = current_time - 3600000 # (1 hour) Time in milliseconds, change as needed
    end_time = current_time
    
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString='YOUR QUERY HERE'
    )
    
    query_id = response['queryId']

    # wait for query to complete
    query_status = None
    while query_status == None or query_status == 'Running' or query_status == 'Scheduled':
        response = client.get_query_results(
            queryId=query_id
        )
        # Change the conditional as needed
        if len(response['results']) > 0 and len(response['results'][0]) > 0:
            result = response['results'][0][0]['value']
            if int(result) > 2:
                    # Send mensage on SLACK
                    message = f'YOUR SLACK MESSAGE HERE'
                    send_slack_message(message)
            return result     
            break
        query_status = response['status']
    return "Query completed, but no results found"
    
