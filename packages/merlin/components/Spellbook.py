# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre


# declaration
class Spellbook(pyre.component, family="merlin.spellbook"):
    """
    This is a sample documentation string for Spellbook
    """


    # class public data
    PROPERTY = pyre.properties.TYPE(default=DEFAULT)
    PROPERTY.doc = "the purpose of this property"


    # per-instance public data


    # class interface
    @pyre.export
    def BEHAVIOR(self, **kwds):
        """
        The documentation of BEHAVIOR
        """


    # meta methods
    def __init__(self, **kwds):
        # chain to the ancestors
        super().__init__(**kwds)

        # all done
        return


    # implementation details


# end of file 
