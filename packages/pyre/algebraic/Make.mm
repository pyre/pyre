# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = algebraic
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
    FloorDivision.py \
    Increment.py \
    Inverse.py \
    LeftModulus.py \
    LeftFloorDivision.py \
    LeftPower.py \
    Modulus.py \
    Multiplication.py \
    Node.py \
    Opposite.py \
    Power.py \
    PseudoUnary.py \
    RightFloorDivision.py \
    RightModulus.py \
    RightPower.py \
    Scaling.py \
    Unary.py \
    __init__.py


export:: export-package-python-modules

# end of file 
