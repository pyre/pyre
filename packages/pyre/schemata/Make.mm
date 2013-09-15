# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = schemata
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Array.py \
    Boolean.py \
    Component.py \
    Date.py \
    Decimal.py \
    Dimensional.py \
    Float.py \
    INet.py \
    InputStream.py \
    Integer.py \
    List.py \
    Numeric.py \
    OutputStream.py \
    Schema.py \
    Sequence.py \
    Set.py \
    String.py \
    Time.py \
    Tuple.py \
    Typed.py \
    URI.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
