# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = apache


WWW_SERVER=root@orthologue.com

all: tidy

deploy:
	ssh $(WWW_SERVER) 'service apache2 restart'


# end of file 
