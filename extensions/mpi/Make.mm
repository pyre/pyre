# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

PROJECT = mpi
PACKAGE =
MODULE = mpi

include MPI/default.def
include std-pythonmodule.def

PROJ_INCDIR = $(BLD_INCDIR)/pyre/$(PROJECT)
PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
PROJ_LIBRARIES = -ljournal

PROJ_SRCS = \
    communicators.cc \
    exceptions.cc \
    groups.cc \
    metadata.cc \
    ports.cc \
    startup.cc

export:: export-headers

EXPORT_INCDIR = $(EXPORT_ROOT)/include/pyre/$(PROJECT)
EXPORT_HEADERS = \
    capsules.h

# end of file
