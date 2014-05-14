# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

PROJECT = pyre
PACKAGE = shells
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    ANSI.py \
    Application.py \
    Daemon.py \
    Director.py \
    Executive.py \
    Fork.py \
    Plain.py \
    Plexus.py \
    Renderer.py \
    Script.py \
    Shell.py \
    Terminal.py \
    User.py \
    __init__.py


export:: export-package-python-modules

# end of file 
