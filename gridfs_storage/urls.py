from django.urls import path
from .views import ServeMediaView


app_name = 'gridfs_storage'
urlpatterns = [
    path('<str:object_id>', ServeMediaView.as_view(), name='media_url')
]
