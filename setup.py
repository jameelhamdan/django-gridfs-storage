import os

from setuptools import setup

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
README = open(os.path.join(ROOT_DIR, 'README.md')).read()
VERSION = open(os.path.join(ROOT_DIR, 'version.txt')).read()


setup(
    name='django-gridfs-storage',
    version=VERSION,
    packages=['gridfs_storage'],
    url='https://github.com/kingjmk/django-gridfs-storage',
    license='MIT',
    author='Jameel Hamdan',
    author_email='jameelhamdan99@yahoo.com',
    description='Django GridFS Storage Engine',
    include_package_data=True,
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'django',
        'pymongo>=3.11.0',
    ],
    python_requires=">3.6",
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
)
