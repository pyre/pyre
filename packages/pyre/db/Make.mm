# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

PROJECT = pyre
PACKAGE = db
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Client.py \
    Collation.py \
    DataStore.py \
    FieldReference.py \
    FieldSelector.py \
    ForeignKey.py \
    Measure.py \
    Postgres.py \
    Query.py \
    Reference.py \
    SQL.py \
    SQLite.py \
    Schemer.py \
    Selector.py \
    Server.py \
    Table.py \
    actions.py \
    exceptions.py \
    expressions.py \
    literals.py \
    __init__.py


export:: export-package-python-modules

# end of file 
