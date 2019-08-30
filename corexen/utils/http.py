import requests
from requests import ConnectTimeout, ConnectionError


class HTTPRequest(object):

    @classmethod
    def post(cls, url, data):
        response = []
        try:
            r = requests.post(url=url, data=data)
            status_code = r.status_code
            if status_code != 404:
                response = r.json()
        except ConnectTimeout:
            status_code = 503
        except ConnectionError:
            status_code = 503
        except Exception as e:
            status_code = 500
        return status_code, response

    @classmethod
    def get(cls, url):
        response = []
        try:
            r = requests.get(url=url)
            status_code = r.status_code
            if status_code != 404:
                response = r.json()
        except Exception:
            status_code = 500
        return status_code == 200, response
