from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('archive/', views.archive, name='archive'),
    path('email/', views.email, name='email'),
    path('data-log/', views.data_log, name='data_log'),
    path('albums/', views.albums, name='albums'),
    path('notepad/', views.notepad, name='notepad'),
    path('heart/', views.heart, name='heart'),
    path('send-email/', views.send_email, name='send_email'),
    path('archive/email/', views.archive_email, name='archive_email'),
    path('archive/photo/', views.archive_photo, name='archive_photo'),
    path('archive/message/', views.archive_message, name='archive_message'),
    path('archive/emotion/', views.archive_emotion, name='archive_emotion'),
    path('archive/days/', views.archive_days, name='archive_days'),
]