# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity folders filesystem explorers

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./node.py
	${PYTHON} ./folder.py
	${PYTHON} ./directory_walker.py
	${PYTHON} ./stat_recognizer.py

folders:
	${PYTHON} ./folder_insert.py
	${PYTHON} ./folder_insert_multiple.py
	${PYTHON} ./folder_insert_badNode.py
	${PYTHON} ./folder_find.py
	${PYTHON} ./folder_subscripts.py

filesystem:
	${PYTHON} ./filesystem.py
	${PYTHON} ./filesystem_access.py
	${PYTHON} ./local.py
	${PYTHON} ./local_find.py
	${PYTHON} ./local_rootNonexistent.py
	${PYTHON} ./local_rootNotDirectory.py
	${PYTHON} ./zip.py
	${PYTHON} ./zip_rootNonexistent.py
	${PYTHON} ./zip_rootNotZipfile.py

explorers:
	${PYTHON} ./finder.py
	${PYTHON} ./finder_pattern.py
	${PYTHON} ./simple_explorer.py
	${PYTHON} ./tree_explorer.py



# end of file 
