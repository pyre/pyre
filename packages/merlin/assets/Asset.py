# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import journal
import merlin
# superclass
from .Product import Product


# class declaration
class Asset(Product):
    """
    Encapsulation of a project asset
    """


    # required configurable state
    ignore = merlin.properties.bool(default=False)
    ignore.doc = "controls whether to ignore this asset"

    private = merlin.properties.bool(default=False)
    private.doc = "mark this asset as private"


    # builder requirements
    def build(self, **kwds):
        """
        Refresh this asset
        """
        # delegate to my flow interface
        return self.pyre_make(**kwds)


    # merlin hooks
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process a generic asset
        """
        # attempt to
        try:
            # ask authority for a handler for my type
            handler = authority.asset
        # if it doesn't exist
        except AttributeError:
            # this is almost certainly a bug; make a channel
            channel = journal.firewall("merlin.assets.identify")
            # complain
            channel.line(f"unable to find a handler for '{self.pyre_name}'")
            channel.line(f"an asset of type '{self.__class__.__name__}'")
            channel.line(f"while looking through the interface of '{authority.pyre_name}'")
            # flush
            channel.log()
            # and fail, just in case firewalls aren't fatal
            return None
        # if it does, invoke it
        return handler(asset=self, **kwds)


# end of file
