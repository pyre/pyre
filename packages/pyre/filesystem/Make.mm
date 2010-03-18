# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    DirectoryWalker.py \
    Explorer.py \
    Folder.py \
    File.py \
    Filesystem.py \
    LocalFilesystem.py \
    NamedPipe.py \
    Node.py \
    Recognizer.py \
    SimpleExplorer.py \
    Socket.py \
    StatRecognizer.py \
    TreeExplorer.py \
    __init__.py


export:: export-package-python-modules

# end of file 
