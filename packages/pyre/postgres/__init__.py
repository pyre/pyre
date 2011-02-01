# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# import and set up the postgres extension
# access the extension
from . import pyrepg
# get hold of the standard compliant exception hierarchy
from ..db import exceptions
# register the exception hierarchy with the module so that the exceptions it raises are
# subclasses of the ones defined in pyre.db
pyrepg.registerExceptions(exceptions)


# end of file 
