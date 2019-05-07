# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre


# class declaration
class Specification(pyre.protocol):
    """
    The protocol of product specifications

    Specifications are snapshots of product attributes
    """


    # required interface
    @pyre.provides
    def pyre_make(self, **kwds):
        """
        Ask my factories to rebuild me
        """


    # facility makers
    @classmethod
    def input(cls, **kwds):
        """
        Make an input descriptor
        """
        # ask my meta-class to build a descriptor marked as input
        facility = cls(input=True, **kwds)
        # and return it
        return facility


    @classmethod
    def output(cls, **kwds):
        """
        Make an output descriptor
        """
        # ask my meta-class to build a descriptor marked as output
        facility = cls(output=True, **kwds)
        # and return it
        return facility


# end of file
