# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre
PACKAGE = pyre
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)

RECURSE_DIRS = \
    algebraic \
    calc \
    components \
    config \
    constraints \
    db \
    filesystem \
    framework \
    ipc \
    parsing \
    patterns \
    records \
    schema \
    shells \
    tabular \
    timers \
    tracking \
    units \
    weaver \
    xml \


#--------------------------------------------------------------------------
#

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    __init__.py


export:: export-python-modules
	BLD_ACTION="export" $(MM) recurse

# end of file 
