# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#

# project defaults
include pyre.def

# the pile of tests
TESTS = \
    index \
    index-access \
    index-bool \
    packing \
    packing-c \
    packing-fortran \
    packing-access \
    slice \
    iterator \
    iterator-access \
    iterator-loop \
    iterator-slice \
    layout \
    layout-order \
    layout-order-default \
    layout-slice \
    grid-view \
    grid-heap \
    grid-direct \
    grid-direct-data \
    grid-direct-set \
    grid-direct-get \
    grid-mosaic \

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
