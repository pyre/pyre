# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# get the machinery for building shared objects
include shared/target.def
# project defaults
include pyre.def
# the package name
PACKAGE = journal
# the products
PROJ_SAR = $(BLD_LIBDIR)/lib$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/lib$(PACKAGE).$(EXT_SO)
# the sources
PROJ_SRCS = \
    debuginfo.cc \
    firewalls.cc \
    journal.cc \
    Chronicler.cc \
    Console.cc \
    Device.cc \
    Renderer.cc \
    Streaming.cc \
# what to export
# the library
EXPORT_LIBS = $(PROJ_DLL)
# the top level header
EXPORT_HEADERS = \
    journal.h
# the headers that are scoped by my project name
EXPORT_PKG_HEADERS = \
    debuginfo.h \
    firewalls.h \
    macros.h \
    manipulators.h manipulators.icc \
    Channel.h Channel.icc \
    Chronicler.h Chronicler.icc \
    Console.h \
    Debug.h Debug.icc \
    Device.h Device.icc \
    Diagnostic.h Diagnostic.icc \
    Error.h Error.icc \
    Firewall.h Firewall.icc \
    Index.h Index.icc \
    Informational.h Informational.icc \
    Inventory.h Inventory.icc \
    Locator.h Locator.icc \
    Null.h Null.icc \
    Renderer.h Renderer.icc \
    Selector.h Selector.icc \
    Streaming.h Streaming.icc \
    Warning.h Warning.icc \

# the standard targets
all: $(PROJ_DLL) export

export:: export-headers export-package-headers export-libraries

live: live-headers live-package-headers live-libraries

# end of file
