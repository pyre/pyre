# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import itertools


class Configurable(object):
    """
    The base class for framework configurable classes

    This class provides storage for class attributes and a place to park utilities that are
    common to both components and interfaces
    """
    # access to the base Inventory class
    # embryonic case for an invariant to simplify the metaclass implementations: all classes in
    # the mro of components and interfaces define a _pyre_Inventory so it is safe to derive one
    # for the current class from the ones in its immediate ancestors
    from .Inventory import Inventory

    # framework data
    _pyre_family = None # my family name for settings that are to be shared by all instances
    _pyre_category = None # my category for attribute classification
    _pyre_ancestors = None # a cached tuple of all my non-trivial ancestors
    _pyre_implements = None # sentinel for the implementation specification (DO NOT REMOVE)
    

    # various utilities
    @classmethod
    def pyre_ancestors(cls, proper=False):
        """
        Return an iterator over all my non-trivial ancestors
        """
        # where should i start iterating?
        # skip myself if proper is True
        start = 1 if proper else 0
        return itertools.takewhile(lambda x: x is not Configurable, cls.__mro__[start:])


    @classmethod
    def pyre_normalizeName(cls, name):
        """
        Convert the given trait name or alias to the canonical one
        """
        # iterate over my ancestors
        for ancestor in cls._pyre_ancestors:
            # look up the name in the namemap
            try:
                return ancestor._pyre_Inventory._pyre_namemap[name]
            except KeyError:
                continue

        raise cls.TraitNotFoundError(cls, name)


# end of file 
