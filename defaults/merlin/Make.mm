# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
include pyre.def
# the package
PACKAGE = defaults/merlin

# add these to the clean pile
PROJ_CLEAN += \
    $(EXPORT_ETCDIR)/$(PROJECT)

# the standard targets
all: tidy

live: # nothing to do for now

# end of file
