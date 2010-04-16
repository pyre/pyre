# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Role import Role
from .Configurable import Configurable


class Interface(Configurable, metaclass=Role):
    """
    The base class for requirement specifications
    """


    def __init__(self, **kwds):
        import journal
        firewall = journal.firewall("pyre.components")
        raise firewall.log("interfaces can not be instantiated")


    # private data
    _pyre_family = None # my family name
    _pyre_category = "interfaces" # my classification as an attribute
    _pyre_ancestors = None # the tuple of my ancestors


# end of file 
