# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#
#

# project defaults
include pyre.def
# the package
PACKAGE = web/www
# my subfolders
RECURSE_DIRS = \
    images \
# the files
EXPORT_WEB = \
    index.html

# standard targets
all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

live: live-web
	BLD_ACTION="live" $(MM) recurse

# end of file
