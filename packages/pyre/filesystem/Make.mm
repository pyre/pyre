# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = filesystem
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)


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
    Naked.py \
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
