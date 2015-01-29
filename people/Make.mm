# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# package name
PACKAGE = people
# add this to the clean pile
PROJ_CLEAN += authorized_keys

# standard targets
all: tidy
# make the autorized keys file
authorized_keys:
	./grant.py

live: authorized_keys
	$(SCP) $< $(PROJ_LIVE_ADMIN)@$(PROJ_LIVE_HOST):$(PROJ_LIVE_DIR)/.ssh

# end of file
