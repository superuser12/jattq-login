#!/usr/bin/env python3

import os
import sys
import time
import json
import requests
import urllib.parse as urlparse


BASE_URL = 'https://98.248.69.219:32708'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_CREDENTIALS = os.path.join(BASE_DIR, 'credentials.json')

API_USER = os.environ.get('API_USERNAME', 'username')
API_PASSWORD = os.environ.get('API_PASSWORD', 'password')


class APIAccessError(Exception):
    pass


class Client(object):

    token_url = '/netq/auth/v1/login'
    device_list_url = '/netq/telemetry/v1/object/inventory'

    def __init__(self, base_url, auth):
        self.url = base_url
        self.auth = auth

    def get_access_token(self):
        response = requests.post(
            urlparse.urljoin(self.url, self.token_url),
            json=self.auth, verify=False
        )
        if response.status_code != 200:
            raise APIAccessError(response.json().get('message', ''))

        # TODO: permission check
        with open(API_CREDENTIALS, 'w') as fh:
            fh.write(json.dumps(response.json(), indent=4))
        return response.json()

    def get_device_list(self, access_token):
        response = requests.get(
            urlparse.urljoin(self.url, self.device_list_url),
            headers={
                "content-type": "application/json",
                "Authorization": access_token
            },
            verify=False
        )
        if response.status_code != 200:
            raise APIAccessError(response.json().get('message', ''))
        return response.json()


def get_access_token(api_client):
    """Get stored access token from credentials file or a new one

    :param api_client: Client obj
    :return: str
    """
    credentials = None
    if os.path.isfile(API_CREDENTIALS):
        with open(API_CREDENTIALS) as fh:
            credentials = json.loads(fh.read())

    # expires_at (ms) must be greater than current time at least by 100 ms
    if credentials and credentials.get('expires_at', 0) > (time.time() * 1000 + 100):
        return credentials.get('access_token', '')

    try:
        credentials = api_client.get_access_token()
    except APIAccessError:
        return None
    return credentials.get('access_token', None)


def main():
    client = Client(base_url=BASE_URL,
                    auth={"username": API_USER,
                          "password": API_PASSWORD})
    access_token = get_access_token(client)
    if access_token is None:
        sys.exit("No access token found")
    device_list = client.get_device_list(access_token)
    print(f"Device List: \n\t{device_list}")


if __name__ == '__main__':
    main()
