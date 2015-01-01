# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

PROJECT = gsl
PACKAGE =
MODULE = gsl

include gsl/default.def
include std-pythonmodule.def

PROJ_INCDIR = $(BLD_INCDIR)/pyre/$(PROJECT)
PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
PROJ_LIBRARIES = -ljournal

PROJ_SRCS = \
    blas.cc \
    exceptions.cc \
    histogram.cc \
    linalg.cc \
    matrix.cc \
    metadata.cc \
    pdf.cc \
    permutation.cc \
    rng.cc \
    vector.cc \

# optional mpi support
MPI_DIR= # should be overriden by the environment
ifneq ($(strip $(MPI_DIR)), )
    include MPI/default.def
    PROJ_SRCS += partition.cc
endif

# actions
export:: export-headers

EXPORT_INCDIR = $(EXPORT_ROOT)/include/pyre/$(PROJECT)
EXPORT_HEADERS = \
    capsules.h

# end of file
