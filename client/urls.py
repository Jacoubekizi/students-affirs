from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('auth/sigin/', SignUpView.as_view(), name='sigin'),
    path('auth/verify-account/<str:pk>/', VerifyAccount.as_view(), name='verify-account'),
    path('auth/login/' , LoginUser.as_view() , name="login"),
    path('auth/logout/', LogoutUser.as_view(), name='logout'),
    path('auth/send-code/' , SendCodePassword.as_view() , name="send-code"),
    path('auth/verify-code/<str:pk>/' , VerifyCode.as_view() , name="verify-code"),
    path('auth/reset-password/<str:user_id>/' , ResetPassword.as_view(), name='reset-password'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # ------------------------------------------------
    path('create-objection/', CreateObjectionView.as_view(), name='create-objection'),
    path('list-objection/', CreateObjectionView.as_view(), name='list-objection'),
    path('get-upt-des-objection/<str:pk>/', RetUpdDesObjectionView.as_view(), name='ret-upt-des-objection'),
    path('list-refusel-objection/', RefuselObjectionView.as_view(), name='get-refuesl-boj'),

    # choice subject
    path('list-create-choice-subject/', CreateChoiceSubjectView.as_view(), name='list-create-choice-subject'),
    path('get-upt-des-shoice-subject/<str:pk>/', RetUpdDesObjectionView.as_view()),

    # Posters
    path('list-posters/', ListPostersView.as_view(), name='list-posters'),
    path('get-poster/<str:pk>/', GetPosterView.as_view(), name='get-poster'),
    path('list-notification/', ListNotificationView.as_view(), name='list-notification'),
    path('get-notification/<str:pk>/', GetNotificationView.as_view(), name='get-notification'),
]
