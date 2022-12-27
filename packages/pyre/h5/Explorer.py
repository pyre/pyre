# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# typing
from .Dataset import Dataset
from .Group import Group
from .Location import Location


# the visitor
class Explorer:
    """
    A visitor that draws the contents of an h5 location
    """

    # interface
    def visit(self, location: Location):
        """
        Draw the tree at {location}
        """
        # easy enough
        yield from location.pyre_identify(authority=self)
        # all done
        return

    # implementation details
    def pyre_onDataset(self, dataset: Dataset, graphic: str = ""):
        """
        Process a {dataset}
        """
        # get the id
        id = dataset.pyre_id
        # the location
        loc = dataset.pyre_location
        # a representation for the value
        val = dataset.string(value=dataset.value)
        # and the shape
        shape = id.shape if id else "unknown"

        # build the label
        yield f"{graphic}{loc} = {val}, shape: {shape if shape else 'scalar'}"
        # all done
        return

    def pyre_onGroup(self, group: Group, graphic: str = ""):
        """
        Process a group
        """
        # use the {group} location as the label
        yield f"{graphic}{group.pyre_location}:"
        # indent
        graphic += "  "
        # go through the {group} children
        for child in group.pyre_locations():
            # and visit each one
            yield from child.pyre_identify(authority=self, graphic=graphic)
        # all done
        return


# end of file
