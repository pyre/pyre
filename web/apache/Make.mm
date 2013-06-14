# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = apache


WWW_SERVER=root@orthologue.com

all: tidy

deploy:
	ssh $(WWW_SERVER) 'service apache2 restart'


# end of file 
