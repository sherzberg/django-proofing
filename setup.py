#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

# Dynamically calculate the version based on photologue.VERSION
version_tuple = __import__('proofing').VERSION
if len(version_tuple) == 3:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
    name = "django-proofing",
    version = version,
    description = "Wonderful photo proofing/gallery management for Django.",
    author = "Spencer Herzberg",
    author_email = "spencer.herzberg@gmail.com",
    url = "https://github.com/whelmingbytes/django-proofing",
    packages = find_packages(),
    package_data = {
        'proofing': [
            'res/*.jpg',
            'locale/*/LC_MESSAGES/*',
            'templates/proofing/*.html',
            'templates/proofing/tags/*.html',
        ]
    },
    zip_safe = False,
#    classifiers = ['Development Status :: 1 - Production/Stable',
#                   'Environment :: Web Environment',
#                   'Framework :: Django',
#                   'Intended Audience :: Developers',
#                   'License :: OSI Approved :: BSD License',
#                   'Operating System :: OS Independent',
#                   'Programming Language :: Python',
#                   'Topic :: Utilities'],
)