import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from configuration import REGISTERED_USER_DATA


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    def setup_method(self):
        data = REGISTERED_USER_DATA

        response1 = MyRequests.post(
            url="https://playground.learnqa.ru/api/user/login",
            data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id = self.get_json_value(response1, "user_id")

    @allure.description("This test check deleting registered user which can not be remove")
    def test_delete_registered_user(self):
        # DELETE
        response2 = MyRequests.delete(
            url=f"https://playground.learnqa.ru/api/user/{self.user_id}",
            cookies={"auth_sid": self.auth_sid},
            headers={"x-csrf-token": self.token}
        )
        Assertions.assert_message_about_deleting_registered_users(response2)

        # GET
        response3 = MyRequests.get(
            url=f"https://playground.learnqa.ru/api/user/{self.user_id}",
            cookies={"auth_sid": self.auth_sid},
            headers={"x-csrf-token": self.token}
        )
        Assertions.assert_json_value_by_name(
            response=response3,
            name="id",
            expected_value=str(self.user_id),
            error_message="User id from auth method is not equal to user id from check method. "
                          "User id was changed or deleted!"
        )

    @allure.description("This test check deleting just created user")
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(
            url=f"https://playground.learnqa.ru/api/user/",
            data=register_data
        )
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post(
            url="https://playground.learnqa.ru/api/user/login",
            data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            url=f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            url=f"https://playground.learnqa.ru/api/user/{user_id}"
        )
        Assertions.assert_code_status(response4, 404)
        Assertions.assert_user_not_found_message(response4)
