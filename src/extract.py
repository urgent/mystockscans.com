#!/usr/bin/env python3
#
# https://github.com/urgent/mystockscans.com/src/extract.py
#
# This script extracts data from
#
# To use the script, do the following:
#  1. Use pip to install packages in requirements.txt
#     (usually pip -r requirements.txt)
#  2. Set API_KEY in .env to the marketstack.com key
#  3. Run the script.  It will make the request, printing out information
#     about the auth process along the way.

import requests
from dotenv import load_dotenv
import os
import io
import json

load_dotenv()

API_BASE_URL = 'https://api.marketstack.com/v1/'

API_KEY = os.getenv("API_KEY")

# Create a session object to reuse TCP connections to the server
session = requests.session()


def do_get(relative_url, *, params={}, headers={}):
    '''
    Executes an HTTP GET against the given resource.
    The request is authorized using the given URL key.
    '''

    params['access_key'] = API_KEY

    url = API_BASE_URL.strip("/") + relative_url

    print("http: Fetching:   {}".format(url))
    print("http: Parameters: {}".format(params))
    print("http: Headers:  {}".format(headers))
    print()

    response = session.get(url, params=params, headers=headers)

    print("http: Status ({}), {} bytes returned:".format(
        response.status_code, len(response.content)))
    content_str = ''
    if len(response.content) > 0:
        content_str = response.content.decode('utf-8')
        print(content_str)
        print()

    response.raise_for_status()

    if len(content_str) > 0:
        return json.loads(content_str)

    return None


def get_eod(id: str):
    return do_get("/tickers/" + id + "/eod")


def extract(id: str, fd_out):
    '''
    Prints top from /devices/
    '''
    devices = get_eod(id)

    json.dump(devices, fd_out, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    output = os.path.join('data', 'extract', 'prices.json')

    os.makedirs(os.path.join('data', 'extract'), exist_ok=True)

    with io.open(output, 'w', encoding='utf8') as fd_out:
        extract("aapl", fd_out)
