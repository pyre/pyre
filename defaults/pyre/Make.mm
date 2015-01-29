# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# package
PACKAGE = defaults/pyre
# my subforlders
RECURSE_DIRS = \
    platforms
# add these to the clean pile
PROJ_CLEAN += $(EXPORT_ETCDIR)

# the standard targets
all: export

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

# end of file
