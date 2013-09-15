# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


PROJECT = merlin-tests

TEST_DIR = /tmp

PROJ_CLEAN += \
    $(TEST_DIR)/deep \
    $(TEST_DIR)/shallow \

MERLIN = $(EXPORT_BINDIR)/merlin

#--------------------------------------------------------------------------
#

all: test

test: init clean

init:
	$(MERLIN) init $(TEST_DIR)/shallow
	$(MERLIN) init --merlin.init.create-prefix $(TEST_DIR)/deep/ly/burried

# end of file 
