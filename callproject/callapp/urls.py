from django.contrib import admin
from django.urls import path
from callapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('voice/', views.voice, name='voice'),
    path('static/hello.wav', views.serve_audio),  # for Twilio to fetch audio
]
