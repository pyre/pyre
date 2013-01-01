# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = apache


WWW_SERVER=root@pyre.caltech.edu
WWW_CONFIG=/etc/apache2/sites-available


all: tidy

install:
	scp pyre $(WWW_SERVER):$(WWW_HOME)

deploy:
	ssh $(WWW_SERVER) 'service apache2 restart'


# end of file 
