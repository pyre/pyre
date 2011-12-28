# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre
PACKAGE = filesystem
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    BlockDevice.py \
    CharacterDevice.py \
    Directory.py \
    Explorer.py \
    File.py \
    Filesystem.py \
    Finder.py \
    Folder.py \
    HDF5.py \
    Local.py \
    NamedPipe.py \
    Node.py \
    Recognizer.py \
    SimpleExplorer.py \
    Socket.py \
    Stat.py \
    TreeExplorer.py \
    Walker.py \
    Zip.py \
    exceptions.py \
    metadata.py \
    __init__.py


export:: export-package-python-modules

# end of file 
