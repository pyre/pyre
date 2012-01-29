# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    Collation.py \
    DataStore.py \
    Entry.py \
    Field.py \
    FieldReference.py \
    ForeignKey.py \
    Postgres.py \
    Query.py \
    SQL.py \
    Selector.py \
    Schemer.py \
    Selection.py \
    Server.py \
    Table.py \
    View.py \
    actions.py \
    fields.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
