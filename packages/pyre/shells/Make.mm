# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#

# project defaults
include pyre.def
# package name
PACKAGE = shells
# the python modules
EXPORT_PYTHON_MODULES = \
    ASCII.py \
    ANSI.py \
    Action.py \
    Application.py \
    CSI.py \
    Command.py \
    Daemon.py \
    Director.py \
    Executive.py \
    Fork.py \
    Interactive.py \
    IPython.py \
    Layout.py \
    Panel.py \
    Plain.py \
    Plexus.py \
    Repertoir.py \
    Script.py \
    Shell.py \
    Terminal.py \
    User.py \
    Web.py \
    __init__.py

# standard targets
all: export

export:: export-package-python-modules

live: live-package-python-modules

# end of file
