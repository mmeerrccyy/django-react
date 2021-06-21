from django.urls import path
from .views import Index

app_name = 'frontend'


urlpatterns = [
    path('', Index.as_view(), name=''),
    path('info', Index.as_view()),
    path('join/', Index.as_view()),
    path('create/', Index.as_view()),
    path('room/<str:roomCode>', Index.as_view()),
]
