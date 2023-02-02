# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal

# a visitor of schemata
class Explorer:
    """
    A visitor that draws the structure of a schema
    """

    # interface
    def explore(self, descriptor, margin="", graphic=""):
        # start things off
        yield self.render(descriptor=descriptor, graphic=graphic)

        # grab the {location} contents
        children = tuple(descriptor._pyre_descriptors.values())
        # if {location} doesn't have any
        if not children:
            # nothing further to do
            return

        # set up the decorations for all but the last child
        bodyMargin = margin + "|  "
        bodyGraphic = margin + "+- "
        # go through all but the last child
        for child in children[:-1]:
            # and explore each one
            yield from self.explore(
                descriptor=child, margin=bodyMargin, graphic=bodyGraphic
            )

        # the last child gets decorated slightly differently
        lastMargin = margin + "   "
        lastGraphic = margin + "`- "
        # repeat for the last child
        yield from self.explore(
            descriptor=children[-1], margin=lastMargin, graphic=lastGraphic
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
        channel.report(self.explore(descriptor=descriptor))
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

    # implementation details
    def render(self, descriptor, graphic=""):
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
