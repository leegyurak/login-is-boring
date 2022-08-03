from django.apps import AppConfig


class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'

def add_user_active_type_datas(apps, schema_editor):
    try:
        from db.models import UserActiveType

        for active_type in UserActiveType._TYPES:
            UserActiveType.objects.update_or_create(
                id=active_type.value,
                name=active_type.name,
                description=active_type.label
            )
            
    except Exception as e:
        print(e)