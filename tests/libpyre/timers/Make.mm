# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#

include clock/default.def

PROJECT = pyre
PACKAGE = timers

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(TESTS)


TESTS = timer

PROJ_LCXX_LIBPATH = $(BLD_LIBDIR)
LIBRARIES = -lpyre-timers $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------
all: test clean


test: $(TESTS)
	./timer


timer: timer.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)


# end of file 
