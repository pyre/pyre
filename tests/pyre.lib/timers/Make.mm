# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

include pyre.def
PACKAGE = timers

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS)


TESTS = \
    movement_ms.cc \
    movement_reset.cc \
    movement_sanity.cc \
    movement_sec.cc \
    movement_start.cc \
    movement_stop.cc \
    movement_us.cc \
    process_timer_example.cc \
    process_timer_ms.cc \
    process_timer_reset.cc \
    process_timer_sanity.cc \
    process_timer_shared.cc \
    process_timer_start.cc \
    process_timer_stop.cc \
    proxy_sec.cc \
    registrar_contains.cc \
    registrar_iter.cc \
    registrar_lookup.cc \
    registrar_sanity.cc \
    registrar_shared.cc \
    timers_sanity.cc \
    wall_timer_example.cc \
    wall_timer_ms.cc \
    wall_timer_reset.cc \
    wall_timer_sanity.cc \
    wall_timer_shared.cc \
    wall_timer_start.cc \
    wall_timer_stop.cc

PROJ_LCXX_LIBPATH = $(BLD_LIBDIR)
PROJ_LIBRARIES = -lpyre -ljournal
LIBRARIES = $(PROJ_LIBRARIES) $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------
all: test clean


test: $(TESTS)
	./timer

# build
%: %.cc
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LCXXFLAGS) $(LIBRARIES)


# end of file
