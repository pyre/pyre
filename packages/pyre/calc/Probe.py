# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from .Observer import Observer


# declaration
class Probe(Observer):
    """
    The base class for objects that observe the values of nodes in a calc graph
    """


    def flush(self, observable):
        """
        The callback that gets invoked when one of the monitored nodes receives a new value
        """
        # by default, do nothing
        return


# end of file
