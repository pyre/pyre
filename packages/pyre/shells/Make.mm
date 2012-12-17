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
    ANSI.py \
    Application.py \
    Daemon.py \
    Darwin.py \
    Director.py \
    Dumb.py \
    Executive.py \
    Fork.py \
    Host.py \
    Linux.py \
    Platform.py \
    Script.py \
    Shell.py \
    Terminal.py \
    User.py \
    __init__.py


export:: export-package-python-modules

# end of file 
