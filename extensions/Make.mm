# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# project defaults
include pyre.def
# my subdirectories
RECURSE_DIRS = \
    host \
    journal \
    timers

# the optional packages
# cuda
CUDA_DIR= # overriden by the the environment
ifneq ($(strip $(CUDA_DIR)),)
  RECURSE_DIRS += cuda
endif

# mpi
MPI_DIR= # overriden by the the environment
ifneq ($(strip $(MPI_DIR)),)
  RECURSE_DIRS += mpi
endif

#gsl
GSL_DIR = # overriden by the environment
ifneq ($(strip $(GSL_DIR)),)
  RECURSE_DIRS += gsl
endif

# postgres
LIBPQ_DIR= # overriden by the the environment
ifneq ($(strip $(LIBPQ_DIR)),)
  RECURSE_DIRS += postgres
endif

# use a tmp directory that knows what we are bulding in this directory structure
PROJ_TMPDIR = $(BLD_TMPDIR)/extensions

# standard targets
all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

live:
	BLD_ACTION="live" $(MM) recurse

# end of file
