# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = calc
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Average.py \
    Calculator.py \
    Const.py \
    Count.py \
    Evaluator.py \
    Expression.py \
    Filter.py \
    Hierarchical.py \
    Interpolation.py \
    Maximum.py \
    Memo.py \
    Minimum.py \
    Node.py \
    Observable.py \
    Observer.py \
    Preprocessor.py \
    Postprocessor.py \
    Probe.py \
    Product.py \
    Reference.py \
    Sum.py \
    SymbolTable.py \
    Unresolved.py \
    Value.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
