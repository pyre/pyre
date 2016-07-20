# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
include pyre.def

# the pile of tests
TESTS = \
    index \
    index-access \
    index-bool \
    layout \
    layout-access \
    iterator \
    iterator-layout \
    iterator-access \
    iterator-loop \
    tile \
    tile-layout \
    slice \
    tile-slice \
    direct-create \
    direct-map \
    direct-instantiate \

# tests that should fail because their access patterns are prohibited
SHOULD_FAIL = \
    direct-clone \

all: test clean

# testing
test: $(TESTS)
	@echo "testing:"
	@for testcase in $(TESTS); do { \
            echo "    $${testcase}" ; ./$${testcase} || exit 1 ; \
            } done

# build
PROJ_CLEAN += $(TESTS) grid.dat
PROJ_LIBRARIES = -lpyre -ljournal
LIBRARIES = $(PROJ_LIBRARIES) $(EXTERNAL_LIBS)

%: %.cc
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LCXXFLAGS) $(LIBRARIES)

# end of file
