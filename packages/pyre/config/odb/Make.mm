# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre
PACKAGE = config/odb
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    ODB.py \
    Shelf.py \
    __init__.py


export:: export-package-python-modules

# end of file 
