import functools

from thefuzz.string_processing import StringProcessor


def validate_string(s):
    """
    Check input has length and that length > 0

    :param s:
    :return: True if len(s) > 0 else False
    """
    try:
        return len(s) > 0
    except TypeError:
        return False


def check_for_equivalence(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if args[0] == args[1]:
            return 100
        return func(*args, **kwargs)
    return decorator


def check_for_none(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if args[0] is None or args[1] is None:
            return 0
        return func(*args, **kwargs)
    return decorator


def check_empty_string(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if len(args[0]) == 0 or len(args[1]) == 0:
            return 0
        return func(*args, **kwargs)
    return decorator


bad_chars = "".join([chr(i) for i in range(128, 256)])  # ascii dammit!
translation_table = {ord(c): None for c in bad_chars}


def ascii_only(s):
    return s.translate(translation_table)


def make_type_consistent(s1, s2):
    """If objects aren't both string instances force them to strings"""
    if isinstance(s1, str) and isinstance(s2, str):
        return s1, s2

    else:
        return str(s1), str(s2)


def full_process(s, force_ascii=False):
    """Process string by
        -- removing all but letters and numbers
        -- trim whitespace
        -- force to lower case
        if force_ascii == True, force convert to ascii"""

    if force_ascii:
        s = ascii_only(str(s))
    # Keep only Letters and Numbers (see Unicode docs).
    string_out = StringProcessor.replace_non_letters_non_numbers_with_whitespace(s)
    # Remove leading and trailing whitespaces and force into lowercase.
    string_out = string_out.strip().lower()
    return string_out


def intr(n):
    '''Returns a correctly rounded integer'''
    return int(round(n))
