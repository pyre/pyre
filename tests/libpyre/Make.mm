# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    algebra \
    journal \
    timers \

# mpi
MPI_DIR= # overriden by the the environment
ifneq ($(strip $(MPI_DIR)),)
  RECURSE_DIRS += mpi
endif

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

test::
	BLD_ACTION="test" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# end of file 
