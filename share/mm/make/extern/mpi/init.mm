# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# add me to the pile
extern += ${if ${findstring mpi,$(extern)},,mpi}

# # find my configuration file
mpi.config := ${dir ${call extern.config,mpi}}

# users set this variable to communicate which libraries they want
mpi.required ?=

# the location of the binaries
mpi.binpath ?= $(mpi.dir)/bin
# the name of the launcher
mpi.executive ?= mpiexec

# compiler flags
mpi.flags ?=
# enable {mpi} aware code
mpi.defines := \
    WITH_MPI \
    ${if ${findstring mpich,$(mpi.flavor)}, WITH_MPICH,} \
    ${if ${findstring openmpi,$(mpi.flavor)}, WITH_OPENMPI,} \
# the canonical form of the include directory
mpi.incpath ?= $(mpi.dir)/include

# linker flags
mpi.ldflags ?=
# the canonical form of the lib directory
mpi.libpath ?= $(mpi.dir)/lib
# its rpath
mpi.rpath = $(mpi.libpath)
# the names of the libraries are flavor dependent
mpi.libraries := \
    ${if ${findstring openmpi,$(mpi.flavor)},mpi_cxx mpi $(mpi.required),}


# end of file
