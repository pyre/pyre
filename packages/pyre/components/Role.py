# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Requirement import Requirement


class Role(Requirement):
    """
    The interface metaclass
    """


    # meta methods
    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a new interface class record
        """
        super().__init__(name, bases, attributes, **kwds)
        # register this interface class
        self._pyre_executive.registerInterfaceClass(self)
        # all done
        return


    # disable instatiation of interfaces
    def __call__(self, **kwds):
        import journal
        firewall = journal.firewall("pyre.components")
        raise firewall.log("interfaces can not be instantiated")


# end of file 
