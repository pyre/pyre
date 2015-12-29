# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os, glob
# access the pyre framework
import pyre


# protocol declaration
class Package(pyre.protocol, family='pyre.externals'):
    """
    The protocol that all external package managers must implement
    """


    # configurable state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    # constants
    category = None # the common name for this package category

    # exceptions
    from pyre.framework.exceptions import ExternalNotFoundError


    # framework support
    @classmethod
    def pyre_default(cls, channel=None, **kwds):
        """
        Identify the default implementation of a package
        """
        # get the user
        user = cls.pyre_user
        # check whether there is a registered preference for this category
        try:
            # if so, we are done
            return user.externals[cls.category]
        # if not
        except (KeyError, AttributeError):
            # moving on
            pass

        # get the package manager
        packager = cls.pyre_externals
        # go through my host specific choices
        for package in packager.choices(category=cls):
            # i only care about the first one
            return package

        # if i get this far, no one knows what to do
        return


# end of file
