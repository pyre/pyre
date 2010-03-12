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

      __new__ gets the name of the class being built, its list of bases and an instance of the
      special attribute dictionary in order to build the class record. It replaces the
      constructor of the class with one that chains to the original and adds the instance to
      extent of the class. The extent is stored as a WeakSet so that it doesn't interfere with
      the normal reference counting. When the instance is destoryed, it is also automatically
      removed from the extent by the WeakSet implementation.
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

        # grab the constructor; it is guaranteed to exist since object has one
        # and all classes derive from object
        constructor = record.__init__

        # build the replacement
        def constructor_wrapper(self, **kwds):
            # chain to the original constructor
            constructor(self, **kwds)
            # add a weak reference to myself in my class' extent
            record._pyre_extent.add(self)
            return

        # attach the replacement
        record.__init__ = constructor_wrapper

        return record
        

# end of file 
