# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access the pyre framework
import pyre


# protocol declaration
class Package(pyre.protocol, family='pyre.externals'):
    """
    The protocol that all external package managers must implement
    """


    # configurable state
    home = pyre.properties.str()
    home.doc = 'the package installation directory'

    requirements = pyre.properties.list(schema=pyre.properties.str())
    requirements.doc = 'the list of package categories on which I depend'


    # constants
    category = None # the common name for this package category


    # exceptions
    from pyre.framework.exceptions import ExternalNotFoundError


    # framewrok support
    @classmethod
    def pyre_default(cls, **kwds):
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
