# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# default compilers; specify as many as necessary in the form {family} or {family/language}
platform.compilers = clang gcc/gfortran python cython

# clean up the debug symbols compilers leave behind
#     platform.clean {stem}
platform.clean = $(1).dSYM

# the location of the system headers
platform.isysroot := /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk

# c
platform.c.flags = -arch arm64 $($(compiler.c).compile.isysroot) $(platform.isysroot)
platform.c.ldflags := -Wl,-headerpad_max_install_names -Wl,-dead_strip_dylibs -Wl,-undefined,dynamic_lookup
platform.c.dll = -dynamiclib
platform.c.ext = -bundle
# c++
platform.c++.flags = -arch arm64 $($(compiler.c++).compile.isysroot) $(platform.isysroot)
platform.c++.ldflags := -Wl,-headerpad_max_install_names -Wl,-dead_strip_dylibs -Wl,-undefined,dynamic_lookup
platform.c++.dll = -dynamiclib
platform.c++.ext = -bundle


# end of file
