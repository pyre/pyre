# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
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
    def locate(self, category):
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
            # for the trait descriptor
            facility = Category()

            # attempt to
            try:
                # get the package manager for this category
                manager = facility.coerce(value=category, locator=locator)
            # if one could not be located
            except facility.CastingError:
                # complain
                raise self.ExternalNotFoundError(category=category) from None
            # otherwise
            else:
                # register it
                self.packages[manager.category] = manager

        # otherwise, ask the package manager to build one
        return manager.pyre_select()


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize my categories
        self.packages = dict()
        # all done
        return


# end of file 
