# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = mpigsl
PACKAGE = 
MODULE = mpigsl


include MPI/default.def
include gsl/default.def
include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)

PROJ_SRCS = \
    exceptions.cc \
    metadata.cc \
    partition.cc \

# end of file
