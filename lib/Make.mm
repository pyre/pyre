# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
include pyre.def
# my dibdirectories
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

# use a tmp directory that knows what we are bulding in this directory structure
PROJ_TMPDIR = $(BLD_TMPDIR)/lib

# the standard targets
all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export::
	BLD_ACTION="export" $(MM) recurse

live:
	BLD_ACTION="live" $(MM) recurse

# archiving support
zipit:
	PYRE_ZIP=$(PYRE_ZIP) BLD_ACTION="zipit" $(MM) recurse

# end of file
