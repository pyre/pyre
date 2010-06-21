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
    _pyre_family = () # my public name
    _pyre_implements = None # the list of interfaces implemented by this component
    _pyre_configurables = None # a tuple of all my ancestors that derive from Configurable

    _pyre_traits = None # a list of the traits found in my declaration
    _pyre_inventory = None # per-instance storage for trait values; built by Actor


    # framework notifications
    def pyre_prepare(self, executive):
        """
        Hook that gets invoked by the framework after the component instance has been
        registered but before any configuration events
        """
        return self


    def pyre_configure(self, executive):
        """
        Hook that gets invoked by the framework after the component instance has been
        configured but before the binding of any of its traits
        """
        return self


    def pyre_bind(self, executive):
        """
        Hook that gets invoked by the framework after all the properties of this component
        instance have been assigned their final values, but before any validation has been
        performed
        """
        return self


    def pyre_validate(self, executive):
        """
        Hook that gets invoked by the framework after the properties of this component instance
        have been validated. It is an opportunity to perform checks that involve the values of
        more than one property at a time, and hence could not have been attached to any one
        property
        """
        return self


    def pyre_initialize(self, executive):
        """
        Hook that gets invoked by the framework right before the component is put into
        action. The component is now in a known good state, with all configurable traits fully
        bound and validated. This is the place where the component should acquire whatever
        further resources it requires.
        """
        return self


    def pyre_finalize(self, executive):
        """
        Hook that gets invoked by the framework right before the component is decomissioned.
        The instance should release all acquired resources.
        """
        return self


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
        return cls._pyre_family[0]


    @classmethod
    def pyre_getExtent(cls):
        """
        Return the extent of {cls}, i.e. the set of all its current instances
        """
        return cls._pyre_executive.registrar.components[cls]


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


    # exceptions
    from ..constraints.exceptions import ConstraintViolationError


# end of file 
