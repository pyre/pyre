# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
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

        # if i get this far...
        return cls.generic()


    # configuration validation
    @classmethod
    def checkFolder(cls, category, folder, filenames):
        """
        Verify that the folder exists and contains the given {filenames}
        """
        # check there is a value
        if not folder:
            # complain
            yield "no {!r} setting".format(category)
            # and stop
            return
        # check that it is a valid directory
        if not os.path.isdir(folder):
            # complain
            yield "{!r} is not a valid directory".format(folder)
            # and stop
            return
        # verify that the given list of filenames exist
        for filename in filenames:
            # form the path
            path = os.path.join(folder, filename)
            # check
            if not os.path.exists(path):
                # complain
                yield "couldn't locate {!r} in {}".format(filename, folder)
                # and stop
                return
        # all done
        return


# end of file
