# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    python \
    journal.lib \
    pyre.lib \
    journal.pkg \
    pyre.pkg \
    merlin.pkg \
    sqlite.pkg \

# the optional packages
# cuda
ifneq ($(strip $(CUDA_DIR)),)
  RECURSE_DIRS += cuda.pkg
endif

# mpi
ifneq ($(strip $(MPI_DIR)),)
  RECURSE_DIRS += mpi.lib mpi.pkg
endif

# gsl
ifneq ($(strip $(GSL_DIR)),)
  RECURSE_DIRS += gsl.pkg
endif

# postgres
ifneq ($(strip $(LIBPQ_DIR)),)
  RECURSE_DIRS += postgres.ext
endif

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

# shortcuts for building specific subdirectories
.PHONY: $(RECURSE_DIRS)

$(RECURSE_DIRS):
	(cd $@; $(MM))


# end of file
