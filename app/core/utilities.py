from datetime import datetime

from rest_framework.exceptions import ValidationError


def limit_pub_date_choices():
    return {'pub_date__lte': datetime.utcnow()}


def validate_gte_today(value: datetime.date):
    print(value)
    if value < datetime.today().date():
        raise ValidationError(
            detail=f'{value} is less than today',
            code='invalid'
        )
