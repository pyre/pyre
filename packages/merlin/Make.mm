# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = merlin
PACKAGE = merlin
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)

RECURSE_DIRS = \
    assets \
    components \
    schemata \
    spells \


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
