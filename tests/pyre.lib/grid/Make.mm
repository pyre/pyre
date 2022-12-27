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
LAYOUT_TESTS = \
    canonical_box.cc \
    canonical_box_skip.cc \
    canonical_cslice.cc \
    canonical_map.cc \
    canonical_map_origin.cc \
    canonical_map_positive.cc \
    canonical_nudge.cc \
    canonical_sanity.cc \
    canonical_slice.cc \
    canonical_visit.cc \
    canonical_visit_order.cc \
    index_access.cc \
    index_arithmetic.cc \
    index_cartesian.cc \
    index_enum.cc \
    index_fill.cc \
    index_from_tuple.cc \
    index_iterator.cc \
    index_sanity.cc \
    index_scaling.cc \
    index_structured_binding.cc \
    index_zero.cc \
    order_access.cc \
    order_c.cc \
    order_fortran.cc \
    order_sanity.cc \
    product_access.cc \
    product_iteration.cc \
    product_ordered_iteration.cc \
    product_sanity.cc \
    rep_at.cc \
    rep_eq.cc \
    rep_fill.cc \
    rep_iteration.cc \
    rep_op.cc \
    rep_reverse_iteration.cc \
    rep_sanity.cc \
    rep_zero.cc \
    sanity.cc \
    shape_access.cc \
    shape_arithmetic.cc \
    shape_cartesian.cc \
    shape_sanity.cc \
    shape_scaling.cc \
    shape_structured_binding.cc

GRID_TESTS = \
    grid_heap_box.cc \
    grid_heap_box_skip.cc \
    grid_heap_expand.cc \
    grid_heap_iteration.cc \
    grid_heap_sanity.cc \
    grid_mmap_sanity.cc \
    grid_mmap_set.cc \
    grid_mmap_get.cc \
    grid_sat.cc \
    grid_sat_box.cc

all: test clean

# testing
test: layout_tests grid_tests

layout_tests: $(LAYOUT_TESTS)
	@echo "testing:"
	@for testcase in $(LAYOUT_TESTS); do { \
            echo "    $${testcase}" ; ./$${testcase} || exit 1 ; \
            } done

grid_tests: $(GRID_TESTS)
	@echo "testing:"
	@for testcase in $(GRID_TESTS); do { \
            echo "    $${testcase}" ; ./$${testcase} || exit 1 ; \
            } done

# build
PROJ_CLEAN += $(LAYOUT_TESTS) $(GRID_TESTS) grid.dat
PROJ_LIBRARIES = -lpyre -ljournal
LIBRARIES = $(PROJ_LIBRARIES) $(EXTERNAL_LIBS)

%: %.cc
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LCXXFLAGS) $(LIBRARIES)

# end of file
