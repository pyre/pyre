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
    And.py \
    Binary.py \
    Division.py \
    Equal.py \
    FloorDivision.py \
    Greater.py \
    GreaterEqual.py \
    Less.py \
    LessEqual.py \
    Literal.py \
    Modulus.py \
    Multiplication.py \
    Node.py \
    NotEqual.py \
    Operator.py \
    Opposite.py \
    Or.py \
    Power.py \
    Subtraction.py \
    Unary.py \
    __init__.py


export:: export-package-python-modules

# end of file 
