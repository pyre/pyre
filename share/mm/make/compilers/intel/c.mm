# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# register {intel} as the C compiler
compiler.c = intel

# the name of the executable
intel.driver ?= icx

# prefices for specific categories
intel.prefix.flags :=
intel.prefix.defines := -D
intel.prefix.incpath := -I

intel.prefix.ldflags :=
intel.prefix.libpath := -L
intel.prefix.rpath := -Wl,-rpath,
intel.prefix.libraries := -l

# compile time flags
intel.compile.only := -c
intel.compile.output := -o
intel.compile.makedep := -MD
intel.compile.base := -pipe $(intel.compile.makedep)
intel.compile.isysroot := -isysroot

# symbols and optimization
intel.debug := -g
intel.opt := -O3
intel.reldeb := -g -O
intel.cov := --coverage
intel.prof := -pg
intel.shared := -fPIC

# language level
intel.std.ansi := -ansi
intel.std.c90 := -std=c90
intel.std.c99 := -std=c99
intel.std.c11 := -std=c11

# link time flags
intel.link.output := -o
# link a dynamically loadable library
intel.link.dll = $(platform.c.dll)
# link an extension
intel.link.ext = $(platform.c.ext)

# command line options
intel.defines = MM_COMPILER_intel

# clean up temporaries left behind while compiling
#  usage: intel.clean {base-name}
intel.clean = $(1).d

# dependency generation intel does this in one pass: the dependency file gets generated during
# the compilation phase so there is no extra step necessary to build it
#   usage: intel.makedep {source} {depfile} {external dependencies}
define intel.makedep =
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
