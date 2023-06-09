import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from configuration import REGISTERED_USER_DATA


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    def setup_method(self):
        data = REGISTERED_USER_DATA

        response1 = MyRequests.post(uri="/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("This test check successfully authorize user by email and password")
    def test_auth_user(self):
        response2 = MyRequests.get(
            uri="/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response=response2,
            name="user_id",
            expected_value=self.user_id_from_auth_method,
            error_message="User id from auth method is not equal to user id from check method"
        )

    @allure.description("This test check authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = MyRequests.get(
                uri="/user/auth",
                headers={"x-csrf-token": self.token},
            )
        else:
            response2 = MyRequests.get(
                uri="/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response=response2,
            name="user_id",
            expected_value=0,
            error_message=f"User is authorized with condition {condition}"
        )
