# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# access the project defaults
include pyre.def
# the package name
PACKAGE = nexus
# python packages
EXPORT_PYTHON_MODULES = \
    Nexus.py \
    Node.py \
    Server.py \
    Service.py \
    exceptions.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

live: live-package-python-modules

# end of file
