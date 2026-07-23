# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access the pyre framework
import pyre


# protocol declaration
class Package(pyre.protocol, family="pyre.externals"):
    """
    The protocol satisfied by all external package categories

    Subclasses declare a package category and publish its known flavors as a sequence of
    recipes; the index realizes recipes by handing them to the package database engines of
    the host and depositing the discoveries into the configuration store
    """

    # configurable state
    version = pyre.properties.str(default="unknown")
    version.doc = "the package version"

    prefix = pyre.properties.path()
    prefix.doc = "the package installation directory"

    # constants
    category = None  # the common name for this package category

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors, in order of preference
        """
        # the base class knows no flavors; subclasses must override
        return ()

    # framework support
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Identify the default installation for this package category
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

        # next, get the host
        host = cls.pyre_host
        # check whether there is a registered preference for this category
        try:
            # if so, we are done
            return host.externals[cls.category]
        # if not
        except (KeyError, AttributeError):
            # moving on
            pass

        # finally, get the index of external packages
        from .Index import Index

        # and ask it to realize one of my recipes
        installation = Index.index().select(protocol=cls)
        # if it succeeded
        if installation is not None:
            # we have our answer
            return installation

        # if we get this far, no one knows what to do
        raise cls.DefaultError(protocol=cls)


# end of file
