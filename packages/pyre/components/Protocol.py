# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# metaclass
from .Role import Role
# superclass
from .Configurable import Configurable


# class declaration
class Protocol(Configurable, metaclass=Role, internal=True):
    """
    The base class for requirement specifications
    """


    # framework data
    pyre_key = None


    # override this in your protocols to provide the default implementation
    @classmethod
    def pyre_default(cls):
        """
        The preferred implementation of this protocol, in case the user has not provided an
        alternative
        """
        # actual protocols should override
        return None


    # introspection
    @classmethod
    def pyre_family(cls):
        """
        Look up my family name
        """
        # if i don't have a key, i don't have a family
        if cls.pyre_key is None: return None
        # otherwise, ask the nameserver
        _, family = cls.pyre_executive.nameserver.lookup(cls.pyre_key)
        # and return the family name
        return family


    @classmethod
    def pyre_package(cls):
        """
        Deduce my package name
        """
        # get the name server
        ns = cls.pyre_executive.nameserver
        # if i don't have a key, i don't have a package
        if cls.pyre_key is None: return None
        # otherwise, ask the nameserver
        _, family = ns.lookup(cls.pyre_key)
        # split the family name apart; the package name is the zeroth entry
        pkgName = family.split(ns.separator)[0]
        # use it to look up the package
        return ns[pkgName]


# end of file 
