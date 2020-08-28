from django.http import FileResponse, Http404
from django.views import View
from gridfs import NoFile
from .storage import GridFSStorage


class ServeMediaView(View):
    """
    Not a very efficient gridfs server, but it works.
    you should use another solution to serve gridfs files in production
    """

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        file_path = self.kwargs['file_path']
        try:
            return FileResponse(GridFSStorage()._open(file_path))
        except NoFile:
            raise Http404('File does not exist')
