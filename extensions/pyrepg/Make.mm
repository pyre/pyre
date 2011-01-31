# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

include libpq/default.def

PROJECT = pyre
PACKAGE = db
MODULE = pyrepg

include std-pythonmodule.def

PROJ_SRCS = \
    exceptions.cc \
    connection.cc \
    metadata.cc

# end of file
