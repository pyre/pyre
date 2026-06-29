# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter mpi,$(extern)},,mpi}

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
# header marker(s): files that must resolve on {incpath}; absence proves breakage
mpi.markers.headers ?= mpi.h

# linker flags
mpi.ldflags ?=
# the canonical form of the lib directory
mpi.libpath ?= $(mpi.dir)/lib
# its rpath
mpi.rpath = $(mpi.libpath)
# the names of the libraries are flavor dependent
mpi.libraries := \
    ${if ${findstring openmpi,$(mpi.flavor)},\
       ${if \
         ${filter 1 2 3 4,${firstword ${subst ., ,$(mpi.version)}}},\
         mpi_cxx mpi, \
         mpi \
       } \
    } \
    ${if ${findstring mpich,$(mpi.flavor)},\
         mpi pmpi \
    }
# {libraries} is critical: an unrecognized flavor leaves it empty and the link silently drops the
# mpi symbols, so declare it required and hint at the most likely cause
mpi.markers.required ?= libraries
mpi.markers.required.hint ?= "(mpi.flavor='$(mpi.flavor)' unrecognized; expected openmpi or mpich)"


# end of file
