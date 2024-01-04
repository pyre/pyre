# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# cuda
languages.cuda.sources := .cu
languages.cuda.headers := .h

# language predicates
languages.cuda.compiled := yes
languages.cuda.interpreted :=

# flags
languages.cuda.categories.compile := flags defines incpath
languages.cuda.categories.link := ldflags libpath libraries


# build a compile command line
#  usage: languages.cuda.compile {source-file} {target-object} {dependencies}
languages.cuda.compile = ${call compiler.compile,cuda,$(compiler.cuda),$(1),$(2),$(3)}


# build a device link command line
#  usage: languages.cuda.dlink {source-file} {executable} {dependencies}
languages.cuda.dlink = ${call compiler.dlink,cuda,$(compiler.cuda),$(1),$(2),$(3)}


# build a link command line
#  usage: languages.cuda.link {source-file} {executable} {dependencies}
languages.cuda.link = ${call compiler.link,cuda,$(compiler.cuda),$(1),$(2),$(3)}


# build a link command line that builds a dll
#  usage: languages.cuda.dll {source-file} {dll} {dependencies}
languages.cuda.dll = ${call compiler.dll,cuda,$(compiler.cuda),$(1),$(2),$(3)}


# end of file
