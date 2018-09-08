#!/usr/bin/env python
# encoding: utf-8

import json
import os
import ccxt
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Slack の設定
SLACK_POST_URL = os.environ['slackPostURL']
SLACK_CHANNEL = os.environ['slackChannel']

def build_message(text, color):
    atachements = {
    "title": "Bitcoin => JPY",
        "text":text,
        "color":color
    }
    return atachements

def lambda_handler(event, context):
    # BitFlyerから情報取得
    bf = ccxt.bitflyer({})
    result = bf.fetch_ticker(symbol='BTC/JPY')

    content = build_message(str(result['bid']) + 'JPY/1BTC', '#0000FF')

    # SlackにPOSTする内容をセット
    slack_message = {
        'channel': SLACK_CHANNEL,
        "username": "Bitcoin Alert",
        "attachments": [content],
    }

    # SlackにPOST
    try:
        req = requests.post(SLACK_POST_URL, data=json.dumps(slack_message))
        logger.info("Message posted to %s", slack_message['channel'])
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)