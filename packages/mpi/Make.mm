# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

PROJECT = mpi
PACKAGE = mpi
PROJ_CLEAN = $(EXPORT_MODULEDIR)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Cartesian.py \
    Communicator.py \
    Group.py \
    Launcher.py \
    Object.py \
    Port.py \
    TrivialCommunicator.py \
    __init__.py


export:: export-python-modules

# end of file
