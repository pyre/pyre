# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = calc
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Average.py \
    Count.py \
    Dependent.py \
    Error.py \
    Expression.py \
    HierarchicalModel.py \
    Literal.py \
    Maximum.py \
    Minimum.py \
    Model.py \
    Node.py \
    Operator.py \
    Probe.py \
    Product.py \
    Reference.py \
    Sum.py \
    SymbolTable.py \
    UnresolvedNode.py \
    Variable.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
