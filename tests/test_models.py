#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_citixen-authorization
------------

Tests for `citixen-authorization` test_models module.
"""

from django.test import TestCase

from companies.models import Company


class TestCompanies(TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        company = Company.objects.create(name='Compañía de prueba')
        self.assertEqual('Compañía de prueba', company.__str__())
        assert True
