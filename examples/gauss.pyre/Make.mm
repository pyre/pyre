# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#
#


PROJECT = gauss.pyre

RECURSE_DIRS = \
    gauss \
    bin \
    defaults \
    tests

# standard targets

all:
	BLD_ACTION="all" $(MM) recurse
	BLD_ACTION="clean" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

build:
	BLD_ACTION="all" $(MM) recurse


# end of file
