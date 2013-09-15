# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = config/pml
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Bind.py \
    Component.py \
    Configuration.py \
    Document.py \
    Node.py \
    PML.py \
    Package.py \
    __init__.py


export:: export-package-python-modules

# end of file 
