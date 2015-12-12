# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# package name
PACKAGE = platforms
# the python modules
EXPORT_PYTHON_MODULES = \
    CentOS.py \
    Darwin.py \
    Debian.py \
    Host.py \
    Linux.py \
    MacPorts.py \
    POSIX.py \
    Platform.py \
    RedHat.py \
    Ubuntu.py \
    __init__.py

# standard targets
all: export

export:: export-package-python-modules

live: live-package-python-modules

# end of file
