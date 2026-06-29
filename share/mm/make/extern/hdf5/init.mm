# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter hdf5,$(extern)},,hdf5}

# find my configuration file
hdf5.config := ${dir ${call extern.config,hdf5}}

hdf5.parallel ?= off
# {parallel} selects serial vs mpi-aware hdf5, so it must always carry a value; declare it required
hdf5.markers.required ?= parallel
hdf5.markers.required.hint ?= "(hdf5.parallel must be 'on' or 'off')"

# compiler flags
hdf5.flags ?=
# enable {hdf5} aware code
hdf5.defines := WITH_HDF5
# the canonical form of the include directory
hdf5.incpath ?= $(hdf5.dir)/include
# header marker(s): files that must resolve on {incpath}; absence proves breakage
hdf5.markers.headers ?= hdf5.h H5Cpp.h

# linker flags
hdf5.ldflags ?=
# the canonical form of the lib directory
hdf5.libpath ?= $(hdf5.dir)/lib
# its rpath
hdf5.rpath = $(hdf5.libpath)
# the names of the libraries
hdf5.libraries := hdf5_cpp hdf5

# my dependencies; a parallel build links against {mpi}, so a {parallel} value naming it induces a
# load-time edge that pulls {mpi} into any asset that depends on {hdf5}. evaluated lazily so it sees
# the effective {hdf5.parallel}, whether defaulted here, set by the user, or detected by the pkgdb
hdf5.dependencies = ${if ${findstring mpi,$(hdf5.parallel)},mpi}


# end of file
