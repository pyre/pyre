# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
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

    # public data
    category = None # overridden by subclasses


    # package factories
    @classmethod
    def package(cls, chosen, platform):
        """
        Build a package instance
        """
        # if there is a request for a specific one
        if chosen is not None:
            # build it and return it
            return cls(name=chosen)

        # if the platform is not known
        if platform is None:
            # get the platform protocol
            from ..platforms import platform as recognizer
            # and ask it to figure what kind of machine we are running on
            platform = recognizer().classDefault()

        # instantiate using a name derived from my category and the platform name
        package = cls(name="{}-{}-default".format(cls.category, platform.distribution))

        # get the default for this platform
        return cls.configureDefaultPackage(package=package, platform=platform)


    @classmethod
    def configureDefaultPackage(cls, package, platform):
        """
        Configure the default package on this {platform}
        """
        # don't know any better...
        return package


# end of file 
