# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal

# typing
from .Descriptor import Descriptor
from .Dataset import Dataset
from .Group import Group


# a visitor of schemata
class Viewer:
    """
    A visitor that draws the structure of a schema
    """

    # interface
    def visit(self, descriptor: Descriptor, margin: str = "", graphic: str = ""):
        """
        Generate a textual representation of the {descriptor} contents
        """
        # delegate to the correct handler
        yield from descriptor._pyre_identify(
            authority=self, margin=margin, graphic=graphic
        )
        # all done
        return

    def info(self, descriptor):
        """
        Render a representation of {descriptor}
        """
        # make a channel
        channel = journal.info("pyre.h5.schema")
        # generate the report
        channel.report(self.visit(descriptor=descriptor))
        # flush
        channel.log()
        # and done
        return

    # metamethods
    def __init__(self, indent=0, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my state
        self.indent = self.INDENT * indent
        # all done
        return

    # visitor implementation
    def _pyre_onDataset(self, dataset: Dataset, graphic: str, **kwds):
        """
        Process a {dataset}
        """
        # draw
        yield self._render(descriptor=dataset, graphic=graphic)
        # all done
        return

    def _pyre_onGroup(self, group: Group, margin: str, graphic: str):
        """
        Process a {group}
        """
        # draw
        yield self._render(descriptor=group, graphic=graphic)
        # collect the children
        children = tuple(group._pyre_descriptors())
        # if there aren't any
        if not children:
            # nothing to do
            return
        # set up the decorations for all but the last child
        bodyMargin = margin + "|  "
        bodyGraphic = margin + "+- "
        # go through all but the last child
        for child in children[:-1]:
            # and visit each one
            yield from self.visit(
                descriptor=child, margin=bodyMargin, graphic=bodyGraphic
            )
        # the last child gets decorated slightly differently
        lastMargin = margin + "   "
        lastGraphic = margin + "`- "
        # repeat for the last child
        yield from self.visit(
            descriptor=children[-1], margin=lastMargin, graphic=lastGraphic
        )
        # all done
        return

    # implementation details
    def _render(self, descriptor, graphic):
        # unpack my state
        indent = self.indent
        # and the {descriptor} information
        label = descriptor._pyre_name
        marker = descriptor._pyre_marker()
        # build a string and return it
        return f"{indent}{graphic}{label} ({marker})"

    # constant
    INDENT = " " * 2


# end of file
