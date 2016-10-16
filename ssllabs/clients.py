#!/usr/bin/env python

import logging
import sys
import time

import requests


class RESTClient(object):
    """
    SSL Labs API client
    """
    default_wait_time = 10
    endpoint = 'https://api.ssllabs.com/api/v2/'

    def __init__(self, host):
        self._host = host

    def info(self):
        url = "".join([self.endpoint, 'info'])
        try:
            response = requests.get(url).json()
        except requests.RequestException:
            logging.exception('Request failed.')
            sys.exit(1)

        return response

    def get_endpoint_data(self, s, host=None, from_cache='on'):

        url = "".join([self.endpoint, 'getEndpointData'])
        host = host or self._host
        payload = {
            'host': host,
            'fromCache': from_cache,
            's': s,
        }

        try:
            response = requests.get(url, params=payload).json()
        except requests.RequestException:
            logging.exception('Request failed.')
            sys.exit(1)
        return response

    def analyze(self, host=None, publish='off', start_new='on', from_cache='off', _all='done', ignore_mismatch='off'):
        """
        Call the analyze API call,
        :param host:
        :param publish:
        :param start_new:
        :param from_cache:
        :param _all:
        :param ignore_mismatch:
        :return:
        """

        host = host or self._host
        payload = {
            'host': host,
            'publish': publish,
            'all': _all,
            'ignoreMismatch': ignore_mismatch
        }

        if start_new == 'on':
            payload['startNew'] = start_new
            payload['ignoreMismatch'] = 'on'
        elif from_cache == 'on':
            payload['fromCache'] = from_cache

        url = "".join([self.endpoint, 'analyze'])
        try:
            response = requests.get(url, params=payload).json()

            if response['status'] in ["DNS", "ERROR"]:
                logging.exception("An error occurred, received %s" % response['status'])

            elif response['status'] == "IN_PROGRESS":
                logging.debug("scan in progress ... ")
                payload.pop('startNew')
                while response['status'] == 'IN_PROGRESS':
                    logging.debug("checking if done")
                    time.sleep(self.default_wait_time)
                    response = requests.get(url, params=payload).json()

            elif response['status'] == "READY":
                logging.info("scan success")

        except requests.RequestException:
            logging.exception('Request failed.')
            sys.exit(1)

        return response
