# 로그인은 지루해
### 목적 🤔
프로젝트를 할 때 회원가입, 로그인 등 인증 절차를 매번 구현하는 것이 귀찮아서 이 불편함을 해소하고자 제작.

### 사용한 기술들 🔧
- [Django](https://www.djangoproject.com/) (메인 백엔드 프레임워크로 사용)
- [Django REST framework](https://www.django-rest-framework.org/) (Django 기반 REST API 제작을 위해 사용)
- [Celery](https://docs.celeryq.dev/en/stable/index.html) (비동기 처리를 위해 사용)
- [Redis](https://redis.io/) (Celery의 [Message broker](https://heodolf.tistory.com/49)로 사용)
