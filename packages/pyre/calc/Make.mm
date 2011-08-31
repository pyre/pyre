# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
    AbstractModel.py \
    Absolute.py \
    Addition.py \
    Aggregator.py \
    Average.py \
    Binary.py \
    Count.py \
    Division.py \
    Error.py \
    Evaluator.py \
    Expression.py \
    Function.py \
    HierarchicalModel.py \
    Literal.py \
    Maximum.py \
    Minimum.py \
    Model.py \
    Multiplication.py \
    Node.py \
    Opposite.py \
    Polyadic.py \
    Power.py \
    Probe.py \
    Product.py \
    Reductor.py \
    Reference.py \
    Subtraction.py \
    Sum.py \
    Unary.py \
    UnresolvedNode.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
