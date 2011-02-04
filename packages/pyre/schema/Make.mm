# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre
PACKAGE = schema
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Array.py \
    Boolean.py \
    Date.py \
    Decimal.py \
    Dimensional.py \
    Descriptor.py \
    Float.py \
    Integer.py \
    Object.py \
    String.py \
    Time.py \
    Type.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
