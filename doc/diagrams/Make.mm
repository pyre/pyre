# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#
#


PROJECT = pyre

RECURSE_DIRS = \
    design \
    packages \
    stencils \

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
