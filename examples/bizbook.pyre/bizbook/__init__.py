# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# the schema
from . import schema

# connect to the bizbook database under postgres
def pg():
    # access the package
    import postgres
    # make a data store and connect to it
    db = postgres.server(name="bizbook").attach()
    # and return it
    return db


# end of file 
