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
    world \
    group \
    group-include \
    group-exclude \
    group-setops \
    communicator \

LIBRARIES = $(EXTERNAL_LIBS)

#--------------------------------------------------------------------------

all: test


test: $(TESTS)
	$(MPI_EXECUTIVE) -np 4 ./sanity
	$(MPI_EXECUTIVE) -np 4 ./world
	$(MPI_EXECUTIVE) -np 4 ./group
	$(MPI_EXECUTIVE) -np 7 ./group-include
	$(MPI_EXECUTIVE) -np 7 ./group-exclude
	$(MPI_EXECUTIVE) -np 7 ./group-setops
	$(MPI_EXECUTIVE) -np 8 ./communicator

sanity: sanity.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

world: world.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

group: group.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

group-include: group-include.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

group-exclude: group-exclude.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

group-setops: group-setops.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

communicator: communicator.cc
	$(CXX) $(CXXFLAGS) $< -o $@ $(LCXXFLAGS) $(LIBRARIES)

# end of file 
