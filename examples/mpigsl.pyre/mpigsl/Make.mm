# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = mpigsl
PACKAGE = 
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Partitioner.py \
    __init__.py


export:: export-python-modules

# end of file 
