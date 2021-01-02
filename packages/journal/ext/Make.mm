# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#

# project defaults
include journal.def
# package name
PACKAGE = ext
# the python modules
EXPORT_PYTHON_MODULES = \
    __init__.py

# standard targets
all: export

export:: export-package-python-modules

live: live-package-python-modules

# end of file
