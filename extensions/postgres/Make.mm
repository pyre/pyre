# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

include libpq/default.def

PROJECT = postgres
PACKAGE = 
MODULE = postgres

include std-pythonmodule.def

PROJ_SRCS = \
    execute.cc \
    exceptions.cc \
    connection.cc \
    metadata.cc

# end of file
