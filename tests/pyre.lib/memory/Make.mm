# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

# project defaults
include pyre.def

# the pile of tests
TESTS = \
    constmap_oob.cc \
    constmap_read.cc \
    constview_access.cc \
    filemap_create.cc \
    filemap_write.cc \
    filemap_read.cc \
    heap_access.cc \
    heap_borrow.cc \
    heap_copy.cc \
    heap_oob.cc \
    map_create.cc \
    map_oob.cc \
    map_read.cc \
    map_write.cc \
    memory_sanity.cc \
    view_access.cc \
    view_oob.cc \

# tests that should fail because their access patterns are prohibited
SHOULD_FAIL = \

all: test clean

# testing
test: $(TESTS)
	@echo "testing:"
	@for testcase in $(TESTS); do { \
            echo "    $${testcase}" ; ./$${testcase} || exit 1 ; \
            } done

# build
PROJ_CLEAN += $(TESTS) direct-grid.dat constdirect-grid.dat
PROJ_LIBRARIES = -lpyre -ljournal
LIBRARIES = $(PROJ_LIBRARIES) $(EXTERNAL_LIBS)

%: %.cc
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LCXXFLAGS) $(LIBRARIES)

# end of file
