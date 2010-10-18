# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import itertools
from .Templater import Templater


class Sheet(metaclass=Templater, hidden=True):
    """
    The base class for worksheets
    """


    # introspection
    @classmethod
    def pyre_measures(cls):
        """
        Generate a sequence of all my measures
        """
        return itertools.chain(cls.pyre_localMeasures, cls.pyre_inheritedMeasures)


    def __init__(self, name=None, **kwds):
        super().__init__(**kwds)

        self.pyre_name = name

        return


# end of file 
