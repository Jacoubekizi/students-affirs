from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from .utils import *
from .options import *

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    phonenumber = PhoneNumberField(region='SY')
    image = models.ImageField(upload_to='images/users',default='images/account. ')
    univercity_id = models.IntegerField(default=12, unique=True)
    is_verified = models.BooleanField(default=False)
    # type_verified = models.CharField(max_length=30, choices=TypeVerified)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','phonenumber')

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = _("User")
        verbose_name_plural = _("Users")



class VerificationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def __str__(self):
        return f'{self.user.username} code:{self.code}'
    
class Chapter(models.Model):
    chapter = models.CharField(max_length=20)
    type_subject = models.CharField(max_length=40, choices=Type_Subject)
    created_at = models.DateField()
    end_at = models.DateField()

    def __str__(self) -> str:
        return f'{self.chapter} - {self.type_subject}'

class Objection(models.Model):
    name = models.CharField(max_length=20, default='اعتراض')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_subject = models.CharField(max_length=20, choices=TypeSubject)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, choices=Year)
    department = models.CharField(max_length=20, choices=Department, null=True, blank=True)
    subject = models.CharField(max_length=40)
    teacher = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.type_subject}-{self.subject}-{self.name}'