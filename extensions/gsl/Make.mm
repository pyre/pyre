# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include gsl.def
# package name
PACKAGE =
# the module
MODULE = gsl
# get gsl support
include gsl/default.def
# build a python extension
include std-pythonmodule.def
# my headers live here
PROJ_INCDIR = $(BLD_INCDIR)/pyre/$(PROJECT)
# use a tmp directory that knows the name of the module
PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
# point to the location of my libraries
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)
# link against these
PROJ_LIBRARIES = -ljournal
# the sources
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
