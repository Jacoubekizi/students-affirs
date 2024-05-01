from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "شؤون الطلاب"
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_verified', 'username']

class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'is_verified']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)

admin.site.register(Chapter)
admin.site.register(Objection)