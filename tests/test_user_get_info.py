import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from configuration import REGISTERED_USER_DATA


@allure.epic("Get info about users cases")
class TestUserGetInfo(BaseCase):
    @allure.description("This test check getting info about not authorization user")
    def test_get_user_info_not_auth(self):
        response = MyRequests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response=response, name="username")
        Assertions.assert_json_has_not_key(response=response, name="email")
        Assertions.assert_json_has_not_key(response=response, name="firstName")
        Assertions.assert_json_has_not_key(response=response, name="lastName")

    @allure.description("This test check getting details about authorization user")
    def test_get_user_details_auth_as_same_user(self):
        data = REGISTERED_USER_DATA

        response1 = MyRequests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            url=f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)
