# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import re


def validate_phone(value):
    pattern = re.compile(r'^1[3578]\d{9}$')
    if not re.match(pattern, value):
        raise ValidationError(
            '手机号码格式错误！',
            params={'value': value},
        )
