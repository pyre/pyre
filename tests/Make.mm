# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    python \
    libpyre \
    pyre \
    journal \
    merlin \
    sqlite \
    opal \

# the optional packages
# cuda
CUDA_DIR = # overriden by the environment
ifneq ($(strip $(CUDA_DIR)),)
  RECURSE_DIRS += cuda
endif

# mpi
MPI_DIR= # overriden by the the environment
ifneq ($(strip $(MPI_DIR)),)
  RECURSE_DIRS += mpi
endif

# gsl
GSL_DIR= # overriden by the the environment
ifneq ($(strip $(GSL_DIR)),)
  RECURSE_DIRS += gsl
endif

# postgres
LIBPQ_DIR= # overriden by the the environment
ifneq ($(strip $(LIBPQ_DIR)),)
  RECURSE_DIRS += postgres
endif

#

all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#  shortcuts to building in my subdirectories
.PHONY: cuda gsl journal libpyre merlin mpi opal postgres pyre python sqlite

cuda:
	(cd cuda; $(MM))

gsl:
	(cd gsl; $(MM))

journal:
	(cd journal; $(MM))

libpyre:
	(cd libpyre; $(MM))

merlin:
	(cd merlin; $(MM))

mpi:
	(cd mpi; $(MM))

opal:
	(cd opal; $(MM))

postgres:
	(cd postgres; $(MM))

pyre:
	(cd pyre; $(MM))

python:
	(cd python; $(MM))

sqlite:
	(cd sqlite; $(MM))


# end of file 
