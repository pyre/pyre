# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access the framework
import pyre
# my protocol and the trait descriptor for external dependencies
from . import category, requirements


# the base class for package managers
class Package(pyre.component, implements=category):
    """
    The base class for all package managers
    """


    # configurable state
    requirements = requirements()
    requirements.doc = 'the list of package categories on which I depend'

    home = pyre.properties.str()
    home.doc = 'the package installation directory'

    # public data
    category = None # overridden by subclasses


    # package factories
    @classmethod
    def pyre_select(cls):
        """
        Select the default package manager for this package and ask for a package instance
        """
        # easy enough
        return cls.pyre_package()


    @classmethod
    def pyre_package(cls):
        """
        Build a package instance
        """
        # get the user
        user = cls.pyre_user
        # has the user chosen one?
        chosen = user.externals.get(cls.category)
        # if yes, we are done
        if chosen: return chosen

        # get the host
        host = cls.pyre_host
        # are there any available packages?
        available = host.externals.get(cls.category, [])
        # if yes, grab the first one and return it
        if available: return available[0]

        # otherwise, instantiate using a name derived from my category and the platform name
        return cls(name="{}-{}-default".format(cls.category, host.distribution))


# end of file 
