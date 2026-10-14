#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A product becomes an instance when an instance writes it, in whichever order its writer and its
readers become instances: it adopts the product its writer holds, every reader instance is bound
to it, and it goes back to its specification once no instance writes it; undoing a binding takes
the product away from its readers, but its writer keeps what it made, so a product that was made
stays made; a product someone pinned by hand is left alone, and an unbound input holds nothing
"""


def test() -> None:
    """
    Pin a reader and a picker bound through their contents to instances, in both orders
    """
    # support
    import pyre

    # a reader that describes a file with one dataset on no axes
    class Lister(
        pyre.flow.factory, family="tests.pyre.viz.readers.lister", implements=pyre.viz.reader
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
            Describe my file
            """
            # it has one dataset, on no axes
            self.contents.fill(axes={}, entries=[{"selector": {}, "source": self.pyre_name}])
            # chain up
            return super().pyre_run(**kwds)

    # the picker class
    Match = pyre.viz.pickers.match()

    # an unbound input of an instance holds nothing
    assert Match(name="tests.pyre.viz.recipe_instances.loose").contents is None

    # a recipe whose reader and picker are bound through their contents
    recipe = pyre.flow.recipe()
    recipe.factory(name="reader", protocol=pyre.viz.reader, pin=Lister)
    recipe.factory(name="picker", protocol=pyre.viz.picker, pin=Match)
    contents = recipe.product(name="contents", specification=pyre.viz.protocols.contents)
    recipe.bind(factory="reader", slot="contents", product="contents")
    recipe.bind(factory="picker", slot="contents", product="contents")
    # is a specification while its ends are classes
    assert contents.level == "protocol"

    # the picker becomes an instance first
    picker = Match(name="tests.pyre.viz.recipe_instances.picker")
    recipe.pin(name="picker", pin=picker)
    # which reads the contents, so they stay a specification, and the picker holds nothing
    assert contents.level == "protocol"
    assert picker.contents is None
    # so it has nothing to suggest
    assert list(picker.pyre_suggest(trait=picker.pyre_trait(alias="selection"))) == []

    # then the reader
    reader = Lister(name="tests.pyre.viz.recipe_instances.reader")
    # whose contents are its own
    own = reader.contents
    recipe.pin(name="reader", pin=reader)
    # which become the instance of the product
    assert contents.level == "instance"
    assert contents.pin is own
    # that the picker reads
    assert picker.contents is own
    # stale, until someone asks
    assert own.pyre_stale
    # and asking for suggestions pulls them through the reader
    suggestions = list(picker.pyre_suggest(trait=picker.pyre_trait(alias="selection")))
    assert suggestions == [{}], suggestions
    assert not own.pyre_stale

    # the reader goes back to its class
    recipe.pin(name="reader", pin=Lister)
    # so no instance writes the contents, which go back to their specification
    assert contents.level == "protocol"
    # and the picker holds nothing
    assert picker.contents is None
    # while the reader keeps what it made
    assert reader.contents is own and not own.pyre_stale

    # the other order: the reader becomes an instance first
    recipe.pin(name="picker", pin=Match)
    recipe.pin(name="reader", pin=reader)
    # which makes the contents an instance, the product the reader made already
    assert contents.level == "instance"
    assert contents.pin is own and not own.pyre_stale
    # and the picker, when it becomes one
    recipe.pin(name="picker", pin=picker)
    # reads it
    assert picker.contents is contents.pin

    # unbinding the reader
    recipe.unbind(factory="reader", slot="contents")
    # leaves nothing that writes the contents, so they go back to their specification
    assert contents.level == "protocol"
    assert picker.contents is None
    # but the reader keeps what it made, which is still made
    assert reader.contents is own and not own.pyre_stale

    # a product pinned by hand
    mine = pyre.viz.contents.memory()(name="tests.pyre.viz.recipe_instances.mine")
    recipe.pin(name="contents", pin=mine)
    # is the one the reader writes once bound
    recipe.bind(factory="reader", slot="contents", product="contents")
    assert reader.contents is mine
    assert picker.contents is mine
    # and it stays when the reader is no longer an instance
    recipe.pin(name="reader", pin=Lister)
    assert contents.pin is mine
    assert picker.contents is mine

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
