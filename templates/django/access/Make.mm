# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include {project.name}.def
# the name of this package
PACKAGE = access
# add this to the clean pile
PROJ_CLEAN += authorized_keys

# standard targets
all: tidy

# make the autorized keys file
authorized_keys: $(PUBLIC_KEYS) grant.py grant.cfg Make.mm
	./grant.py

live: authorized_keys
	$(SCP) $< $(PROJ_LIVE_ADMIN)@$(PROJ_LIVE_HOST):$(PROJ_LIVE_DIR)/.ssh

# convenience (and for checking before deploying)
keys: authorized_keys

# end of file
