# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Actor import Actor
from .Configurable import Configurable


class Component(Configurable, metaclass=Actor):
    """
    The base class for all components
    """


    # framework data
    _pyre_name = None # my public name
    _pyre_family = None # my public name
    _pyre_implements = None # the list of interfaces implemented by this component
    _pyre_configurables = None # a tuple of all my ancestors that derive from Configurable

    _pyre_traits = None # a list of the traits found in my declaration
    _pyre_inventory = None # per-instance storage for trait values; built by Actor


    # class interface
    @classmethod
    def pyre_getPackageName(cls):
        """
        Extract the name of the package that this component is a part of by splitting the
        family name apart based on the _pyre_FAMILY_SEPARATOR and returning the leading
        fragment
        """
        # bail out if there is not family name
        if not cls._pyre_family: return None
        # otherwise, split the family name na dreturn the first fragment
        return cls._pyre_family.split(cls._pyre_FAMILY_SEPARATOR)[0]


    @classmethod
    def pyre_getExtent(cls):
        """
        Return the extent of {cls}, i.e. the set of all its current instances
        """
        return cls._pyre_registrar.registrar.components[cls]


    # meta methods
    def __init__(self, name, **kwds):
        super().__init__(**kwds)

        # component instance registration is done by Actor.__call__, the metaclass method that
        # invokes this constructor

        # store my name
        self._pyre_name = name
        # build my inventory instance by calling the constructor that my metaclass attached at
        # compile time
        self._pyre_inventory = self._pyre_Inventory()

        return


    def __getattr__(self, name):
        """
        Trap attribute lookup errors and attempt to resolve the name in my inventory's namemap

        This makes it possible to get the value of a trait by using any of its aliases.
        """
        # attempt to resolve the attribute name by normalizing it
        try:
            canonical = self.pyre_normalizeName(name)
        except self.TraitNotFoundError as error:
            missing = AttributeError(
                "{0.__class__.__name__!r} has no attribute {1!r}".format(self, name))
            raise missing from error
        # if we got this far, restart the attribute lookup using the canonical name
        # don't be smart here; let getattr do its job, which involves invoking the trait
        # descriptors if necessary
        return getattr(self, canonical)


    def __setattr__(self, name, value):
        """
        Trap attribute retrieval and attempt to normalize the name before making the assignment
        """
        # normalize the name
        try:
            name = self.pyre_normalizeName(name)
        except self.TraitNotFoundError:
            return super().__setattr__(name, value)

        return super().__setattr__(name, value)


    # constants
    _pyre_FAMILY_SEPARATOR = '.'


# end of file 
