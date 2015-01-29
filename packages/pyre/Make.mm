# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# the name of the package
PACKAGE = pyre
# add this to the clean pile
PROJ_CLEAN += $(EXPORT_MODULEDIR)
# my subfolders
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
    geometry \
    ipc \
    nexus \
    parsing \
    patterns \
    platforms \
    primitives \
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
# the python modules
EXPORT_PYTHON_MODULES = \
    __init__.py

# standard targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: __init__.py export-python-modules
	BLD_ACTION="export" $(MM) recurse
	@$(RM) __init__.py

live: live-python-modules
	BLD_ACTION="live" $(MM) recurse

# construct my {__init__.py}
__init__.py: __init__py
	@sed -e "s:BZR_REVNO:$$(bzr revno):g" __init__py > __init__.py

# end of file
