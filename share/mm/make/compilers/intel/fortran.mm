# -*- Makefile -*-
#
# michael a.g. aïvázis <mmichael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# register {ifx} as the FORTRAN compiler
compiler.fortran := ifx

# the name of the executable
ifx.driver ?= ifx

# prefices for specific categories
ifx.prefix.flags :=
ifx.prefix.defines := -D
ifx.prefix.incpath := -I

ifx.prefix.ldflags :=
ifx.prefix.libpath := -L
ifx.prefix.rpath := -Wl,-rpath,
ifx.prefix.libraries := -l

# compile time flags
ifx.compile.base := -fpp -nologo
ifx.compile.only := -c
ifx.compile.output := -o
ifx.compile.makedep :=

# symbols and optimization
ifx.debug := -g -traceback -check all
ifx.reldeb := -g -O2 -traceback
ifx.opt := -O3 -xHost
ifx.cov := -profile-functions -profile-loops=all
ifx.prof := -pg
ifx.shared := -fPIC

# language level
ifx.std.f77 :=
ifx.std.f95 := -std=f95
ifx.std.f03 := -std=f2003
ifx.std.f08 := -std=f2008
ifx.std.legacy :=

# link time flags
ifx.link.output := -o
ifx.link.shared :=
# link a dynamically loadable library
ifx.link.dll := -shared

# mixed language programming
ifx.mixed.flags ?=
ifx.mixed.defines ?=
ifx.mixed.incpath ?=
ifx.mixed.ldflags ?=
ifx.mixed.libpath ?=
ifx.mixed.libraries += ifcore ifport

# dependency generation
# ifx cannot generate dependencies
define ifx.makedep =
endef


# end of file
