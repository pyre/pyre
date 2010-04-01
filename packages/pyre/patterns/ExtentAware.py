# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref


class ExtentAware(type):
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
    def __new__(cls, name, bases, attributes):
        """
        Intercept the class record creation and install a replacement constructor that record
        the number of instances of this class
        """
        # build the class record
        record = super().__new__(cls, name, bases, attributes)
        # add the weakset attribute
        record._pyre_extent = weakref.WeakSet()
        # and return it
        return record


    def __call__(cls, **kwds):
        """
        Intercept the call to the client constructor, build the instance and keep a weak
        reference to it
        """
        # build the instance
        instance = super().__call__(**kwds)
        # add it to the class extent
        instance.__class__._pyre_extent.add(instance)
        # and return it
        return instance
        

# end of file 
