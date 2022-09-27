# 로그인은 지루해
### 목적 🤔
프로젝트를 할 때 회원가입, 로그인 등 인증 절차를 매번 구현하는 것이 귀찮아서 이 불편함을 해소하고자 제작.

### 사용한 기술들 🔧
1. [Django](https://www.djangoproject.com/) (메인 백엔드 프레임워크로 사용)
2. [Django REST framework](https://www.django-rest-framework.org/) (Django 기반 REST API 제작을 위해 사용)
3. [Celery](https://docs.celeryq.dev/en/stable/index.html) (비동기 처리를 위해 사용)
4. [Redis](https://redis.io/) (Celery의 [Message broker](https://heodolf.tistory.com/49)로 사용)
5. [Swagger](https://swagger.io/) (API 문서 및 API 테스트를 위해 사용)
6. [Pytest](https://docs.pytest.org/en/7.1.x/) (테스트코드를 작성하기 위해 사용)

### 테스트 커버리지 🧮
2022.09.27 main branch에 merge된 PR 기준 **96%**

![스크린샷 2022-09-27 오후 10 22 46](https://user-images.githubusercontent.com/62545703/192538355-64619070-8c80-413b-9381-3940bbd08d12.png)
