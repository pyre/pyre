# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class AbstractMetaclass(type):
    """
    A base metaclass from which all the pyre metaclasses derive.

    The only reason to have this class is a quirk in the python implementation of type where
    __init__ does not accept signatures that involve **kwds, making it virtually impossible to
    build correct metaclass hierarchies. Hopefully, this will be fixed someday...

    implementation details:
      __init__: swallow the **kwds arguments that type does not recognize
    """


    def __init__(self, name, bases, attributes, **kwds):
        """
        Swallow **kwds and call type.__init__

        parameters:
          cls: the metaclass invoked; guranteed to be an AttributeClassifier descendant
          name: the name of the class being built
          bases: the tuple of base class records
          **kwds: whatever keywords were not explicitly captured by others
        """
        super().__init__(name, bases, attributes)
        return


# end of file 
