# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to weak references
import weakref
# my superclass
from .AbstractMetaclass import AbstractMetaclass


class ExtentAware(AbstractMetaclass):
    """
    Metaclass that endows its instances with awareness of their extent.

    The extent of a class is the set of its instances.

    implementation details:

        __new__: intercept the creation of the client class record and add the reference
        counting weak set as a class attribute

        __call__: capture the creation of an instance, since it is this method that triggers
        the call to the client class' constructor. we let super().__call__ build the instance
        and then add a weak reference to it in _pyre_extent
    """


    # class methods
    def __new__(cls, name, bases, attributes, pyre_extentRoot=False, **kwds):
        """
        Intercept the class record creation and install a replacement constructor that records
        the number of instances of this class
        """
        # the old implementation replaced the client constructor with one that added a weak
        # reference to the new instance in _pyre_extent. as a side effect, each class in a
        # hierarchy maintained an extent for itself and its descendants, assuming that __init__
        # was chaining upwards correctly. the current implementation with __new__/__call__
        # behaves somewhat differently: the extent is stored with the first class that mentions
        # ExtentAware as a metaclass, and all descendants are counted by that class

        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # add the weakset attribute that maintains the extent, if it is not already there this
        # has the effect of storing the class extent at the root class in a hierarchy which
        # makes it easy to check that descendants have been garbage collected as well. if you
        # want to keep track of the extent at some other point in a class hierarchy, declare
        # that class with {pyre_extentRoot} set to {True}
        if pyre_extentRoot or not hasattr(record, "_pyre_extent"): 
            record._pyre_extent = weakref.WeakSet()
        # and return it
        return record


    def __call__(self, *args, **kwds):
        """
        Intercept the call to the client constructor, build the instance and keep a weak
        reference to it
        """
        # build the instance
        instance = super().__call__(*args, **kwds)
        # add it to the class extent
        self._pyre_extent.add(instance)
        # and return it
        return instance
        

# end of file 
