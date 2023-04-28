from django.urls import path
from . import views

urlpatterns = [
    path('backend', views.backend, name='backend'),
    path('quiz', views.quiz, name='quiz'),
    path('quiz_complete', views.quiz_complete, name='quiz_complete'),
    path('register', views.register_view, name='register'),
    path('login',views.login_view,name='login'),
]