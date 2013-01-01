# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#

PROJECT = pyre
PACKAGE = xml
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    AttributeDescriptor.py \
    DTD.py \
    Descriptor.py \
    Document.py \
    ElementDescriptor.py \
    Ignorable.py \
    Node.py \
    Reader.py \
    exceptions.py \
    __init__.py


export:: export-package-python-modules

# end of file 
