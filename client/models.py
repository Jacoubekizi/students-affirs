from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as FirebaseNotification
from .utils import *
from .options import *

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    phonenumber = PhoneNumberField(region='SY')
    image = models.ImageField(upload_to='images/users',default='images/account. ')
    univercity_id = models.IntegerField(default=12, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    # type_verified = models.CharField(max_length=30, choices=TypeVerified)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','phonenumber')

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = _("User")
        verbose_name_plural = _("Users")

class Employee(models.Model):
    employee = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.employee.username

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_subject = models.CharField(max_length=20, choices=TypeSubject)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, choices=Year)
    department = models.CharField(max_length=20, choices=Department, null=True, blank=True)
    subject = models.CharField(max_length=40)
    teacher = models.CharField(max_length=40)
    payment = models.ImageField(upload_to='objection/payment') #new
    is_processed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.type_subject}-{self.subject}-اعتراض'

# class RefuselObjection(models.Model):
#     objection = models.OneToOneField(Objection, on_delete=models.CASCADE)
#     reason = models.CharField(max_length=10000)

#     def __str__(self) -> str:
#         return f'{self.objection.subject} على مادة {self.objection.user.username}طلب اعتراض مرفوض باسم'
    
#     def save(self, *args, **kwargs) -> None:
#         self.objection.is_refusel = True
#         self.objection.save()
#         super().save(*args, **kwargs)
    

class ShoiceSubject(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, choices=Year)
    department = models.CharField(max_length=20, choices=Department, null=True, blank=True)
    subject = models.CharField(max_length=40)
    is_processed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.year}-{self.subject}'
    

class Poster(models.Model):
    description = models.TextField()

    def save(self,*args, **kwargs) -> None:
        super().save(*args, **kwargs)
        title = 'اعلان'
        content = 'تم اضافة اعلان جديد انقر للاطلاع على تاتفاصيل'
        users = CustomUser.objects.all()
        noti = Notification.objects.create(poster = self, title=title, content=content)
        for user  in users:
            noti.user.add(user)
            noti.save()
            devices = FCMDevice.objects.filter(user=user.id)
            devices.send_message(
                message=Message(
                    notification=FirebaseNotification(
                        title=title,
                        body=content
                    ),
                ),
            )
    def __str__(self) -> str:
        return f'{self.id}-إعلان'
    
class Notification(models.Model):
    user = models.ManyToManyField(CustomUser)
    poster = models.OneToOneField(Poster, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        for user in self.user.all():
            return self.title
        
class RePractical(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, choices=Year)
    department = models.CharField(max_length=20, choices=Department, null=True, blank=True)
    subject = models.CharField(max_length=40)
    image_id_front = models.ImageField(upload_to='re_practical/image_id_front', default='image.png') #new
    image_id_back = models.ImageField(upload_to='re_practical/image_id_back', default='image.png') #new
    is_processed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.department}-{self.year}-{self.user.username}إعادة عملي'
    
class Permanence(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, choices=Year)
    department = models.CharField(max_length=20, choices=Department, null=True, blank=True)
    image_id_front = models.ImageField(upload_to='permanence/image_id_front')
    image_id_back = models.ImageField(upload_to='permanence/image_id_back')
    image_university = models.ImageField(upload_to='permanence/university')
    is_processed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.year}-{self.user.username}- وثيقة دوام'
    
class Deferment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, choices=Year)
    department = models.CharField(max_length=20, choices=Department, null=True, blank=True)
    image_id_front = models.ImageField(upload_to='defement/image_id_front')
    image_id_back = models.ImageField(upload_to='defement/image_id_back')
    image_university = models.ImageField(upload_to='defement/university')
    photograph = models.ImageField(upload_to='defement/photograph')
    is_processed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.year}-{self.user.username}- مصدقة تأجيل'
    
# class ReCorrection(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class RequestDegree(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username}-كشف علامات'

class RequestDegreeTransitional(models.Model):
    request_degree = models.ForeignKey(RequestDegree, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, choices=Year)
    department = models.CharField(max_length=20, choices=Department, null=True, blank=True)
    payment = models.ImageField(upload_to='request_degree/payemnt')
    image_id_front = models.ImageField(upload_to='request_degree_graduation/image_id_front', blank=True, null=True)
    image_id_back = models.ImageField(upload_to='request_degree_graduation/image_id_back', blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.request_degree.user.username}-كشف علامات مرحلة انتقالية'

class RequestDegreeGraduation(models.Model):
    request_degree = models.ForeignKey(RequestDegree, on_delete=models.CASCADE)
    payment = models.ImageField(upload_to='request_degree/payemnt')
    image_id_front = models.ImageField(upload_to='request_degree_graduation/image_id_front', blank=True, null=True)
    image_id_back = models.ImageField(upload_to='request_degree_graduation/image_id_back', blank=True, null=True)
    passport = models.ImageField(upload_to='request_degree_graduation/passport', blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.request_degree.user.username}-كشف علامات تخرج'