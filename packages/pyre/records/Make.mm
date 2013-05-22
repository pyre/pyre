# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = records
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Accessor.py \
    CSV.py \
    ConstAccessor.py \
    Derivation.py \
    DynamicRecord.py \
    Entry.py \
    Field.py \
    Immutable.py \
    Literal.py \
    Mutable.py \
    NamedTuple.py \
    Record.py \
    Templater.py \
    exceptions.py \
    fields.py \
    __init__.py


export:: export-package-python-modules

# end of file 
