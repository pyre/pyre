# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

# project defaults
include pyre.def
# package name
PACKAGE = extensions
# the module
MODULE = host
# build a python extension
include std-pythonmodule.def
# use a tmp directory that knows the name of the module
PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)/$(MODULE)
# link against these
PROJ_LIBRARIES = -ljournal
# the sources
PROJ_SRCS = \
    cpu.cc \
    metadata.cc

# end of file
