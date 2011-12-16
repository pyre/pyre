# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    journal \
    algebra \
    patterns \
    timers \

# the optional packages
# mpi
MPI_DIR= # overriden by the the environment
ifneq ($(strip $(MPI_DIR)),)
  RECURSE_DIRS += mpi
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
