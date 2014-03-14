# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = algebraic
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    AbstractNode.py \
    Algebra.py \
    Arithmetic.py \
    Boolean.py \
    Category.py \
    Composite.py \
    Leaf.py \
    Literal.py \
    Operator.py \
    Ordering.py \
    Variable.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
