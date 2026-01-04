# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import journal

# typing
from .Datatype import Datatype
from .Dataset import Dataset
from .Group import Group
from .Location import Location


# the visitor
class Viewer:
    """
    A visitor that draws the contents of an h5 location
    """

    # interface
    def visit(self, location: Location):
        """
        Draw the tree at {location}
        """
        # easy enough
        yield from location._pyre_identify(authority=self)
        # all done
        return

    # implementation details
    def _pyre_onDataset(self, dataset: Dataset, graphic: str = ""):
        """
        Process a {dataset}
        """
        # the schema
        layout = dataset._pyre_layout
        # the type
        typename = layout.type
        # and the location
        loc = dataset._pyre_location.name
        # attempt to
        try:
            # get the value
            value = dataset.value
        # if something goes wrong
        except journal.ApplicationError as error:
            # make a channel
            channel = journal.warning("pyre.h5.api.viewer")
            # report
            channel.log(f"unable to read the value of '{dataset._pyre_location}'")
            # and bail
            return
        # build a representation for the value
        rep = layout.string(value=value)
        # assemble the label
        yield f"{graphic}{loc} = {rep} ({typename})"
        # all done
        return

    def _pyre_onGroup(self, group: Group, graphic: str = ""):
        """
        Process a group
        """
        # use the {group} location as the label
        yield f"{graphic}{group._pyre_location.name}:"
        # indent
        graphic += "  "
        # go through the {group} children
        for location in group._pyre_locations():
            # and visit each one
            yield from location._pyre_identify(authority=self, graphic=graphic)
        # all done
        return

    def _pyre_onDatatype(self, datatype: Datatype, graphic: str = ""):
        """
        Process a datatype
        """
        # and the location
        loc = datatype._pyre_location.name
        # assemble the label
        yield f"{graphic}{loc}: datatype declaration"
        # all done
        return


# end of file
