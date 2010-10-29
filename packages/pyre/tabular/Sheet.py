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


    # interface
    def populate(self, records=None):
        """
        """


    # introspection
    @classmethod
    def pyre_measures(cls):
        return itertools.chain(cls.pyre_localMeasures, cls.pyre_inheritedMeasures)


    @classmethod
    def pyre_derivations(cls):
        return itertools.chain(cls.pyre_localDerivations, cls.pyre_inheritedDerivations)


    @classmethod
    def pyre_items(cls):
        return itertools.chain(cls.pyre_measures(), cls.pyre_derivations())


    # meta methods
    def __init__(self, name=None, **kwds):
        super().__init__(**kwds)

        self.pyre_name = name

        return


# end of file 
