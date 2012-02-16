# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = gsl
PACKAGE = 
MODULE = gsl

include gsl/default.def
include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
EXTERNAL_LIBS += -ljournal

PROJ_SRCS = \
    exceptions.cc \
    matrix.cc \
    metadata.cc \
    rng.cc \
    vector.cc \

# end of file
