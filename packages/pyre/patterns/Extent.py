# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import weakref

# superclass
from .Type import Type


# metaclass that allows classes to count their instances
class Extent(Type):
    """
    Metaclass that endows its instances with awareness of their extent, defined as the set of
    instances of the class and all its subclasses.

    The class extent is stored with the first base class in a hierarchy that mentions {Extent}
    as a metaclass, and all descendants are counted by that class. Descendants that want to
    keep track of their own extent and prevent their extent from being counted by a superclass
    must be declared with {pyre_extent} set to {True}
    """


    # metamethods
    def __new__(cls, name, bases, attributes, *, pyre_extent=False, **kwds):
        """
        Endow the class record being created, with a registry of instances of all classes whose
        base it is.

        The implementation here attaches a {weakset} of instances to the first class in a
        hierarchy that mentions {Extent} as its metaclass, by taking advantage of the way
        python metaclasses work. Do not forget that {Extent} will process the class records of
        all subclasses of this base class. Setting {pyre_extent} to {True} in the declaration
        of a subclass allows that particular subclass to become a new extent root for its
        subclasses, and prevents instances from counted by its base classes.
        """
        # chain up
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # initialize storage for the instances. this happens only if the user has marked this
        # class as an extent root by explicitly setting {pyre_extent} to {True}, or if the
        # attribute that holds the storage is missing, which is true only for the first class
        # that specifies {Extent} as its metaclass
        if pyre_extent or not hasattr(record, "pyre_extent"):
            # build the registry
            record.pyre_extent = weakref.WeakSet()
        # all done
        return record


    def __call__(self, *args, **kwds):
        """
        Intercept the constructor call, build the instance, and place a weak reference to it in
        our registry
        """
        # build the instance
        instance = super().__call__(*args, **kwds)
        # keep track of it
        self.pyre_extent.add(instance)
        # and make it available to the caller
        return instance


# end of file
