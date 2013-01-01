# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    Container.py \
    Date.py \
    Decimal.py \
    Dimensional.py \
    Float.py \
    INet.py \
    Integer.py \
    List.py \
    Object.py \
    String.py \
    Time.py \
    Tuple.py \
    Type.py \
    URI.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
