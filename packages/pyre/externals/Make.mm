# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = externals
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Category.py \
    Library.py \
    MPI.py \
    MPICH.py \
    OpenMPI.py \
    Package.py \
    Python.py \
    Tool.py \
    __init__.py


export:: export-package-python-modules

# end of file 
