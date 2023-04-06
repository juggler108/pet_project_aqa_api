import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Register user cases")
class TestUserRegister(BaseCase):
    @allure.description("This test check creating user successfully")
    def test_create_user_successful(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test check creating user with existing email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("https://playground.learnqa.ru/api/user/", data=data)
        content = response.content.decode("utf-8")
        Assertions.assert_code_status(response, 400)
        assert content == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"
