from django.urls import re_path
from .views import ServeMediaView


app_name = 'gridfs_storage'
urlpatterns = [
    re_path(r'^(?P<file_path>.*)/$', ServeMediaView.as_view(), name='media_url')
]
