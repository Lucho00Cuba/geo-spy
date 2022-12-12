#!/usr/bin/env python3
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sys
import requests
import json
import logging

HTML_FILE_NAME = "index.html"
app = FastAPI()

def get_file_data(file_path):
    with open(file_path, 'r') as open_file:
        return open_file.read()

def slack(message=None):
    if message is None:
        return 1
    url = "https://hooks.slack.com/services/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"
    title = (f"Client IP :zap:")
    slack_data = {
        "username": "Maverick",
        "icon_emoji": ":airplane:",
        "attachments": [
            {
                "color": "#2348ad",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    else:
        logging.info('SEND DATA SLACK')
    return 0

@app.get("/", response_class=HTMLResponse)
def get_website():
    html_data = ""
    try:
        html_data = get_file_data(HTML_FILE_NAME)
    except FileNotFoundError:
        pass
    except Exception as e:
        logging.error(f'{e}')
    return html_data

@app.post("/location_update")
async def update_location(data: dict):
    message = None
    if data['status'] == "success":
        for key in data:
            if data[key] != " " and data[key] != False:
                if message == None:
                    message = f"{key}: {data[key]}\n"
                else:
                    message = message + f"{key}: {data[key]}\n"
    if message != None:
        slack(message)
    return "OK"

def start_http_server():
    logging.info('Starting HTTP')
    try:
        uvicorn.run(app, host="0.0.0.0")
    except Exception as e:
        logging.error(f'{e}')

if __name__ == "__main__":
    start_http_server()
