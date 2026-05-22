from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class UserService:
    @staticmethod
    @transaction.atomic
    def create_user(email, password, **extra_fields):
        user = User.objects.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        return user
    
    @staticmethod
    def get_user_details(user):
        return user
    