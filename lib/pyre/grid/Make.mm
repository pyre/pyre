# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# access the machinery for building shared objects
include shared/target.def
# project defaults
include pyre.def
# the name of the package
PACKAGE = grid

# the products
PROJ_SAR = $(BLD_LIBDIR)/lib$(PROJECT).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/lib$(PROJECT).$(EXT_SO)
# the private build space
PROJ_TMPDIR = $(BLD_TMPDIR)/${PROJECT}/lib/$(PROJECT)
# the sources
PROJ_SRCS = \
    MemoryMap.cc \

# what to clean
PROJ_CLEAN += $(EXPORT_INCDIR)/$(PACKAGE)

# what to export
# the library
EXPORT_LIBS = $(PROJ_DLL)
EXPORT_HEADERS = \
    grid.h \
# the package headers
EXPORT_PKG_HEADERS = \
    Direct.h Direct.icc \
    Index.h Index.icc \
    Iterator.h Iterator.icc \
    Layout.h Layout.icc \
    MemoryMap.h \
    Slice.h Slice.icc \
    Tile.h Tile.icc \
    public.h

# the standard targets
all: export

export:: $(PROJ_DLL) export-headers export-package-headers export-libraries

# end of file
