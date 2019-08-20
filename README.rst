=============================
Citixen Authorization
=============================

A simple application to manage the authorization system in general.

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
