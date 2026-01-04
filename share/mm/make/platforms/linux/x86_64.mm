# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# default compilers; specify as many as necessary in the form {family} or {family/language}
platform.compilers = gcc nvcc python cython

# clean up the debug symbols compilers leave behind
#     platform.clean {stem}
platform.clean :=

# the location of the system headers
platform.isysroot :=

# c
platform.c.flags :=
platform.c.ldflags :=
platform.c.dll = -shared
platform.c.ext = -shared
# c++
platform.c++.flags :=
platform.c++.ldflags :=
platform.c++.dll = -shared
platform.c++.ext = -shared


# end of file
