# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class AbstractMetaclass(type):
    """
    The base metaclass from which all pyre metaclasses derive.

    The main raison d'être for this class is a quirk in the python implementation of {type}
    where __init__ does not accept signatures that involve **kwds, making it virtually
    impossible to build correct metaclass hierarchies. Hopefully this will be fixed soon.

    implementation details:
      __new__: swallow the **kwds that {type} does not recognize
      __init__: swallow the **kwds that {type} does not recognize
    """


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Swallow **kwds and call type.__new__
        """
        return super().__new__(cls, name, bases, attributes)


    def __init__(self, name, bases, attributes, **kwds):
        """
        Swallow **kwds and call type.__init__
        """
        return super().__init__(name, bases, attributes)


# end of file 
