# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os
import merlin


# declaration
class User(merlin.component, family='pyre.user'):
    """
    Encapsulation of user specific information
    """


    # public data
    name = merlin.properties.str()
    email = merlin.properties.str()
    affiliation = merlin.properties.str()

    uid = os.getuid()
    home = os.environ['HOME']
    username = os.environ['LOGNAME']


# end of file 
