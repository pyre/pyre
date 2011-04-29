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
    index \
    chronicler \
    chronicler-envvar \
    debug \

LIBRARIES = $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------

all: test clean

test: $(TESTS)
	./sanity
	./index
	./chronicler
	DEBUG_OPT=pyre.journal.test1:pyre.journal.test2 ./chronicler-envvar
	./debug


sanity: sanity.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

index: index.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

chronicler: chronicler.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

chronicler-envvar: chronicler-envvar.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

debug: debug.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)


# end of file 
