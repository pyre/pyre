# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A folder: the tables of a database as files of rows, in the text format of postgres's copies,
and the server that keeps them
"""

# the visitor that writes the values of the columns
from .Text import Text as text

# and the server
from .Server import Server as server

# end of file
