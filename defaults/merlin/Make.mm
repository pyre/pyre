# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = defaults/merlin

RECURSE_DIRS = \

#--------------------------------------------------------------------------
#

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#

export:: # export-etc
	BLD_ACTION="export" $(MM) recurse

release:: # release-etc
	BLD_ACTION="release" $(MM) recurse


# end of file 
