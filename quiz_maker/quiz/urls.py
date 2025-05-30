from django.urls import path
from . import views


urlpatterns = [
    path('', views.upload_file, name="upload_file"),
    path('start/<int:question_id>/', views.start_quiz, name="start_quiz"),
    path('result/', views.result, name="result"),
]