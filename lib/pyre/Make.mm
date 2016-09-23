# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
include pyre.def
# my subdirectories
RECURSE_DIRS = \
    algebra \
    geometry \
    grid \
    memory \
    patterns \
    timers \

# the top level headers
EXPORT_HEADERS = \
    geometry.h \
    grid.h \

# use a tmp directory that knows what we are building in this directory structure
PROJ_TMPDIR = $(BLD_TMPDIR)/lib

# the standard targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: export-headers
	BLD_ACTION="export" $(MM) recurse

live:
	BLD_ACTION="live" $(MM) recurse

# archiving support
zipit:
	PYRE_ZIP=$(PYRE_ZIP) BLD_ACTION="zipit" $(MM) recurse

# end of file
