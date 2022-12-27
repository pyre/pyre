# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import os
import pyre


# declaration
class User(pyre.component):
    """
    Encapsulation of user specific information
    """


    # configurable state
    # administrative
    name = pyre.properties.str()
    name.doc = 'the full name of the user'

    username = pyre.properties.str()
    username.default = os.environ.get('LOGNAME')
    username.doc =  "the username"

    uid = pyre.properties.str()
    uid.default = os.getuid()
    uid.doc = "the user's system id"

    home = pyre.properties.path()
    home.default = os.environ.get('HOME')
    home.doc = "the location of the user's home directory"

    email = pyre.properties.str()
    email.doc = 'the email address of the user'

    affiliation = pyre.properties.str()
    affiliation.doc = 'the affiliation of the user'

    # choices and defaults
    externals = pyre.externals.dependencies()
    externals.doc = 'the database of preferred instances for each external package category'


# end of file
