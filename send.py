#!/usr/bin/python3
# -*- coding: utf-8 -*-
from os import listdir, chdir
from collections import deque
from time import sleep
import sys
import re
import fnmatch
import requests
import datetime
import configparser

default_limit = 1


class TailBot:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=1000):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

    def get_last_message(self, offset):
        bot.get_updates(offset)
        last_update = bot.get_last_update()
        result = {}
        result['update_id'] = last_update['update_id']
        try:
            last_message = last_update['message']
        except KeyError:
            last_message = last_update['edited_message']

        result['text'] = last_message['text'].lower()
        result['chat_id'] = last_message['chat']['id']
        result['chat_name'] = last_message['chat']['first_name']
        return result


def get_log(path, count):
    try:
        with open(path, 'r') as target_file:
            return ''.join(list(deque(target_file, count)))

    except FileNotFoundError:
        return "File not exist"


def format_message(prefix, log_data):
    if not len(log_data) > 0:
        return "There is nothing to show"
    else:
        return "%s: %s" % (prefix.upper(), log_data)


def main(config):
    offset = None
    while True:
        last_message = bot.get_last_message(offset)
        message = last_message['chat_name'] + ", this сommand is not supported"
        limit = ''.join([i if i.isdigit() else '' for i in last_message['text']])
        if not limit.isdigit():
            limit = default_limit

        for command in config['paths']:
            found = last_message['text'].find(command)
            if found >= 0:
                message = format_message(command, get_log(config['paths'][command], int(limit)))

        bot.send_message(last_message['chat_id'], message)
        offset = last_message['update_id'] + 1


required_config = {'paths', 'token'}


def validate_config(config):
    for required_section in required_config:
        if not required_section in config:
            print('Config parse error: section "%s" is not found' % required_section)
            exit()
        else:
            for key in config[required_section]:
                if not len(config[required_section][key]) > 0:
                    print('Empty value for key "%s" in section "%s" ' % (key, required_section))
                    exit()

    print('Config parsed.')
    for key in config['paths']:
        print('command "%s" supported to show "%s"' % (key, config['paths'][key]))


if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        config.read('send.cfg')
        validate_config(config)
        bot = TailBot(config['token']['value'])
        main(config)
    except KeyboardInterrupt:
        exit()
