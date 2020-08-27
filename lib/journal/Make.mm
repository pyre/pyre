# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2020 all rights reserved
#

# get the machinery for building shared objects
include shared/target.def
# project defaults
include pyre.def
# the package name
PACKAGE = journal
# the sources
PROJ_SRCS = \
    debuginfo.cc \
    firewalls.cc \
    ANSI.cc \
    ANSI_x11.cc \
    Alert.cc \
    Chronicler.cc \
    Console.cc \
    Device.cc \
    ErrorConsole.cc \
    File.cc \
    Memo.cc \
    Renderer.cc \
    Splitter.cc \
    Stream.cc \
    Trash.cc

# the products
PROJ_SAR = $(BLD_LIBDIR)/lib$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/lib$(PACKAGE).$(EXT_SO)
# the private build space
PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/lib/$(PACKAGE)
# what to clean
PROJ_CLEAN += $(EXPORT_LIBS) $(EXPORT_INCDIR)

# what to export
# the library
EXPORT_LIBS = $(PROJ_DLL)
# the top level header
EXPORT_HEADERS = \
    journal.h

# the headers that are scoped by my project name
EXPORT_PKG_HEADERS = \
    api.h \
    debuginfo.h \
    exceptions.h exceptions.icc \
    externals.h \
    firewalls.h \
    forward.h \
    macros.h \
    manipulators.h \
    public.h \
    ANSI.h \
    ASCII.h \
    Alert.h \
    CSI.h CSI.icc \
    Channel.h Channel.icc \
    Chronicler.h Chronicler.icc \
    Console.h Console.icc \
    Debug.h Debug.icc \
    Device.h Device.icc \
    Entry.h Entry.icc \
    Error.h Error.icc \
    ErrorConsole.h ErrorConsole.icc \
    File.h File.icc \
    Firewall.h Firewall.icc \
    Flush.h Flush.icc \
    Index.h Index.icc \
    Informational.h Informational.icc \
    Inventory.h Inventory.icc \
    InventoryProxy.h InventoryProxy.icc \
    Locator.h Locator.icc \
    Memo.h \
    Note.h Note.icc \
    Null.h Null.icc \
    Renderer.h \
    Splitter.h \
    Stream.h Stream.icc \
    Trash.h Trash.icc \
    Verbosity.h Verbosity.icc \
    Warning.h Warning.icc

# the standard targets
all: export

export:: $(PROJ_DLL) export-headers export-package-headers export-libraries

live: live-headers live-package-headers live-libraries

# archiving support
zipit:
	cd $(EXPORT_ROOT); \
        zip -r $(PYRE_ZIP) lib/lib$(PACKAGE).$(EXT_SO); \
        zip -r $(PYRE_ZIP) ${addprefix include/pyre/, $(EXPORT_HEADERS)} ; \
        zip -r $(PYRE_ZIP) include/pyre/$(PACKAGE)

# end of file
