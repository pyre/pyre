# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#

include pyre.def
PACKAGE = algebra

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS)
PROJ_LIBRARIES =
LIBRARIES = $(PROJ_LIBRARIES) $(EXTERNAL_LIBS)

TESTS = bcd

#--------------------------------------------------------------------------

all: test clean


test: $(TESTS)
	./cayley_hamilton \
	./tensor_algebra \
	./tensor_arithmetic \
	./tensor_basis \
	./tensor_eigenvalues \
	./tensor_eigenvalues_transformation \
	./tensor_invariants \
	./tensor_packings \
	./tensor_print \
	./tensor_symmetry \
	./tensor_utilities \
	./vector_identities \


# build
%: %.cc
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LCXXFLAGS) $(LIBRARIES)


# end of file
