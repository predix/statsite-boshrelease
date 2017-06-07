#!/usr/bin/env python3
import sys
import requests
try: import simplejson as json
except ImportError: import json

lines = sys.stdin.read().split("\n")
metrics = [l.split("|") for l in lines]

# The last value is an empty list
metrics = metrics[:-1]

json_dict = {}
json_text = ""
num_metrics = 0
for key, value, timestamp in metrics:
    print (key, value, timestamp)
    key =  key.replace(".","_")
    json_dict["eventType"] = key
    json_dict["amount"] = float(value) 
    json_dict["account"] = timestamp
    json_text += json.JSONEncoder().encode(json_dict) + "," + "\n"
    num_metrics += 1

json_text = "[" + json_text + "]"

if num_metrics > 0:
    url     = 'https://insights-collector.newrelic.com/v1/accounts/NEWRELIC_ACCOUNT_ID/events'
    payload = json_text
    headers = {"Content-Type": "application/json", "X-Insert-Key": "NEWRELIC_API_KEY"}
    try:
        res = requests.post(url, data=payload, headers=headers)
        print ("Number of metrics sent to Newrelic:")
        print (num_metrics)
        print (res)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

sys.exit(0)
