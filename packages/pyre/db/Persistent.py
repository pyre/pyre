# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Persistent:
    """
    Metaclass that enables the creation of classes whose instances store part of their
    attributes in relational database tables.

    {Persistent} and its instance {Object} provide the necessary layer to bridge object
    oriented semantics with the relational model. The goal is to make the existence of the
    relational tables more transparent to the developer of database applications by removing as
    much of the grunt work of storing and retrieving object state as possible.
    """


# end of file
