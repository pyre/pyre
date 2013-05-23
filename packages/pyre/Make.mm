# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    descriptors \
    extensions \
    externals \
    filesystem \
    framework \
    ipc \
    parsing \
    patterns \
    platforms \
    records \
    schemata \
    shells \
    tabular \
    timers \
    tracking \
    traits \
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


export:: __init__.py export-python-modules
	BLD_ACTION="export" $(MM) recurse
	@$(RM) __init__.py

# construct my {__init__.py}
__init__.py: __init__py
	@sed -e "s:BZR_REVNO:$$(bzr revno):g" __init__py > __init__.py


# end of file 
