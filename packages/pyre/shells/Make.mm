# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# package name
PACKAGE = shells
# the python modules
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
    Plexus.py \
    Renderer.py \
    Repertoir.py \
    Script.py \
    Shell.py \
    Terminal.py \
    User.py \
    VFS.py \
    __init__.py

# standard targets
all: export

export:: export-package-python-modules

live: live-package-python-modules

# end of file
