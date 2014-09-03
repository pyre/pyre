# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from ..patterns.AbstractMetaclass import AbstractMetaclass


# declaration
class Category(AbstractMetaclass):
    """
    Metaclass that builds class hierarchies with specific properties from a given base class
    """


    # implementation details
    @classmethod
    def leafDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of literals
        """
        # if the {record} specifies a leaf mix-in, add it to the pile
        if record.leaf: yield record.leaf
        # yield the default leaf class
        yield cls.leaf
        # and the buck stops here...
        yield record
        # all done
        return


    @classmethod
    def compositeDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of literals
        """
        # if the {record} specifies a composite mix-in, add it to the pile
        if record.composite: yield record.composite
        # yield the default composite class
        yield cls.composite
        # the traversible
        yield cls.traversible
        # and the buck stops here...
        yield record
        # all done
        return


# end of file 
