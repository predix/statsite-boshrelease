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
for key, value, timestamp in metrics:
    print (key, value, timestamp)
    key = key.replace(".","_")
    #print key, value, timestamp
    json_dict["eventType"] = key
    json_dict["amount"] = float(value) 
    json_dict["account"] = timestamp
    json_text += json.JSONEncoder().encode(json_dict) + "," + "\n"

json_text = "[" + json_text + "]"
url     = 'https://insights-collector.newrelic.com/v1/accounts/NEWRELIC_ACCOUNT_ID/events'
payload = json_text
headers = {"Content-Type": "application/json", "X-Insert-Key": "NEWRELIC_API_KEY"}
try:
    res = requests.post(url, data=payload, headers=headers)
except requests.exceptions.RequestException as e: 
    print (e)
    sys.exit(1)
