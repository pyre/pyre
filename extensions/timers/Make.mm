# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# find out what kind of clock support is provided by this platform
include clock/default.def

# project defaults
include pyre.def
# package name
PACKAGE = extensions
# the module
MODULE = timers
# build a python extension
include std-pythonmodule.def
# use a tmp directory that knows the name of the module
PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)/$(MODULE)
# link against these
PROJ_LIBRARIES = -lpyre -ljournal
# the sources
PROJ_SRCS = \
    display.cc \
    metadata.cc

# end of file
