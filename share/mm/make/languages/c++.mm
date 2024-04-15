# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# c++
languages.c++.sources := .cc .cpp .cxx .c++
languages.c++.headers := .h .hpp .hxx .h++ .icc

# language predicates
languages.c++.compiled := yes
languages.c++.interpreted :=

# flags
languages.c++.categories.compile := flags defines incpath
languages.c++.categories.link := ldflags libpath rpath libraries


# build a compile command line
#  usage: languages.c++.compile {source-file} {target-object} {dependencies}
languages.c++.compile = ${call compiler.compile,c++,$(compiler.c++),$(1),$(2),$(3)}


# build a link command line
#  usage: languages.c++.link {source-file} {executable} {dependencies}
languages.c++.link = ${call compiler.link,c++,$(compiler.c++),$(1),$(2),$(3)}


# build a link command line that builds a dll
#  usage: languages.c++.dll {source-file} {dll} {dependencies}
languages.c++.dll = ${call compiler.dll,c++,$(compiler.c++),$(1),$(2),$(3)}

# build a link command line that builds an extension
#  usage: languages.c++.ext {source-file} {ext} {dependencies}
languages.c++.ext = ${call compiler.ext,c++,$(compiler.c++),$(1),$(2),$(3)}


# end of file
