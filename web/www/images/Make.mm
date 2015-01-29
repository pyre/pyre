# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# the package
PACKAGE = web/www/images
# the files
EXPORT_WEB = \
    pyre.png

# standard targets
all: tidy

live: live-web

# end of file
