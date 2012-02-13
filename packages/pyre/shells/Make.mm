# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

PROJECT = pyre
PACKAGE = shells
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    Application.py \
    Daemon.py \
    Director.py \
    Executive.py \
    Fork.py \
    Host.py \
    Script.py \
    Shell.py \
    User.py \
    __init__.py


export:: export-package-python-modules

# end of file 
