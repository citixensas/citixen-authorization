import django
import jsonschema
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, EmailValidator
from django.utils.deconstruct import deconstructible
from django.utils.encoding import punycode
from tld import get_tld
from tld.exceptions import TldDomainNotFound


class JSONSchemaValidator(BaseValidator):
    def compare(self, a, b):
        try:
            jsonschema.validate(a, b)
        except jsonschema.exceptions.ValidationError as e:
            raise django.core.exceptions.ValidationError(e)


class CorexenEmailValidator(EmailValidator):

    def __init__(self, message=None, code=None, whitelist=None):
        super(CorexenEmailValidator, self).__init__(
            message=message,
            code=code,
            whitelist=whitelist)

    def __call__(self, value):
        if not value or '@' not in value:
            raise ValidationError(self.message, code=self.code)

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code)

        if domain_part not in self.domain_whitelist:
            if not self.validate_domain_part(domain_part):
                # Try for possible IDN domain-part
                try:
                    domain_part = punycode(domain_part)
                except UnicodeError:
                    pass
                else:
                    if self.validate_domain_part(domain_part):
                        self.validate_domain_tld(domain_part)
                        return
                raise ValidationError(self.message, code=self.code)
            self.validate_domain_tld(domain_part)

    def validate_domain_tld(self, domain_part):
        try:
            get_tld(domain_part, fix_protocol=True)
        except TldDomainNotFound:
            raise ValidationError(self.message, code=self.code)
