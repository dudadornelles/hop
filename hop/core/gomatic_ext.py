import json
import requests


class SecureHostRestClient(object):
    def __init__(self, host, username=None, password=None, ssl=False, verify_ssl=True):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__ssl = ssl
        self.__verify_ssl = verify_ssl

    def __repr__(self):
        return 'HostRestClient("{0}", ssl={1})'.format(self.__host, self.__ssl)

    def __path(self, path):
        http_prefix = 'https://' if self.__ssl else 'http://'
        return '{0}{1}{2}'.format(http_prefix, self.__host, path)

    def __auth(self):
        return (self.__username, self.__password) if self.__username or self.__password else None

    def get(self, path):
        return requests.get(self.__path(path), auth=self.__auth(), verify=self.__verify_ssl)

    def post(self, path, data):
        url = self.__path(path)
        result = requests.post(url, data, auth=self.__auth(), verify=self.__verify_ssl)
        if result.status_code != 200:
            try:
                result_json = json.loads(result.text.replace("\\'", "'"))
                message = result_json.get('result', result.text)
                raise RuntimeError("Could not post config to Go server (%s) [status code=%s]:\n%s" % (
                    url, result.status_code, message))
            except ValueError:
                raise RuntimeError(
                    "Could not post config to Go server (%s) [status code=%s] (and result was not json):\n%s" % (
                        url, result.status_code, result))
