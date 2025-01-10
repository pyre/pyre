# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# register {nvcc} as the CUDA compiler
compiler.cuda := nvcc

# the name of the executable
nvcc.driver ?= nvcc

# prefices for specific categories
nvcc.prefix.flags :=
nvcc.prefix.defines := -D
nvcc.prefix.incpath := -I

nvcc.prefix.ldflags :=
nvcc.prefix.libpath := -L
nvcc.prefix.libraries := -l

# compile time flags
nvcc.compile.base :=
nvcc.compile.only := -dc
nvcc.compile.output := -o
nvcc.compile.makedep := -M

# language selection
nvcc.force.c := --x c
nvcc.force.c++ := --x c++
nvcc.force.cu := --x cu

# symbols and optimization
nvcc.debug := -g
nvcc.reldeb := -g -O
nvcc.opt := -O3
nvcc.cov := --coverage
nvcc.prof := -pg
nvcc.shared := -Xcompiler -fPIC

# language level
nvcc.std.c++03 := --std=c++03
nvcc.std.c++11 := --std=c++11
nvcc.std.c++14 := --std=c++14
nvcc.std.c++17 := --std=c++17
nvcc.std.c++20 := --std=c++20 # cuda 12.x

# link time flags
nvcc.link.output := -o
nvcc.link.shared :=
nvcc.link.device := -dlink
# link a dynamically loadable library
nvcc.link.dll := -shared

# command line options
nvcc.defines = MM_COMPILER_nvcc

# clean up temporaries left behind while compiling
#  usage: nvcc.clean {base-name}
nvcc.clean = $(1).d

# dependency generation
# nvcc does this in two passes: the dependency file gets generated during an additional compilation
# phase, so there is an extra step necessary to build it
# N.B. the adjustments necessary to transform the dependency file into canonical form appear to be
#      the same as {gcc}; this may not be the case if nvcc uses a different compiler underneath, so
#      this is something that has to be investigated
#   usage: nvcc.makedep {source} {depfile} {external dependencies}
define nvcc.makedep =
    nvcc \
        $(1) \
        $(nvcc.compile.base) \
        $(nvcc.compile.makedep) \
        ${call compiler.compile.options,cuda,nvcc,$(3)} > $(2) ; \
    $(cp) $(2) $(2).tmp ; \
    $(sed) \
        -e 's/\#.*//' \
        -e 's/^[^:]*: *//' \
        -e 's/ *\\$$$$//' \
        -e '/^$$$$/d' \
        -e 's/$$$$/ :/' \
        $(2) >> $(2).tmp ; \
    $(mv) $(2).tmp $(2)
endef


# end of file
