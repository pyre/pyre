# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


compiler.cython := cython

# prefices for specific categories
cython.prefix.flags :=
cython.prefix.incpath := -I

# compile time flags
cython.compile.base += -3 --cplus --line-directives
cython.compile.only :=
cython.compile.output := -o

# symbols and optimization; not {cython}'s job really, but the compiler protocol requires them
cython.debug :=
cython.reldeb :=
cython.opt :=
cython.cov :=
cython.prof :=
cython.shared :=


# end of file
