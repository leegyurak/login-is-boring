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


@pytest.mark.django_db
class TestEmailVerifyView:

    @pytest.fixture(autouse=True)
    def setUpClass(self):
        self.url = '/v1/accounts/email-verify'
        self.deactive_user = baker.make(
            User, username='테스트', email='test1@test.devgyurak', 
            nickname='미인증 테스트 유저', verify_code='000000', active_type_id=UserActiveType.TYPES.DEACTIVE.value
        )
        self.active_user = baker.make(
            User, username='테스트', email='test2@test.devgyurak', 
            nickname='인증 테스트 유저', active_type_id=UserActiveType.TYPES.ACTIVE.value
        )

        yield

        User.objects.all().delete()

    def test_존재하지않는유저이메일인증(self, client):
        payload = {
            'verify_code': '000000'
        }

        response = client.post(
            f'{self.url}?email=test@test.devgyurak',
            payload,
            content_type='application/json'
        )

        assert response.status_code == 404

    def test_유저이메일인증(self, client):
        payload = {
            'verify_code': '000000'
        }

        response = client.post(
            f'{self.url}?email={self.deactive_user.email}',
            payload,
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_이미인증된유저이메일인증(self, client):
        payload = {
            'verify_code': '000000'
        }

        response = client.post(
            f'{self.url}?email={self.active_user.email}',
            payload,
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_잘못된인증번호로인증시도(self, client):
        payload = {
            'verify_code': '000001'
        }

        response = client.post(
            f'{self.url}?email={self.deactive_user.email}',
            payload,
            content_type='application/json'
        )

        assert response.status_code == 400


@pytest.mark.django_db
class TestLoginView:

    @pytest.fixture(autouse=True)
    def setUpClass(self):
        self.url = '/v1/accounts/login'
        self.deactive_user = baker.make(
            User, username='미인증', email='test1@test.devgyurak',
            active_type_id=UserActiveType.TYPES.DEACTIVE.value
        )
        self.active_user = baker.make(
            User, username='인증', email='test2@test.devgyurak',
            active_type_id=UserActiveType.TYPES.ACTIVE.value
        )

        self.deactive_user.set_password('test123!')
        self.active_user.set_password('test123!')

        self.deactive_user.save()
        self.active_user.save()

        yield

        User.objects.all().delete()

    def test_존재하지않는계정로그인(self, client):
        payload = {
            'email': 'test@test.devgyurak',
            'password': 'test123!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        assert response.status_code == 404

    def test_미인증유저로그인(self, client):
        payload = {
            'email': 'test1@test.devgyurak',
            'password': 'test123!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_잘못된비밀번호로그인(self, client):
        payload = {
            'email': 'test1@test.devgyurak',
            'password': 'test123!!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_로그인(self, client):
        payload = {
            'email': 'test2@test.devgyurak',
            'password': 'test123!'
        }

        response = client.post(
            self.url,
            payload,
            content_type='application/json'
        )

        body = response.json()

        assert response.status_code == 200
        assert body.get('access_token') is not None
        assert body.get('refresh_token') is not None