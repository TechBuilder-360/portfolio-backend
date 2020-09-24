import datetime
from django import template

register = template.Library()

@register.simple_tag()
def days_until():
    delta = datetime.date(2020,9,30) - datetime.date.today()
    return delta.days