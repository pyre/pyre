# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = opal
PACKAGE = opal
PROJ_CLEAN += $(EXPORT_MODULEDIR)

RECURSE_DIRS = \
    html \
    shells \


# standard targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# export

EXPORT_PYTHON_MODULES = \
    __init__.py

export:: export-python-modules
	BLD_ACTION="export" $(MM) recurse


# end of file
