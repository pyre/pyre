# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

# project defaults
include journal.def
# package name
PACKAGE =
# the module
MODULE = journal
# build a python extension
include std-pythonmodule.def
# my headers
PROJ_INCDIR = $(BLD_INCDIR)/pyre/$(PROJECT)
# use a tmp directory that knows the name of the module
PROJ_TMPDIR = $(BLD_TMPDIR)/extensions/$(PROJECT)
# link against these
PROJ_LIBRARIES = -ljournal
# the sources
PROJ_SRCS = \
    api.cc \
    chronicler.cc \
    debug.cc \
    devices.cc \
    error.cc \
    exceptions.cc \
    firewall.cc \
    info.cc \
    warning.cc

# end of file
