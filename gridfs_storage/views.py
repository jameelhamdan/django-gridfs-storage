from django.http import FileResponse
from django.views import View
from .storages import GridFSStorage


class ServeMediaView(View):
    """
    Not a very efficient gridfs server, but it works.
    you should use another solution to serve gridfs files in production
    """

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        object_id = self.kwargs['object_id']
        return FileResponse(GridFSStorage()._open(object_id))
