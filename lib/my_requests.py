import allure
import requests
from lib.logger import Logger
from configuration import BASE_URL


class MyRequests:
    @staticmethod
    def get(uri: str, params: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL '{BASE_URL}{uri}'"):
            return MyRequests._send(uri, params, headers, cookies, "GET")

    @staticmethod
    def post(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL '{BASE_URL}{uri}'"):
            return MyRequests._send(uri, data, headers, cookies, "POST")

    @staticmethod
    def put(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL '{BASE_URL}{uri}'"):
            return MyRequests._send(uri, data, headers, cookies, "PUT")

    @staticmethod
    def delete(uri: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL '{BASE_URL}{uri}'"):
            return MyRequests._send(uri, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(uri: str, data: dict, headers: dict, cookies: dict, method: str):
        url = f"{BASE_URL}{uri}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url=url, data=data, headers=headers, cookies=cookies, method=method)

        if method == "GET":
            response = requests.get(url=url, params=data, headers=headers, cookies=cookies)
        elif method == "POST":
            response = requests.post(url=url, data=data, headers=headers, cookies=cookies)
        elif method == "PUT":
            response = requests.put(url=url, data=data, headers=headers, cookies=cookies)
        elif method == "DELETE":
            response = requests.delete(url=url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response=response)

        return response
