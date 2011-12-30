# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre
PACKAGE = depository/merlin

RECURSE_DIRS = \
    spells \

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

EXPORT_ETCDIR = $(EXPORT_ROOT)
EXPORT_ETC = \

export:: # export-etc
	BLD_ACTION="export" $(MM) recurse


# end of file 
