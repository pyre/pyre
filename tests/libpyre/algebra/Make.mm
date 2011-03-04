# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = algebra

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS)


TESTS = bcd

#--------------------------------------------------------------------------
all: test
	bcd

test: $(TESTS)
	./bcd


bcd: bcd.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXX_FLAGS)


# end of file 
