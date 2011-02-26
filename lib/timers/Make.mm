# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = timers

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_SAR = $(BLD_LIBDIR)/lib$(PROJECT)-$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/lib$(PROJECT)-$(PACKAGE).$(EXT_SO)

RECURSE_DIRS = \
    epoch \
    mach \
    posix \

PROJ_SRCS = \
    Display.cc \
    Timer.cc \


PROJ_TEMPLATES = \
    Display.h Display.icc \
    Timer.h Timer.icc\

#--------------------------------------------------------------------------
#

all: $(PROJ_DLL) export
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


export:: export-package-headers
	BLD_ACTION="export" $(MM) recurse


EXPORT_HEADERS = \
    timers.h \
    $(PROJ_TEMPLATES) 


# end of file 
