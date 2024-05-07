from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class PostAdminSite(admin.AdminSite):
    site_header = "Welcome To Admin Site"
    site_title = "Blog Admin"
    index_title = "Welcome To Admin Site"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.is_active and request.user.is_staff and request.user.is_employee

post_admin_site = PostAdminSite(name='post-admin')

class CustomUserAdmin(UserAdmin):

    actions = ['create_employee']
    def create_employee(self, request, queryset):
        user = queryset.get(is_employee=True)
        Employee.objects.create(employee=user)

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['username','id' ,'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
    (None, 
         {'fields':('email', 'password',)}
     ),
    ('User Information',
        {'fields':('username', 'first_name', 'last_name')}
    ),
    ('Permissions', 
        {'fields':('is_verified', 'is_staff', 'is_superuser', 'is_employee', 'is_active', 'groups','user_permissions')}
    ),
    ('Registration', 
        {'fields':('date_joined', 'last_login',)}
    )
    )
    add_fieldsets = (
        (None, {'classes':('wide',),
            'fields':(
                'email','username', 'password1', 'password2', 'is_staff', 'is_employee',
            )}
            ),
        )
    search_fields = ("email",)
    ordering = ("email",)
    list_filter = ['is_employee',]


class VerificationCodeAdmin(admin.ModelAdmin):

    list_display = ['user','id', 'is_verified', 'code']
    fieldsets = (
    ('User Information',
     
        {'classes':('wide',), 'fields':('user',)}
    ),
    ('Permissions',
        {'classes':('wide',),
         'fields':('is_verified','code')},

    ),
    )

    search_fields = ['user__username',]


class ObjectionAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['user', 'type_subject', 'chapter', 'subject', 'teacher', 'is_processed']

    fieldsets = (
        ('Objection Information',
            {
                'classes':('wide',),
                'fields':('name', 'type_subject', 'chapter', )}
        ),
        ('User Information',
            {
            'classes':('wide',),
            'fields':('user', 'year', 'department', 'subject', 'teacher', 'is_processed')},
        ),
    )

    search_fields = ['user__username']
    list_per_page = 25
    list_filter = ['is_processed']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'type_subject', 'end_at', 'created_at']

    fieldsets = (
        ('Chapter Information',
            {
                'classes':('wide',),
                'fields':('chapter', )}
        ),
        ('Type Subject Information',
            {
            'classes':('wide',),
            'fields':('type_subject', 'end_at', 'created_at')},
        ),
    )

    search_fields = ['chapter']

class PosterAdmin(admin.ModelAdmin):
    list_display = ['description',]

    fieldsets = (
        ('Poster Information',
            {
                'classes':('wide',),
                'fields':('description', )}
        ),
    )

    list_per_page = 25
    

class ShoiceSubjectAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['user', 'year', 'subject', 'is_processed']

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'year', 'subject', 'is_processed')}
        ),
    )
    
    search_fields = ['user__username', 'subject', 'year']
    list_per_page = 25
    list_filter = ['is_processed']

class NotificationAdmin(admin.ModelAdmin):

    list_display = ['poster', 'title', 'content']
    search_fields = ['user__username']

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'poster', 'title', 'content')}
        ),
    )
    list_per_page = 25

class RePracticalAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['user', 'year', 'department', 'subject', 'is_processed']
    search_fields = ['user', 'subject']
    list_per_page = 25

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'year', 'department', 'subject', 'is_processed')}
        ),
    )

    list_filter = ['is_processed']

class PermanenceAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['user', 'year', 'department', 'image_id', 'image_university', 'is_processed']
    search_fields = ['user_username']
    list_per_page = 25

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'year', 'department', 'image_id', 'image_university', 'is_processed')}
        ),
    )

    list_filter = ['is_processed']

class DefermentAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['user', 'year', 'department', 'image_id', 'image_university', 'photograph', 'is_processed']
    search_fields = ['user_username']
    list_per_page = 25

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'year', 'department', 'image_id', 'image_university', 'photograph', 'is_processed')}
        ),
    )

    list_filter = ['is_processed']
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Objection, ObjectionAdmin)
admin.site.register(Poster, PosterAdmin)
admin.site.register(ShoiceSubject, ShoiceSubjectAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(RePractical, RePracticalAdmin)
admin.site.register(Permanence, PermanenceAdmin)
admin.site.register(Deferment, DefermentAdmin)
admin.site.register(Employee)




post_admin_site.register(CustomUser, CustomUserAdmin)
post_admin_site.register(VerificationCode, VerificationCodeAdmin)
post_admin_site.register(Chapter, ChapterAdmin)
post_admin_site.register(Objection, ObjectionAdmin)
post_admin_site.register(Poster, PosterAdmin)
post_admin_site.register(ShoiceSubject, ShoiceSubjectAdmin)
post_admin_site.register(Notification, NotificationAdmin)
post_admin_site.register(RePractical, RePracticalAdmin)
post_admin_site.register(Permanence, PermanenceAdmin)
post_admin_site.register(Deferment, DefermentAdmin)
post_admin_site.register(Employee)

# post_admin_site.register(RefuselObjection)
