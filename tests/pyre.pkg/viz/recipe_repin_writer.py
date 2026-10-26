#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that pinning the writer of a product to another instance leaves the old one out of the
flow: making the product downstream runs only the instance that writes it now, even when the
old one is kept alive by its name
"""


def test() -> None:
    """
    Pin a reader to one instance and then to another, and make the dataset a picker reads from it
    """
    # support
    import pyre

    # the names of the readers that described their file, in the order they ran
    runs = []

    # a reader that describes a file with one dataset on no axes, and records that it ran
    class Lister(
        pyre.flow.factory, family="tests.pyre.viz.readers.repin", implements=pyre.viz.reader
    ):
        """
        A reader whose file holds one dataset
        """

        # user configurable state
        uri = pyre.properties.uri()

        # the output
        contents = pyre.viz.protocols.contents.output()

        # flow hooks
        def pyre_run(self, **kwds):
            """
            Describe my file, and record that i did
            """
            # record the run
            runs.append(self.pyre_name)
            # the file has one dataset, on no axes
            self.contents.fill(axes={}, entries=[{"selector": {}, "source": self.pyre_name}])
            # chain up
            return super().pyre_run(**kwds)

    # a recipe
    recipe = pyre.flow.recipe()
    # with a reader
    recipe.factory(name="reader", protocol=pyre.viz.reader, pin=Lister)
    # and a picker
    recipe.factory(name="picker", protocol=pyre.viz.picker, pin=pyre.viz.pickers.match())
    # and the contents that pass between them
    recipe.product(name="contents", specification=pyre.viz.protocols.contents)
    # written by the reader
    recipe.bind(factory="reader", slot="contents", product="contents")
    # and read by the picker
    recipe.bind(factory="picker", slot="contents", product="contents")

    # the first reader, which its name keeps alive in the configuration store
    first = Lister(name="tests.pyre.viz.recipe_repin_writer.first")
    # is pinned in place
    recipe.pin(name="reader", pin=first)
    # and then replaced by a second one
    second = Lister(name="tests.pyre.viz.recipe_repin_writer.second")
    # pinned in the same place
    recipe.pin(name="reader", pin=second)
    # the first holds nothing any more
    assert first.contents is None
    # and the contents are written by the second alone
    assert set(recipe.node(name="contents").pin.pyre_factories) == {second}

    # the picker, as an instance
    picker = pyre.viz.pickers.match()(name="tests.pyre.viz.recipe_repin_writer.picker")
    # pinned in place
    recipe.pin(name="picker", pin=picker)
    # making its dataset
    picker.pyre_make()
    # runs the second reader only
    assert runs == [second.pyre_name], runs
    # and picks its dataset
    assert picker.dataset.source == second.pyre_name, picker.dataset.source

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
