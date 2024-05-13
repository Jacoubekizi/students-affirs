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
    path('update-image/', UpdateImagteView.as_view(), name='update-image'),
    path('update-email/', UpdateEmailView.as_view(), name='update-email'),
    path('get-info-user/', RetrieveInfoUser.as_view(), name='get-info-user'),

    # ------------------------------------------------
    path('create-objection/', CreateObjectionView.as_view(), name='create-objection'),
    path('list-objection/', CreateObjectionView.as_view(), name='list-objection'),
    path('get-upt-des-objection/<str:pk>/', RetUpdDesObjectionView.as_view(), name='ret-upt-des-objection'),
    # path('list-refusel-objection/', RefuselObjectionView.as_view(), name='get-refuesl-boj'),

    # choice subject
    path('list-create-choice-subject/', CreateChoiceSubjectView.as_view(), name='list-create-choice-subject'),
    path('get-upt-des-shoice-subject/<str:pk>/', RetUpdDesShoiceSubjectView.as_view()),

    # Posters
    path('list-posters/', ListPostersView.as_view(), name='list-posters'),
    path('get-poster/<str:pk>/', GetPosterView.as_view(), name='get-poster'),
    path('list-notification/', ListNotificationView.as_view(), name='list-notification'),
    path('get-notification/<str:pk>/', GetNotificationView.as_view(), name='get-notification'),

    # Re Practical
    path('list-create-re-practical/', ListCreateRePracticalView.as_view(), name='list-create-re-practical'),
    path('ret-upt-des-re-practical/<str:pk>/', RetUptDesRePracticalView.as_view(), name='ret-upt-des-re-practical'),

    # Permanence
    path('list-create-permanence/', ListCreatePermanenceView.as_view(), name='list-create-permanence'),
    path('ret-upt-des-permanence/<str:pk>/', RetUptDesPermanenceView.as_view(), name='ret-upt-des-permanence'),

    # Deferment
    path('list-create-deferment/', ListCreateDefermentView.as_view(), name='list-create-deferment'),
    path('ret-upt-des-deferment/<str:pk>/', RetUptDesDefermentView.as_view(), name='ret-upt-des-deferment'),

    # Request Degree Graduation
    path('list-create-request-degree-graduation/', ListCreateRequestDegreeGraduationView.as_view(), name='list-create-request-degree-graduation'),
    path('ret-upt-des-degree-graduation/<str:pk>/', RetUpdDesRequestDegreeGraduationView.as_view(), name='ret-upt-des-degree-graduation'),

    # Request Degree Transitional
    path('list-create-request-degree-transitional/', ListCreateRequestDegreeTransitionalView.as_view(), name='list-create-request-degree-transitional'),
    path('ret-upt-des-degree-transitional/<str:pk>/', RetUpdDesRequestDegreeTransitionalView.as_view(), name='ret-upt-des-degree-transitional'),
]
