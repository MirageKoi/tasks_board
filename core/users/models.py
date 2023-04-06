from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    
    def __str__(self):
        return self.username


# from django.conf import settings
# from django.db import models
# from rest_framework.authtoken.models import Token as AuthToken


# class Token(AuthToken):
#     key = models.CharField("Key", max_length=40, db_index=True, unique=True)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name="auth_token",
#         on_delete=models.CASCADE,
#         verbose_name="User",
#     )
