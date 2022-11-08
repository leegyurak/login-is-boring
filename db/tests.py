import pytest
from model_bakery import baker

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from db.models import UserActiveType


User = get_user_model()


@pytest.mark.django_db
class TestGetTokenMethod:
    
    @pytest.fixture(autouse=True)
    def setUpClass(self):
        self.active_user = baker.make(User, active_type_id=UserActiveType.TYPES.ACTIVE.value)
        self.deactive_user = baker.make(User, active_type_id=UserActiveType.TYPES.DEACTIVE.value)

        yield

        User.objects.all().delete()

    def test_인증된유저의토큰발급(self):
        token_obj = self.active_user.get_token()

        assert token_obj.get('access_token') is not None
        assert token_obj.get('refresh_token') is not None

    def test_인증되지않은유저의토큰발급(self):
        with pytest.raises(PermissionDenied):
            self.deactive_user.get_token()