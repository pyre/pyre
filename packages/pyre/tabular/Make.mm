# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = tabular
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Aggregator.py \
    CSV.py \
    Chart.py \
    Column.py \
    Dimension.py \
    Index.py \
    InferredDimension.py \
    IntervalDimension.py \
    Measure.py \
    Pivot.py \
    Record.py \
    Reduction.py \
    Sheet.py \
    SheetMaker.py \
    View.py \
    exceptions.py \
    measures.py \
    __init__.py


export:: export-package-python-modules

# end of file 
