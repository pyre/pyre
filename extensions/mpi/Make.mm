# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = mpi
PACKAGE = 
MODULE = mpi

include std-pythonmodule.def

PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
EXTERNAL_LIBS += -ljournal

PROJ_SRCS = \
    communicators.cc \
    exceptions.cc \
    groups.cc \
    metadata.cc \
    ports.cc \
    startup.cc

# end of file
