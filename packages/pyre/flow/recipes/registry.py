# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# my parts
from .Catalogs import Catalogs

# the catalogs other extensions registered, in the order they did
_registered = []


# let an extension contribute its catalog
def register(*, catalog) -> None:
    """
    Add the {catalog} of an extension to the ones recipes are staged against; registering
    the same catalog again changes nothing
    """
    # a catalog that is already known
    if any(known is catalog for known in _registered):
        # is not added twice
        return
    # add it
    _registered.append(catalog)
    # all done
    return


# the catalogs recipes are staged against
def catalogs() -> Catalogs:
    """
    The catalogs recipes are staged against: pyre's own first, when its extension is present,
    followed by the ones other extensions registered, in the order they did
    """
    # start with pyre's own, if its extension was built
    own = [pyre.libpyre.flow.catalog()] if pyre.libpyre is not None else []
    # add the rest and hand them off
    return Catalogs(catalogs=own + _registered)


# end of file
