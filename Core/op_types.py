from collections import namedtuple


class Optset(namedtuple('Optset', 'values is_shuffle')):

    """
    Class creat a namedtuple element with default values
    """

    def __new__(cls, values, is_shuffle=True):
        # add default values
        return super(Optset, cls).__new__(cls, values, is_shuffle)