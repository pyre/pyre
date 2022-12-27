# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
# framework
import merlin


# class declaration
class Category(merlin.component,
                family="merlin.assets.categories.category",
                implements=merlin.protocols.assetCategory):
    """
    The base category for all file based assets
    """


    # constants
    category = "unknown"


    # interface
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a header file
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.category
        # if it doesn't exist
        except AttributeError:
            # this is almost certainly a bug; make a channel
            channel = journal.firewall("merlin.assets.identify")
            # complain
            channel.line(f"unable to find a handler for '{self.pyre_name}'")
            channel.line(f"for the asset category '{self.__class__.__name__}'")
            channel.line(f"while looking through the interface of '{visitor.pyre_name}'")
            # flush
            channel.log()
            # and fail, just in case firewalls aren't fatal
            return None
        # if it does, invoke it
        return handler(**kwds)


# end of file
