# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = traits
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Array.py \
    Behavior.py \
    Bool.py \
    Dict.py \
    Dimensional.py \
    Facility.py \
    Float.py \
    INet.py \
    InputFile.py \
    Integer.py \
    List.py \
    Object.py \
    OutputFile.py \
    Property.py \
    Set.py \
    Sequence.py \
    Slotted.py \
    String.py \
    Trait.py \
    Tuple.py \
    URI.py \
    properties.py \
    __init__.py


export:: export-package-python-modules

# end of file 
