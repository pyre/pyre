# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
        # if the {record} does not specify a leaf mix-in
        if not record.leaf:
            # set it to the default
            record.leaf = cls.leaf
        # yield the leaf class
        yield record.leaf
        # and the buck stops here...
        yield record
        # all done
        return


    @classmethod
    def compositeDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of literals
        """
        # if the {record} does not specify a leaf mix-in
        if not record.composite:
            # set it to the default
            record.composite = cls.composite
        # yield the leaf class
        yield record.composite
        # and the buck stops here...
        yield record
        # all done
        return


# end of file 
