# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length

from rpihelper.services.logic import SystemctlCommands, get_services

__all__ = (
    'ServicesForm',
)


class ServicesForm(Form):
    service = TextField('Service name', validators=(
        DataRequired(),
        Length(min=1, max=20),
    ))
    command = SelectField('Command', choices=(
        (SystemctlCommands.START, 'Start',),
        (SystemctlCommands.STOP, 'Stop',),
        (SystemctlCommands.RESTART, 'Restart',),
    ))

    def validate_service(form, field):
        services_names = [
            service['name'] for service in get_services()
        ]

        if field.data not in services_names:
            raise ValidationError('Unknown service name')
