# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    python \
    libpyre \
    pyre \
    journal \
    merlin \

# the optional packages
# gsl
GSL_DIR= # overriden by the the environment
ifneq ($(strip $(GSL_DIR)),)
  RECURSE_DIRS += gsl
endif

# mpi
MPI_DIR= # overriden by the the environment
ifneq ($(strip $(MPI_DIR)),)
  RECURSE_DIRS += mpi
endif

# postgres
LIBPQ_DIR= # overriden by the the environment
ifneq ($(strip $(LIBPQ_DIR)),)
  RECURSE_DIRS += postgres
endif

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# end of file 
