# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Requirement import Requirement


class Role(Requirement):
    """
    The metaclass for interfaces
    """


    # meta methods
    def __init__(self, name, bases, attributes, hidden=False, **kwds):
        """
        Initialize a new interface class record
        """
        super().__init__(name, bases, attributes, **kwds)
        # if this interface is not ignorable
        if not hidden:
            # register it
            self.pyre_executive.registerInterfaceClass(self)
        # all done
        return


    def __call__(self, **kwds):
        """
        Disable the instantiation of interface objects
        """
        import journal
        firewall = journal.firewall("pyre.components")
        raise firewall.log("interfaces cannot be instantiated")


# end of file 
