# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

include libpq/default.def

PROJECT = pyre
PACKAGE = timers
MODULE = timers

include std-pythonmodule.def

PROJ_SRCS = \
    metadata.cc

# end of file
