# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# register {flang} as the FORTRAN compiler
compiler.fortran := flang

# the name of the executable
flang.driver ?= flang

# prefices for specific categories
flang.prefix.flags :=
flang.prefix.defines := -D
flang.prefix.incpath := -I

flang.prefix.ldflags :=
flang.prefix.libpath := -L
# VERIFY: rpath syntax; flang is LLVM-based so this should match clang
flang.prefix.rpath := -Wl,-rpath,
flang.prefix.libraries := -l

# compile time flags
# flang has no {-pipe}; leave the base empty
flang.compile.base :=
flang.compile.only := -c
flang.compile.output := -o
flang.compile.makedep :=

# symbols and optimization
flang.debug := -g
# VERIFY: gfortran uses -g -O; using -g -O2 here as a conservative LLVM-friendly choice
flang.reldeb := -g -O2
flang.opt := -O3
# VERIFY: --coverage (LLVM style) vs -coverage (GCC style); flang-new likely uses --coverage
flang.cov := --coverage
# VERIFY: gprof-style -pg has limited support in LLVM Fortran; may silently do nothing
flang.prof := -pg
flang.shared := -fPIC
# openmp support
flang.openmp := -fopenmp

# language level
# VERIFY: all std flags below; they mirror gfortran but flang-new may differ
flang.std.f77 :=
flang.std.f95 := -std=f95
flang.std.f03 := -std=f2003
# VERIFY: flang-new targets f2018 rather than f2008; adjust if your version uses -std=f2008
flang.std.f08 := -std=f2018
# VERIFY: -std=legacy is gfortran-only; leaving empty — let us know if you need a replacement
flang.std.legacy :=

# link time flags
flang.link.output := -o
flang.link.shared :=
# link a dynamically loadable library
flang.link.dll := -shared

# mixed language programming
flang.mixed.flags ?=
flang.mixed.defines ?=
flang.mixed.incpath ?=
flang.mixed.ldflags ?=
flang.mixed.libpath ?=
flang.mixed.libraries += flang_rt.runtime

# dependency generation
# flang cannot generate dependencies (leave empty; revisit if flang-new gains -MD support)
define flang.makedep =
endef


# end of file
