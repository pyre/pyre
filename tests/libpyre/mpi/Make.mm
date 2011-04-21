# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = mpi

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS)


TESTS = sanity

PROJ_LCXX_LIBPATH = $(BLD_LIBDIR)
LIBRARIES = -lpyre-mpi $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------
all: test


test: $(TESTS)
	./sanity


sanity: sanity.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)


# end of file 
