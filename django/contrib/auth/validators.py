import re

from django.core import validators
from django.utils.deconstruct import deconstructible


class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r'\A[\w.@+-]+\Z'
    message = _('Enter a valid username. This value may contain only English letters, numbers, and @/./+/-/_ characters.')
    flags = re.ASCII


class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'\A[\w.@+-]+\Z'
    message = _('Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')
@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0
