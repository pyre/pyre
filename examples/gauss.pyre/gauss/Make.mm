# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = gauss
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)

RECURSE_DIRS = \
    functors \
    integrators \
    meshes \
    shapes \
    util \


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
