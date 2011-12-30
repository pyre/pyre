# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
        # record whether I am hidden
        self.pyre_hidden = hidden
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
        raise firewall.log("interfaces cannot be instantiated", stackdepth=-1)


# end of file 
