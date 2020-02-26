import django
import jsonschema
from django.core.validators import BaseValidator


class JSONSchemaValidator(BaseValidator):
    def compare(self, a, b):
        try:
            jsonschema.validate(a, b)
        except jsonschema.exceptions.ValidationError as e:
            raise django.core.exceptions.ValidationError(e)
