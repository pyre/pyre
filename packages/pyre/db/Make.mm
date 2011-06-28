# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

PROJECT = pyre
PACKAGE = db
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Column.py \
    ColumnReference.py \
    DataStore.py \
    SQL.py \
    Schemer.py \
    Server.py \
    Table.py \
    View.py \
    actions.py \
    columns.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
