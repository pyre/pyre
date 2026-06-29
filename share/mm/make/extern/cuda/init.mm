# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add me to the pile
extern += ${if ${filter cuda,$(extern)},,cuda}

# find my configuration file
cuda.config := ${dir ${call extern.config,cuda}}

# compiler flags
cuda.flags ?=
# enable {cuda} aware code
cuda.defines += WITH_CUDA
# the canonical form of the include directory; cuda 13+ reorganized headers under cccl/
cuda.incpath ?= $(cuda.dir)/include ${wildcard $(cuda.dir)/include/cccl}
# header marker(s): files that must resolve on {incpath}; absence proves breakage
cuda.markers.headers ?= cuda_runtime.h

# linker flags
cuda.ldflags ?=
# the canonical form of the lib directory
cuda.libpath ?= $(cuda.dir)/lib64
# its rpath
cuda.rpath = $(cuda.libpath)
# the set of cuda libraries to link against
cuda.libraries ?=


# end of file
