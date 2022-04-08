"""Custom validators for flask form."""

from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,\
    SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf,\
    URL, ValidationError, Length
import re


class OptionalURL(URL):
    """Check the url syntaxt but only if the field is filled."""

    def __init__(self, message=None):
        """Instantiate the object."""
        super().__init__()
        if not message:
            message = "Invalid URL!"

        self.message = message

    def __call__(self, form, field):
        """Run when the object is calling."""
        if field.data:
            super().__call__(form, field)


class PhoneNumber(object):
    """Validate phone number (american format). 
    
    Only if the field is filled.
    """

    def __init__(self, message=None):
        """Instantiate the object."""
        super().__init__()
        if not message:
            message = "Valid format: `XXX-XXX-XXXX`."

        self.message = message

    def __call__(self, form, field):
        """Run when the object is calling."""
        pattern = re.compile(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$")

        if field.data:
            if len(field.data) != 12:
                raise ValidationError(self.message)

            if not bool(re.match(pattern, field.data)):
                raise ValidationError(self.message)

