# django-gridfs-storage

### Simple django GridFS storage engine


## Usage:
<ol>
<li> Install <code>django_gridfs_storage</code>:

```
pip install django_gridfs_storage
```
</li>
<li> Into settings.py file of your project, add <code>gridfs_storage</code> to <code>INSTALLED_APPS</code>:

```python
INSTALLED_APPS = [
    ...,
    'gridfs_storage',
]
```
</li>   
<li> add the following variables to your settings:

```python
# defaults to default local mongodb server
DEFAULT_GRIDFS_URL = 'mongodb://127.0.0.1:27017' 
# if set to None, it will refuse to serve files and raise an Exception
DEFAULT_GRIDFS_SERVE_URL = None  
DEFAULT_COLLECTION = 'storage'
```
</li>
<li> To serve files through django (not recommended) you can use this in urls.py:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    ...,
    path('media/', include('gridfs_storage.urls')),
]
```
and set the <code>DEFAULT_GRIDFS_SERVE_URL</code> to the prefix you specified in the path. in this case its <code>/media/</code>
</li>

<li> If you wish to use it on all <code>FileField</code> and <code>ImageField</code> set it as the default Storage:

```python
DEFAULT_FILE_STORAGE = 'gridfs_storage.storages.GridFSStorage'
```
</li>

<li> If you wish to use on individual field bases set it as the field storage:

```python
from django.db import models
from gridfs_storage.storages import GridFSStorage

class SampleModel(models.Model):
    attachment = models.FileField(storage=GridFSStorage())
    first_pic = models.ImageField(storage=GridFSStorage(location='sample/images'))
    
    # To store in a different collection than "storage"
    another_pic = models.ImageField(storage=GridFSStorage(collection='image_storage'))
    
    # Serve through custom cdn connected to the same gridfs or similar, the limit is the sky :)
    served_outside = models.ImageField(storage=GridFSStorage(base_url='https://img.cdn/serve/'))
```
</li>
</ol>

## Requirements:

  1. Python 3.6 or higher.
  2. Django 2.2 or higher.
  3. MongoDB 3.4 or higher.


## Known Issues

    # TODO: location has a problem, fix it
    # TODO: upload doens't work outside of admin