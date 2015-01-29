# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# access the project defaults
include pyre.def
# the package name
PACKAGE = nexus/http
# python packages
EXPORT_PYTHON_MODULES = \
    Request.py \
    Response.py \
    Server.py \
    exceptions.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

live: live-package-python-modules

# end of file
