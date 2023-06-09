import os
from datetime import datetime
from requests import Response


class Logger:
    file_name = f"logs/log_{str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))}.log"

    @classmethod
    def _write_log_to_file(cls, data: str):
        with open(cls.file_name, "a", encoding="utf-8") as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        test_name = os.environ.get("PYTEST_CURRENT_TEST")
        data_to_add = (
            f"\n-----\n"
            f"Test: {test_name}\n"
            f"Time: {str(datetime.now())}\n"
            f"Request method: {method}\n"
            f"Request URL: {url}\n"
            f"Request data: {data}"
            f"Request headers: {headers}"
            f"Request cookies: {cookies}\n"
        )
        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = (
            f"Response code: {response.status_code}\n"
            f"Response_text: {response.text}\n"
            f"Response header: {headers_as_dict}\n"
            f"Response cookies: {cookies_as_dict}"
            f"\n-----\n"
        )
        cls._write_log_to_file(data_to_add)
