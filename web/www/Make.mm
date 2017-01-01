# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#
#

# project defaults
include pyre.def
# my subfolders
RECURSE_DIRS = \
    graphics \
    scripts \
    styles \

# the files
EXPORT_WEB = pyre.html

# standard targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: export-web
	BLD_ACTION="export" $(MM) recurse

live: live-web
	BLD_ACTION="live" $(MM) recurse

# end of file
