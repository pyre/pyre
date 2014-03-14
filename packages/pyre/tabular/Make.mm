# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = tabular
PROJ_CLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Chart.py \
    Column.py \
    Dimension.py \
    Inferred.py \
    Interval.py \
    Measure.py \
    Pivot.py \
    Primary.py \
    Reduction.py \
    Selector.py \
    Sheet.py \
    Surveyor.py \
    Tabulator.py \
    View.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
