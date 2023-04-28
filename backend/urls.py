from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include


urlpatterns = [
    path('backend', views.backend, name='backend'),
    path('quiz', views.quiz, name='quiz'),
    path('quiz_complete', views.quiz_complete, name='quiz_complete'),
    path('register', views.register_view, name='register'),
    path('login',views.login_view,name='login'),
    path('api/addQuestion/', views.add_question, name='add_question'),
    path('api/answer/<int:id>/', views.answer_question, name='answer_question'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]