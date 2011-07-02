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
    Equal.py \
    Expression.py \
    FloorDivision.py \
    Greater.py \
    GreaterEqual.py \
    Inverse.py \
    Less.py \
    LessEqual.py \
    Literal.py \
    Modulus.py \
    Multiplication.py \
    Node.py \
    NotEqual.py \
    Opposite.py \
    Or.py \
    Power.py \
    Unary.py \
    __init__.py


export:: export-package-python-modules

# end of file 
