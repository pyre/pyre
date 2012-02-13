# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os
import pyre


# declaration
class User(pyre.component, family='pyre.user'):
    """
    Encapsulation of user specific information
    """


    # public data
    name = pyre.properties.str()
    email = pyre.properties.str()
    affiliation = pyre.properties.str()

    uid = os.getuid()
    home = os.environ.get('HOME')
    username = os.environ.get('LOGNAME')


# end of file 
