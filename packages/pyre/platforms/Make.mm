# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = platforms
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    CentOS.py \
    Darwin.py \
    Host.py \
    Linux.py \
    MacPorts.py \
    POSIX.py \
    Platform.py \
    RedHat.py \
    Ubuntu.py \
    __init__.py


export:: export-package-python-modules

# end of file 
