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
    state \
    index \
    index-state \
    chronicler \
    chronicler-envvar \
    channel \
    debug \

LIBRARIES = $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------

all: test clean

test: $(TESTS)
	./sanity
	./state
	./index
	./index-state
	./chronicler
	DEBUG_OPT=pyre.journal.test1:pyre.journal.test2 ./chronicler-envvar
	./channel
	./debug


sanity: sanity.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

state: state.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

index: index.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

index-state: index-state.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

chronicler: chronicler.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

chronicler-envvar: chronicler-envvar.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

channel: channel.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug: debug.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)


# end of file 
