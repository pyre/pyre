# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


class Tree:
    """
    A visitor that draws the structure of {location} instances
    """

    # interface
    def explore(self, location, margin="", graphic=""):
        # start things off
        yield self.render(location=location, graphic=graphic)

        # grab the {location} contents
        children = tuple(location.pyre_locations())
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
                location=child, margin=bodyMargin, graphic=bodyGraphic
            )

        # the last child gets decorated slightly differently
        lastMargin = margin + "   "
        lastGraphic = margin + "`- "
        # repeat for the last child
        yield from self.explore(
            location=children[-1], margin=lastMargin, graphic=lastGraphic
        )

        # all done
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
    def render(self, location, graphic=""):
        # unpack my state
        indent = self.indent
        # and the {location} information
        label = location.pyre_location
        marker = location.pyre_marker
        # build a string and return it
        return f"{indent}{graphic}{label} ({marker})"

    # constant
    INDENT = " " * 2


# end of file
