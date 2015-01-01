# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre
PACKAGE = records
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Accessor.py \
    CSV.py \
    Calculator.py \
    Compiler.py \
    Evaluator.py \
    Extractor.py \
    Immutable.py \
    Mutable.py \
    NamedTuple.py \
    Record.py \
    Selector.py \
    Templater.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file
