import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserModel(AbstractBaseUser):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=Gender.MALE)
    date_of_birth = models.DateField()

    USERNAME_FIELD=("email")

    def __str__(self):
        return self.username
