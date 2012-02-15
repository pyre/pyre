# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    $(PACKAGES)

PACKAGES = \
    pyre \
    journal \
    merlin \

# the optional packages
# gsl
GSL_DIR = # overriden by the environment
ifneq ($(strip $(GSL_DIR)),)
  RECURSE_DIRS += gsl
endif
# mpi
MPI_DIR= # overriden by the the environment
ifneq ($(strip $(MPI_DIR)),)
  PACKAGES += mpi
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

#--------------------------------------------------------------------------
#

PYRE_ZIP = $(EXPORT_ROOT)/pyre-${PYRE_VERSION}.zip

zip:
	for package in $(PACKAGES); do { \
	    ( cd $${package}; zip -r ${PYRE_ZIP} $${package}; ) \
	} done


# end of file 
