# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# class declaration
class Externals:
    """
    The database of external packages, tools and libraries that are available to pyre
    applications
    """

    # types
    from .exceptions import ExternalNotFoundError


    # public data
    packages = None # map of package names to their managers


    # interface
    def locate(self, category, platform=None, chosen=None):
        """
        Locate a package from the given {category} suitable for {platform} subject to the
        {user} choices
        """
        # first, check whether we know the category already
        try:
            # get it
            manager = self.packages[category]
        # if not
        except KeyError:
            # access the locator factory
            from .. import tracking
            # build a locator
            locator = tracking.simple('while looking for external package {!r}'.format(category))
            # ask the protocol
            from ..externals.Category import Category
            # for package managers for this category
            for manager in Category().resolve(value=category, locator=locator):
                # register the manager
                self.packages[manager.category] = manager
                # we only care about the first one, so bail out
                break
            # if the category could not be resolved
            else:
                # let the user know
                raise self.ExternalNotFoundError(category=category) from None

        # otherwise, ask the package manager to build one
        return manager.package(chosen=chosen, platform=platform)


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize my categories
        self.packages = dict()
        # all done
        return


# end of file 
