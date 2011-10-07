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
    AbstractNode.py \
    Boolean.py \
    Cast.py \
    Composite.py \
    Expression.py \
    Hierarchical.py \
    Leaf.py \
    Literal.py \
    Memo.py \
    Node.py \
    Number.py \
    Operator.py \
    Ordering.py \
    Reference.py \
    SymbolTable.py \
    Unresolved.py \
    Variable.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
