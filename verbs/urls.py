from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('quiz/', views.quiz, name='quiz'),
    # Simple quiz
    path('quiz/simple/', views.simple_quiz, name='simple_quiz'),
    path('quiz/simple/result/', views.quiz_result_simple, name='quiz_result_simple'),
    # Smart adaptive quiz
    path('quiz/smart/', views.smart_quiz, name='smart_quiz'),
    path('quiz/smart/result/', views.smart_quiz_result, name='smart_quiz_result'),
    # Old quiz system
    path('quiz/start/', views.start_quiz, name='start_quiz'),
    path('quiz/submit/', views.submit_answer, name='submit_answer'),
    path('quiz/result/', views.quiz_result, name='quiz_result'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-username/', views.change_username, name='change_username'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/change-avatar/', views.change_avatar, name='change_avatar'),
    path('verbs/', views.verbs_list, name='verbs_list'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
