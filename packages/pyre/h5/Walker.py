#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre


# structure traversal of h5 locations
class Walker:
    """
    A visitor of the hierarchical structure of an h5 {location}
    """


    # interface
    def breadth(self, location, prefix=pyre.primitives.path.root):
        """
        Perform a breadth-first traversal of {location}
        """
        # prime the work pile
        todo = [(prefix, None, location)]

        # now go through it
        for prefix, parent, location in todo:
            # return the current entry
            yield prefix, parent, location
            # compute the new path
            prefix = prefix / location.pyre_location
            # and add its children to the work pile
            todo.extend((prefix, location, child) for child in location.pyre_locations())

        # all done
        return


    def depth(self, location, parent=None, prefix=pyre.primitives.path.root):
        """
        Perform a depth-first traversal of {location}
        """
        # first up, the {location} itself
        yield prefix, parent, location

        # compute the new path
        prefix = prefix / location.pyre_location

        # grab the {location} contents
        for child in location.pyre_locations():
            # and explore each one
            yield from self.depth(location=child, parent=location, prefix=prefix)

        # all done
        return


# end of file
