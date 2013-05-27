# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#

PROJECT = pyre
PACKAGE = platforms
PROJ_CLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


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
