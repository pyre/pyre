# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter kokkos,$(extern)},,kokkos}

# find my configuration file
kokkos.config := ${dir ${call extern.config,kokkos}}

# compiler flags
kokkos.flags ?=
# enable {kokkos} aware code
kokkos.defines := WITH_KOKKOS
# the canonical form of the include directory
kokkos.incpath ?= $(kokkos.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
kokkos.markers.headers ?= Kokkos_Core.hpp

# linker flags
kokkos.ldflags ?=
# the canonical form of the lib directory
kokkos.libpath ?= $(kokkos.dir)/lib
# its rpath
kokkos.rpath = $(kokkos.libpath)
# the set of kokkos libraries to link against
kokkos.libraries ?=


# end of file
