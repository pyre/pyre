# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# metaclass
from .Decorator import Decorator


# declaration
class Descriptor(metaclass=Decorator):
    """
    The base class for typed descriptors

    Descriptors are class data members that collect compile time meta-data about attributes.

    In pyre, classes that use descriptors typically have a non-trivial metaclass that harvests
    them and catalogs them. The base class that implements most of the harvesting logic is
    {pyre.patterns.AttributeClassifier}. The descriptors themselves are typically typed,
    because they play some kind of rôle during conversions between internal and external
    representations of data.
    """


    # types
    # variables
    class variable:
        """Concrete class for representing descriptors"""

        # constant
        category = 'descriptor'

        # support for graph traversals
        def identify(self, authority, **kwds):
            """Let {authority} know I am a descriptor"""
            return authority.onDescriptor(descriptor=self, **kwds)


    # interface
    def bind(self, **kwds):
        """
        Called by my client to let me know that all the available meta-data have been harvested
        """
        # end of the line; nothing else to do
        return self


    # data
    optional = False


    # meta-methods
    def __init__(self, optional=optional, **kwds):
        # chain up
        super().__init__(**kwds)
        # mark me
        self.optional = optional
        # all done
        return


# end of file 
