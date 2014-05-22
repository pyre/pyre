# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from .Director import Director


# class declaration
class Plector(Director):
    """
    Metaclass that facilitates the construction of {plexus} applications
    """


    def __new__(cls, name, bases, attributes, action=None, **kwds):
        # chain up
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # if an {action} protocol is provided
        if action:
            # instantiate it to get a descriptor and attach it to the record; doing this after
            # record instantiation bypasses {action} being recorded as a trait and makes it a
            # regular class variable
            record.pyre_action = action
        # all done
        return record

        # the following is the implementation necessary to turn {action} into an actual trait
        # if an {action} protocol is provided
        if action:
            # add it to the attributes so my superclass can turn it into a trait
            attributes['pyre_action'] = action()
        # chain up to get the record built and return it
        return super().__new__(cls, name, bases, attributes, **kwds)


# end of file 
