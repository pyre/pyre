# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
include mpi.def
# package name
PACKAGE = mpi
# the python modules
EXPORT_PYTHON_MODULES = \
    Cartesian.py \
    Communicator.py \
    Group.py \
    Launcher.py \
    Object.py \
    Port.py \
    Slurm.py \
    TrivialCommunicator.py \
    __init__.py

# standard targets
all: export

export:: export-python-modules

live: live-python-modules

# end of file
