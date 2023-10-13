# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'userProfile'  # Set the app namespace

urlpatterns = [
    # Other URL patterns for your application
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-material/', views.add_material, name='add_material'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('meditate/', views.meditate, name='meditate'),
    path('scenario/', views.scenario_view, name='scenario_view'),
    path('scenario-feedback/', views.scenario_feedback_view, name='scenario_feedback_view'),
    path('journal/', views.journal, name='journal'),
    path("chatbot/",  views.chatbot, name='chatbot'),
    path("chatbot_qna/",  views.chatbot_qna, name='chatbot_qna'),
    path("fun-activity/",  views.activity, name='activity'),
    path("articles/",  views.articles, name='articles'),
    path("diagnose/",  views.diagnose, name='diagnose'),
    path('fitness/', views.fitness, name='fitness'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

