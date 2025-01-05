# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# cython
languages.cython.sources := .pyx
languages.cython.headers := .pxd .pxi

# language predicates
languages.cython.compiled := yes
languages.cython.interpreted :=

# flags
languages.cython.categories.compile := flags incpath
languages.cython.categories.link :=

# build a compile command line
#  usage: languages.cython.compile {source-file} {target-object} {dependencies}
languages.cython.compile = ${call compiler.compile,cython,$(compiler.cython),$(1),$(2),$(3)}


# end of file
