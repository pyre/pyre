# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

PROJECT = pyre
PACKAGE = doc/gauss/simple

PROJ_TIDY += gauss
PROJ_CLEAN += gauss.dSYM

include gsl/default.def

#--------------------------------------------------------------------------
#

all: gauss

gauss: gauss.cc
	$(CXX) $(CXXFLAGS) -o $@ gauss.cc $(LCXXFLAGS) $(EXTERNAL_LIBS)


# end of file
