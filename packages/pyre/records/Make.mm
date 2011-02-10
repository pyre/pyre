# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre
PACKAGE = records
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Accessor.py \
    CSV.py \
    ConstAccessor.py \
    Derivation.py \
    DynamicRecord.py \
    Field.py \
    FieldProxy.py \
    Record.py \
    Templater.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
