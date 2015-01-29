# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# project globals
include pyre.def
# the package
PACKAGE = web/apache

# standard targets
all: tidy

live: live-apache-conf live-apache-restart

# there is another target that might be useful:
#
#    live-apache-conf: make a link to the configuration file in the apache {sites-available}
#                      directory, followed by enabling the site

# end of file
