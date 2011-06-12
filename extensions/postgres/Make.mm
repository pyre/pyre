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

PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
EXTERNAL_LIBS += -ljournal

PROJ_SRCS = \
    connection.cc \
    execute.cc \
    exceptions.cc \
    interlayer.cc \
    metadata.cc

# end of file
