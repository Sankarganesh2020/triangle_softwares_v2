import datetime
from datetime import date
from django import template
register = template.Library()


@register.filter(expects_localtime=True, is_safe=False)
def custom_date(value, arg=None):
    if value in (None, ''):
        return ''
    if isinstance(value, int):
        # input date as timestamp integer
        value = date.fromtimestamp(value)
    elif isinstance(value, str):
        # input date as timestamp string
        value = date.fromtimestamp(int(value))
    else:
        value = value

    return value

@register.filter
def div( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value / arg
    except: pass
    return ''

@register.filter
def sub( value, arg ):
    '''
    Subtract the value; argument is the Subtractor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        return value - arg
    except: pass
    return ''