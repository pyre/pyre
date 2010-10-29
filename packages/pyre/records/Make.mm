# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    Absolute.py \
    Addition.py \
    Binary.py \
    CSV.py \
    ConstAccessor.py \
    Derivation.py \
    Division.py \
    DynamicRecord.py \
    Field.py \
    FloorDivision.py \
    Minus.py \
    Multiplication.py \
    NodalDerivationAccessor.py \
    NodalFieldAccessor.py \
    Plus.py \
    Power.py \
    Record.py \
    Remainder.py \
    Subtraction.py \
    Templater.py \
    Unary.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
