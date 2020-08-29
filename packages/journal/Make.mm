# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2020 all rights reserved
#

# project defaults
include journal.def
# the name of the package
PACKAGE = journal
# add this to the clean pile
PROJ_CLEAN += $(EXPORT_MODULEDIR)
# my subfolders
RECURSE_DIRS = \
    ext

# the python modules
EXPORT_PYTHON_MODULES = \
    ANSI.py \
    ANSI_x11.py \
    ASCII.py \
    Alert.py \
    CSI.py \
    Channel.py \
    Chronicler.py \
    Console.py \
    Debug.py \
    Device.py \
    Entry.py \
    Error.py \
    ErrorConsole.py \
    File.py \
    Firewall.py \
    Index.py \
    Informational.py \
    Inventory.py \
    Memo.py \
    Null.py \
    Renderer.py \
    Splitter.py \
    Stream.py \
    Tee.py \
    Trash.py \
    Warning.py \
    exceptions.py \
    meta.py \
    palettes.py \
    __init__.py


# standard targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: meta.py export-python-modules
	BLD_ACTION="export" $(MM) recurse
	@$(RM) meta.py

live: live-python-modules
	BLD_ACTION="live" $(MM) recurse

revision: meta.py export-python-modules
	@$(RM) meta.py

# construct my {meta.py}
meta.py: meta.py.in Make.mm
	@sed \
          -e "s:@MAJOR@:$(PROJECT_MAJOR):g" \
          -e "s:@MINOR@:$(PROJECT_MINOR):g" \
          -e "s:@MICRO@:$(PROJECT_MICRO):g" \
          -e "s:@REVISION@:$(REVISION):g" \
          -e "s|@TODAY@|$(TODAY)|g" \
          meta.py.in > meta.py

# shortcuts for building specific subdirectories
.PHONY: $(RECURSE_DIRS)

$(RECURSE_DIRS):
	(cd $@; $(MM))


# end of file
