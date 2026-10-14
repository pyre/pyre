#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a component hears about changes to its dict traits, whether the whole table is
assigned or one of its keys is set or removed
"""


def test() -> None:
    """
    Change the table of a component in every way and count the notifications
    """
    # support
    import pyre

    # a component that records the traits it is told have changed
    class Reader(pyre.component, family="pyre.tests.dict.notify.reader"):
        """
        A component with a dict trait that listens for changes
        """

        # a table of strings
        selection = pyre.properties.kv()

        # the hook
        def pyre_traitModified(self, trait, new, old):
            """
            Record the name of the trait that changed, and the value of its table
            """
            # record
            self.heard.append((trait.name, dict(new.value)))
            # and chain up
            return super().pyre_traitModified(trait=trait, new=new, old=old)

        # meta-methods
        def __init__(self, **kwds):
            # chain up
            super().__init__(**kwds)
            # the changes i heard about
            self.heard = []
            # all done
            return

    # make a reader
    reader = Reader(name="reader")
    # assign a whole table
    reader.selection = {"band": "L"}
    # set a key
    reader.selection["frequency"] = "A"
    # and remove one
    del reader.selection["band"]
    # every change was heard, with the table as it was after it
    assert reader.heard == [
        ("selection", {"band": "L"}),
        ("selection", {"band": "L", "frequency": "A"}),
        ("selection", {"frequency": "A"}),
    ], reader.heard

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
