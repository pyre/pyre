# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from ..patterns.AttributeClassifier import AttributeClassifier


# class declaration
class Persistent(AttributeClassifier):
    """
    Metaclass that enables the creation of classes whose instances store part of their
    attributes in relational database tables.

    {Persistent} and its instance {Object} provide the necessary layer to bridge object
    oriented semantics with the relational model. The goal is to make the existence of the
    relational tables more transparent to the developer of database applications by removing as
    much of the grunt work of storing and retrieving object state as possible.
    """


    # meta-methods
    def __init__(self, name, bases, attributes, schema=None, **kwds):
        # chain up
        super().__init__(name, bases, attributes, **kwds)

        # if i model a table
        if schema is not None:
            # attach my schema
            self.pyre_primaryTable = schema
            # register me with the schema manager
            self.pyre_schema.models[schema] = self

        # all done
        return


    def __call__(self, **kwds):
        """
        Create one of my instances
        """
        # make one and return it
        return super().__call__()


# end of file
