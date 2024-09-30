# -*- Makefile -*-
#
# michael a.g. aïvázis <mmichael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# register {gfortran} as the FORTRAN compiler
compiler.fortran := gfortran

# the name of the executable
gfortran.driver ?= gfortran

# prefices for specific categories
gfortran.prefix.flags :=
gfortran.prefix.defines := -D
gfortran.prefix.incpath := -I

gfortran.prefix.ldflags :=
gfortran.prefix.libpath := -L
gfortran.prefix.rpath := -Wl,-rpath,
gfortran.prefix.libraries := -l

# compile time flags
gfortran.compile.base := -pipe
gfortran.compile.only := -c
gfortran.compile.output := -o
gfortran.compile.makedep :=

# symbols and optimization
gfortran.debug := -g
gfortran.reldeb := -g -O
gfortran.opt := -O3
gfortran.cov := -coverage
gfortran.prof := -pg
gfortran.shared := -fPIC

# language level
gfortran.std.f77 :=
gfortran.std.f95 := -std=f95
gfortran.std.f03 := -std=f2003
gfortran.std.f08 := -std=f2008
gfortran.std.legacy := -std=legacy

# link time flags
gfortran.link.output := -o
gfortran.link.shared :=
# link a dynamically loadable library
gfortran.link.dll := -shared

# mixed language programming
gfortran.mixed.flags ?=
gfortran.mixed.defines ?=
gfortran.mixed.incpath ?=
gfortran.mixed.ldflags ?=
gfortran.mixed.libpath ?=
gfortran.mixed.libraries += gfortran

# dependency generation
# gfortran cannot generate dependencies
define gfortran.makedep =
endef


# end of file
