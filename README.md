=============================
Citixen Authorization
=============================

A simple application to manage the authorization system in general.

[![Build Status](https://travis-ci.org/citixensas/citixen-authorization.svg?branch=master)](https://travis-ci.org/citixensas/citixen-authorization)

Documentation
-------------

The full documentation is at https://citixen-authorization.readthedocs.io.

Quickstart
----------

Install Citixen Authorization::

    pip install citixen-authorization

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'companies.apps.CompaniesConfig',
        ...
    )

Add Citixen Authorization's URL patterns:

.. code-block:: python

    from companies import urls as companies_urls


    urlpatterns = [
        ...
        url(r'^', include(companies_urls)),
        ...
    ]


Features
--------

* Companies and headquarters

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


BumpVersion
-----------

bumpversion [major|minor|patch]

$ cat VERSION
0.0.0
$ bumpversion major; cat VERSION
1.0.0-dev0
$ bumpversion minor; cat VERSION
1.1.0-dev0
$ bumpversion patch; cat VERSION
1.1.1-dev0
$ bumpversion build; cat VERSION
1.1.1-dev1
$ bumpversion build; cat VERSION
1.1.1-dev2
$ bumpversion --tag release; cat VERSION
1.1.1
$ bumpversion minor; cat VERSION
1.2.0-dev0

docker-compose -f .\develop.yml run --rm corexen_develop.django bumpversion --tag release
docker-compose -f .\develop.yml run --rm corexen_develop.django bumpversion patch
