# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

include libpq/default.def

PROJECT = pyre
PACKAGE = extensions
MODULE = postgres

include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)/$(MODULE)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
EXTERNAL_LIBS += -ljournal

PROJ_SRCS = \
    connection.cc \
    execute.cc \
    exceptions.cc \
    interlayer.cc \
    metadata.cc

# end of file
