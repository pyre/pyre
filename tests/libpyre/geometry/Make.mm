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
    order \
    order-access \
    slice \
    iterator \
    iterator-access \
    iterator-loop \
    iterator-slice \
    tile \
    tile-order \
    tile-slice \
    point \
    brick \
    grid-view \
    grid-heap \
    grid-direct \
    grid-direct-set \
    grid-direct-get \

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
