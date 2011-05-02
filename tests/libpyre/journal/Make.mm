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


TESTS = \
    sanity \
    inventory \
    index \
    index-inventory \
    chronicler \
    channel \
    debug \
    debug-envvar \

LIBRARIES = $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------

all: test clean

test: $(TESTS)
	./sanity
	./inventory
	./index
	./index-inventory
	./chronicler
	./channel
	./debug
	DEBUG_OPT=pyre.journal.test ./debug-envvar


sanity: sanity.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

inventory: inventory.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

index: index.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

index-inventory: index-inventory.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

chronicler: chronicler.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

channel: channel.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug: debug.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug-envvar: debug-envvar.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)


# end of file 
