import os
from urllib.parse import urljoin
from bson import ObjectId
from bson.errors import InvalidId
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri
from django.conf import settings
from gridfs import GridFS, NoFile
from pymongo import MongoClient


__all__ = ('GridFSStorage',)


def _get_subcollections(collection):
    """
    Returns all sub-collections of `collection`.
    """
    # XXX: Use the MongoDB API for this once it exists.
    for name in collection.database.collection_names():
        cleaned = name[:name.rfind('.')]
        if cleaned != collection.name and cleaned.startswith(collection.name):
            yield cleaned


@deconstructible
class GridFSStorage(Storage):
    default_url = 'mongodb://127.0.0.1:27017'

    def __init__(self, location='', default_url='', collection='storage', base_url='/media/'):
        self.location = location.strip(os.sep)
        self.collection = collection
        self.default_url = default_url or getattr(settings, 'GRIDFS_URL', self.default_url)
        self.base_url = base_url

        if not self.collection:
            raise ImproperlyConfigured("'collection' may not be empty.")

        if self.base_url and not self.base_url.endswith('/'):
            raise ImproperlyConfigured("If set, 'base_url' must end with a slash.")

    def get_file_name(self, oid):
        return self.fs.get(ObjectId(oid)).filename

    def _open(self, path, mode='rb'):
        """
        Returns a :class:`~gridfs.GridOut` file opened in `mode`, or
        raises :exc:`~gridfs.errors.NoFile` if the requested file
        doesn't exist and mode is not 'w'.
        """
        gridfs, filename = self._get_gridfs(path)
        try:
            return gridfs.get_last_version(filename)
        except NoFile:
            if 'w' in mode:
                return gridfs.new_file(filename=filename)
            else:
                raise

    def _save(self, path, content):
        """
        Saves `content` into the file at `path`.
        """
        gridfs, filename = self._get_gridfs(path)
        gridfs.put(content, filename=filename, contentType=content.content_type)
        return path

    def delete(self, path):
        """
        Deletes the file at `path` if it exists.
        """
        gridfs, filename = self._get_gridfs(path)
        try:
            gridfs.delete(gridfs.get_last_version(filename=filename).__getattribute__('_id'))
        except NoFile:
            pass

    def exists(self, path):
        """
        Returns `True` if the file at `path` exists in GridFS.
        """
        gridfs, filename = self._get_gridfs(path)
        return gridfs.exists(filename=filename)

    def listdir(self, path):
        """
        Returns a tuple (folders, lists) that are contained in the
        folder `path`.
        """
        gridfs, filename = self._get_gridfs(path)
        assert not filename
        subcollections = _get_subcollections(gridfs.__getattribute__('__collection'))
        return set(c.split('.')[-1] for c in subcollections), gridfs.list()

    def size(self, path):
        """
        Returns the size of the file at `path`.
        """
        gridfs, filename = self._get_gridfs(path)
        return gridfs.get_last_version(filename=filename).length

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        gridfs, filename = self._get_gridfs(name)
        try:
            file_oid = gridfs.get_last_version(filename=name).__getattr__('_id')
        except NoFile:
            # In case not found by filename
            try:
                # Check is a valid ObjectId
                file_oid = ObjectId(name)
            except (InvalidId, TypeError, ValueError):
                return None
            # Check if exist a file with that ObjectId
            if not gridfs.exists(file_oid):
                return None
        return urljoin(self.base_url, filepath_to_uri(str(file_oid)))

    def created_time(self, path):
        """
        Returns the datetime the file at `path` was created.
        """
        gridfs, filename = self._get_gridfs(path)
        return gridfs.get_last_version(filename=filename).upload_date

    def _get_gridfs(self, path):
        """
        Returns a :class:`~gridfs.GridFS` using the sub-collection for
        `path`.
        """
        path, filename = os.path.split(path)
        path = os.path.join(self.collection, self.location, path.strip(os.sep))
        collection_name = path.replace(os.sep, '.').strip('.')

        if not hasattr(self, '_db'):
            self._db = MongoClient(self.default_url)[self.collection]

        return GridFS(self._db, collection_name), filename

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        return self.created_time(name)

    def get_modified_time(self, name):
        pass

    def path(self, name):
        pass
