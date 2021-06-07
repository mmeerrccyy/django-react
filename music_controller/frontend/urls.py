from django.urls import path
from .views import Index


urlpatterns = [
    path('', Index.as_view()),
    path('join/', Index.as_view()),
    path('create/', Index.as_view()),
]
