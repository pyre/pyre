# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    lib \
    packages \
    extensions \
    defaults \
    bin \
    templates \
    schema \
    tests \
    examples \
    web \
    bot \
    people \

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
.PHONY: bin defaults doc examples extensions lib packages schema tests web

bin:
	(cd bin; $(MM))

defaults:
	(cd defaults; $(MM))

doc:
	(cd doc; $(MM))

examples:
	(cd examples; $(MM))

extensions:
	(cd extensions; $(MM))

lib:
	(cd lib; $(MM))

packages:
	(cd packages; $(MM))

schema:
	(cd schema; $(MM))

tests:
	(cd tests; $(MM))

web:
	(cd web; $(MM))

build: lib packages extensions defaults bin

test: build tests examples


#--------------------------------------------------------------------------
#
PYRE_ZIP = $(EXPORT_ROOT)/pyre-1.0.zip

zip: build zipit

zipit:
	$(RM_F) $(PYRE_ZIP)
	(cd $(EXPORT_ROOT); zip -r ${PYRE_ZIP} * )


# end of file 
