# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = descriptors
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Boolean.py \
    Converter.py \
    Decimal.py \
    Default.py \
    Descriptor.py \
    Dimensional.py \
    Float.py \
    INet.py \
    Integer.py \
    Normalizer.py \
    Object.py \
    Processor.py \
    Public.py \
    String.py \
    Typed.py \
    URI.py \
    Validator.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
