# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    CSV.py \
    Column.py \
    Derivation.py \
    Index.py \
    Measure.py \
    Pivot.py \
    Record.py \
    Sheet.py \
    Templater.py \
    View.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
