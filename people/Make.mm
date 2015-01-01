# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre
PACKAGE = people

PROJ_CLEAN += authorized_keys


all: tidy

authorized_keys:
	./grant.py

SCP = scp
SERVER = orthologue.com
MANAGER = root
DESTINATION = /home/projects/pyre/.ssh

deploy: authorized_keys
	$(SCP) $< $(MANAGER)@$(SERVER):$(DESTINATION)


# end of file
