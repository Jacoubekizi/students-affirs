from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

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

    actions = ['set_permission_for_employee']
    def set_permission_for_employee(self, request, queryset):
        user_id = queryset.update(is_employee=True)
        user = CustomUser.objects.get(id=user_id)
        Employee.objects.create(employee=user)
        group = Group.objects.get(name='employee')        
        group.user_set.add(user)
        return group


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

    list_display = ['user', 'user_id','type_subject', 'chapter', 'subject', 'teacher', 'is_processed']

    def user_id(self, obj):
        return obj.user.univercity_id

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

    search_fields = ['user__username', 'user__univercity_id']
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

    list_display = ['user', 'user_id', 'year', 'department', 'subject', 'is_processed']

    def user_id(self, obj):
        return obj.user.univercity_id

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'year', 'department', 'subject', 'is_processed')}
        ),
    )
    
    search_fields = ['user__username', 'subject', 'year', 'user__univercity_id']
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

    list_display = ['user', 'user_id', 'year', 'department', 'subject', 'is_processed']

    def user_id(self, obj):
        return obj.user.univercity_id
    
    search_fields = ['user__username', 'user__univercity_id', 'subject']
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

    list_display = ['user', 'user_id', 'year', 'department', 'image_id_front', 'image_id_back', 'image_university', 'is_processed']
    search_fields = ['user_username']

    def user_id(self, obj):
        return obj.user.univercity_id
    
    list_per_page = 25

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'year', 'department', 'image_id_front', 'image_id_back', 'image_university', 'is_processed')}
        ),
    )

    list_filter = ['is_processed']
    search_fields = ['user__username', 'user__univercity_id']

class DefermentAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['user','user_id', 'year', 'department', 'image_id_front', 'image_id_back', 'image_university', 'photograph', 'is_processed']
    search_fields = ['user__username']
    list_per_page = 25

    def user_id(self, obj):
        return obj.user.univercity_id
    
    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('user', 'year', 'department', 'image_id_front', 'image_id_back', 'image_university', 'photograph', 'is_processed')}
        ),
    )

    list_filter = ['is_processed']

class RequestDegreeGraduationAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['request_degree', 'user_id', 'payment', 'image_id_front', 'image_id_back', 'passport', 'is_processed']

    def user_id(self, obj):
        return obj.request_degree.user.univercity_id
    
    search_fields = ['request_degree__user__username', 'request_degree__user__univercity_id']
    list_per_page = 25

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('request_degree', 'payment', 'image_id_front', 'image_id_back', 'passport', 'is_processed')}
        ),
    )

    list_filter = ['is_processed']


class RequestDegreeTransitionalAdmin(admin.ModelAdmin):

    actions = ['processed']
    def processed(self, request, queryset):
        queryset.update(is_processed=True)

    list_display = ['request_degree', 'user_id', 'department', 'payment', 'image_id_front', 'image_id_back', 'is_processed']

    def user_id(self, obj):
        return obj.request_degree.user.univercity_id
    
    search_fields = ['request_degree__user__username', 'request_degree__user__univercity_id']
    list_per_page = 25

    fieldsets = (
        ('Information',
            {
                'classes':('wide',),
                'fields':('request_degree', 'payment', 'image_id_front', 'image_id_back', 'is_processed')}
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
admin.site.register(RequestDegreeGraduation, RequestDegreeGraduationAdmin)
admin.site.register(RequestDegreeTransitional, RequestDegreeTransitionalAdmin)
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
post_admin_site.register(RequestDegreeGraduation, RequestDegreeGraduationAdmin)
post_admin_site.register(RequestDegreeTransitional, RequestDegreeTransitionalAdmin)
post_admin_site.register(Employee)

# post_admin_site.register(RefuselObjection)



# admin.site.register(RequestDegree)