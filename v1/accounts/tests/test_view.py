import pytest
from model_bakery import baker

from django.contrib.auth import get_user_model

from db.models import UserActiveType


User = get_user_model()


@pytest.mark.django_db
class TestSignUpView:

    @pytest.fixture(autouse=True)
    def setUpClass(self):
        self.user = baker.make(
            User, username='테스트', email='test@test.devgyurak', 
            nickname='테스트 유저', active_type_id=UserActiveType.TYPES.DEACTIVE.value
        )
        self.url = '/v1/accounts/sign-up'

        yield

        User.objects.all().delete()

    def test_이메일이잘못된유저생성(self, client):
        payload = {
            'email': 'test@test',
            'username': '테스트',
            'nickname': '테스트 유저',
            'password': 'test777!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        assert response.status_code == 400
        assert response.json().get('email')[0] == '유효한 이메일 주소를 입력하십시오.'

    def test_중복된이메일유저생성(self, client):
        payload = {
            'email': 'test@test.devgyurak',
            'username': '테스트',
            'nickname': '테스트 유저',
            'password': 'test777!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        assert response.status_code == 400
        assert response.json().get('email')[0] == 'This email already exists.'

    def test_이름이잘못된유저생성(self, client):
        payload = {
            'email': 'test@test.gyurak',
            'username': '잘못된테스트',
            'nickname': '테스트 유저',
            'password': 'test!!!!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        assert response.status_code == 400
        assert type(response.json().get('username')) is list

    def test_비밀번호잘못된유저생성(self, client):
        payload = {
            'email': 'test@test.gyurak',
            'username': '테스트',
            'nickname': '테스트 유저',
            'password': 'test!!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        assert response.status_code == 400
        assert type(response.json().get('password')) is list

    def test_유저생성(self, client):
        payload = {
            'email': 'test@test.gyuraklee',
            'username': '테에스트',
            'nickname': '테스트 유저',
            'password': 'test777!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        created_user = User.objects.get(username='테에스트')

        assert response.status_code == 201
        assert len(created_user.verify_code) == 6
        assert created_user.active_type_id == UserActiveType.TYPES.DEACTIVE.value