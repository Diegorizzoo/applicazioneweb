from django.urls import path
from . import views

urlpatterns = [
    path('backend', views.backend, name='backend'),
    path('quiz', views.quiz, name='quiz'),
    path('quiz_complete', views.quiz_complete, name='quiz_complete')
]