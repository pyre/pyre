# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    Action.py \
    Application.py \
    Command.py \
    Daemon.py \
    Director.py \
    Executive.py \
    Fork.py \
    Layout.py \
    Panel.py \
    Plain.py \
    Plector.py \
    Plexus.py \
    Renderer.py \
    Repertoir.py \
    Script.py \
    Shell.py \
    Terminal.py \
    User.py \
    VFS.py \
    __init__.py


export:: export-package-python-modules

# end of file
