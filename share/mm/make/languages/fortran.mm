# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# fortran
languages.fortran.sources := .f .f77 .f90 .f95 .f03 .F .F77 .F90 .F95 .F03
languages.fortran.headers := .h .inc
languages.fortran.modules := .mod

# language predicates
languages.fortran.compiled := yes
languages.fortran.interpreted :=

# flags
languages.fortran.categories.compile := flags defines incpath
languages.fortran.categories.link := ldflags libpath rpath libraries


# build a compile command line
#  usage: languages.fortran.compile {source-file} {target-object} {dependencies}
languages.fortran.compile = ${call compiler.compile,fortran,$(compiler.fortran),$(1),$(2),$(3)}


# build a link command line
#  usage: languages.fortran.link {source-file} {executable} {dependencies}
languages.fortran.link = ${call compiler.link,fortran,$(compiler.fortran),$(1),$(2),$(3)}


# build a link command line that builds a dll
#  usage: languages.fortran.dll {source-file} {dll} {dependencies}
languages.fortran.dll = ${call compiler.dll,fortran,$(compiler.fortran),$(1),$(2),$(3)}


# end of file
