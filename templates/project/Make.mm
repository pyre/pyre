# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#


PROJECT = {project.name}

RECURSE_DIRS = \
    {project.name} \
    lib \
    extension \
    defaults \
    tests \
    doc \

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#  shortcuts to building in my subdirectories
.PHONY: {project.name} defaults extension lib tests doc

{project.name}:
	(cd {project.name}; $(MM))

defaults:
	(cd defaults; $(MM))

doc:
	(cd doc; $(MM))

extension:
	(cd extension; $(MM))

lib:
	(cd lib; $(MM))

tests:
	(cd tests; $(MM))

build: {project.name} lib extension defaults

test: build tests


# end of file 
