# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# the package
PACKAGE = defaults/$(PROJECT)/platforms

# the files
EXPORT_ETC = \
    macports.pfg

# add these to the clean pile
PROJ_CLEAN += $(EXPORT_ETCDIR)

# the standard targets
all: export

export:: export-etc

live: live-etc

# end of file
