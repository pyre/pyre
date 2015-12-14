# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# class declaration
class Externals:
    """
    The database of external packages, tools and libraries that are available to pyre
    applications
    """

    # types
    from .exceptions import ExternalNotFoundError


    # interface
    def locate(self, category):
        """
        Locate a package from the given {category} suitable for {platform} subject to the
        {user} choices
        """
        # build the trait descriptor and ask it find us an instance
        return category.pyre_default()


# end of file
