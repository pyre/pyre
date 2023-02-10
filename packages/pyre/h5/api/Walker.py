# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# typing
from . import api


# structure traversal of h5 locations
class Walker:
    """
    A visitor of the hierarchical structure of an h5 {location}
    """

    # interface
    def breadth(self, location: api.location):
        """
        Perform a breadth-first traversal of {location}
        """
        # prime the work pile
        todo = [location]
        # now go through it
        for location in todo:
            # return the current entry
            yield location
            # and add its children to the work pile
            todo.extend(location._pyre_locations())

        # all done
        return

    def depth(self, location: api.location):
        """
        Perform a depth-first traversal of {location}
        """
        # first up, the {location} itself
        yield location
        # followed by the {location} contents
        yield from location._pyre_locations()
        # all done
        return


# end of file
