from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "شؤون الطلاب"
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_verified', 'username']

class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'is_verified']


class ObjectionAdmin(admin.ModelAdmin):
    # actions = ['refusal_objection']
    # list_display = ['reason', ]
    pass
    # def refusal_user(self, request, queryset):
    #     user = queryset.get(is_accepted=False)
    #     user.delete()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)

admin.site.register(Chapter)
admin.site.register(Objection, ObjectionAdmin)
admin.site.register(RefuselObjection)