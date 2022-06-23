#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


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
        # prime the workload
        todo = [(location, prefix)]

        # now go through it
        for entry, path in todo:
            # return the current entry
            yield entry, path
            # compute the new path
            newPath = path / entry.pyre_location
            # and add its children to the pile
            todo.extend((child, newPath) for child in entry.pyre_locations())

        # all done
        return


    def depth(self, location, prefix=pyre.primitives.path.root):
        """
        Perform a depth-first traversal of {location}
        """
        # first up, the {location} itself
        yield location, prefix

        # compute the new path
        prefix = prefix / location.pyre_location

        # grab the {location} contents
        for child in location.pyre_locations():
            # and explore each one
            yield from self.depth(location=child, prefix=prefix)

        # all done
        return


# end of file
