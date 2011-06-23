# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# metaclass
from .Schemer import Schemer


# declaration
class Table(metaclass=Schemer):
    """
    Base class for database table declarations
    """


    # publicly accessible data in the protected pyre namespace
    pyre_name = None # the name of the table; must match the name in the database
    pyre_localColumns = None # a tuple of the column descriptors that were declared locally
    pyre_columns = None # a tuple of all the column descriptors, including inherited ones


# end of file 
