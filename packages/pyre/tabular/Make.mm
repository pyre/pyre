# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre
PACKAGE = tabular
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


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
    Derivation.py \
    Dimension.py \
    Index.py \
    InferredDimension.py \
    IntervalDimension.py \
    Measure.py \
    Pivot.py \
    Record.py \
    Reduction.py \
    Sheet.py \
    Templater.py \
    View.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
