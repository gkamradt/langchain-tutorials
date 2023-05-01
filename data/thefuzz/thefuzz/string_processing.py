import re


class StringProcessor:
    """
    This class defines method to process strings in the most
    efficient way. Ideally all the methods below use unicode strings
    for both input and output.
    """

    regex = re.compile(r"(?ui)\W")

    @classmethod
    def replace_non_letters_non_numbers_with_whitespace(cls, a_string):
        """
        This function replaces any sequence of non letters and non
        numbers with a single white space.
        """
        return cls.regex.sub(" ", a_string)
