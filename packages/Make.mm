# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# project global settings
include pyre.def
# the pyre archive
PYRE_ZIP = $(EXPORT_ROOT)/pyre-${PYRE_VERSION}.zip
# my subdirectories
RECURSE_DIRS = \
    $(PACKAGES)
# the ones that are always available
PACKAGES = \
    pyre \
    journal \
    merlin \
    opal \

# the optional packages
# cuda
CUDA_DIR = # overriden by the environment
ifneq ($(strip $(CUDA_DIR)),)
  PACKAGES += cuda
endif

# gsl
GSL_DIR = # overriden by the environment
ifneq ($(strip $(GSL_DIR)),)
  PACKAGES += gsl
endif

# mpi
MPI_DIR= # overriden by the the environment
ifneq ($(strip $(MPI_DIR)),)
  PACKAGES += mpi
endif

# the standard targets
all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

# convenience
zip:
	for package in $(PACKAGES); do { \
	    ( cd $${package}; zip -r ${PYRE_ZIP} $${package}; ) \
	} done

# shortcuts for building specific subdirectories
.PHONY: $(RECURSE_DIRS)

$(RECURSE_DIRS):
	(cd $@; $(MM))


# end of file
