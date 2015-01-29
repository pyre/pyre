# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# access the machinery for building shared objects
include shared/target.def
# project defaults
include pyre.def
# the package name
PACKAGE = timers
# my subfolders
RECURSE_DIRS = \
    epoch \
    mach \
    posix \

# libraries
PROJ_SAR = $(BLD_LIBDIR)/lib$(PROJECT)-$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/lib$(PROJECT)-$(PACKAGE).$(EXT_SO)
# sources
PROJ_SRCS = \
    Display.cc \
    Timer.cc \
# the target
EXPORT_LIBS = $(PROJ_DLL)
# top level header
EXPORT_HEADERS = \
    timers.h \
# headers scoped by the package name
EXPORT_PKG_HEADERS = \
    Display.h Display.icc \
    Timer.h Timer.icc

# standard targets
all: $(PROJ_DLL) export
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: export-headers export-package-headers export-libraries
	BLD_ACTION="export" $(MM) recurse

live: live-headers live-package-headers live-libraries
	BLD_ACTION="live" $(MM) recurse

# end of file
