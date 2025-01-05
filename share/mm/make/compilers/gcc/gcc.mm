# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# register {gcc} as the C compiler
compiler.c := gcc

# the name of the executable
gcc.driver ?= gcc

# prefices for specific categories
gcc.prefix.flags :=
gcc.prefix.defines := -D
gcc.prefix.incpath := -I

gcc.prefix.ldflags :=
gcc.prefix.libpath := -L
gcc.prefix.rpath := -Wl,-rpath,
gcc.prefix.libraries := -l

# compile time flags
gcc.compile.only := -c
gcc.compile.output := -o
gcc.compile.makedep := -MD
gcc.compile.base := -fno-diagnostics-color -pipe $(gcc.compile.makedep)
gcc.compile.isysroot := -isysroot

# symbols and optimization
gcc.debug := -g
gcc.reldeb := -g -O
gcc.opt := -O3
gcc.cov := --coverage
gcc.prof := -pg
gcc.shared := -fPIC

# language level
gcc.std.ansi := -ansi
gcc.std.c90 := -std=c90
gcc.std.c99 := -std=c99
gcc.std.c11 := -std=c11

# link time flags
gcc.link.output := -o
# link a dynamically loadable library
gcc.link.dll = $(platform.c.dll)
# link an extension
gcc.link.ext = $(platform.c.ext)

# command line options
gcc.defines = MM_COMPILER_gcc

# clean up temporaries left behind while compiling
#  usage: gcc.clean {base-name}
gcc.clean = $(1).d

# dependency generation
# gcc does this in one pass: the dependency file gets generated during the compilation phase so
# there is no extra step necessary to build it
#   usage: gcc.makedep {source} {depfile} {external dependencies}
define gcc.makedep =
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
