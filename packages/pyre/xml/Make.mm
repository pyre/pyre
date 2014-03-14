# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = xml
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


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
