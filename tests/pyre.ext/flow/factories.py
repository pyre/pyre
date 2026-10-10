#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that factories made through the catalog bind their slots by name, checked against the
types they compute with, and expose their settings by name
"""


def test():
    # the flow bindings
    from pyre.extensions.pyre import flow

    # get the catalog
    catalog = flow.catalog()
    # find the normalizer that makes values in single precision
    (entry,) = [
        e
        for e in catalog.factories.values()
        if e.className == "Parametric" and catalog.products[e.slots[1].product].cell == "float"
    ]
    # make one
    normalizer = catalog.makeFactory(decl=entry.decl, name="normalizer")
    # it is a factory
    assert isinstance(normalizer, flow.Factory)
    # with the name it was given
    assert normalizer.name == "normalizer"
    # and the slots of its kind
    assert [slot.name for slot in normalizer.slots] == ["signal", "normalized"]

    # make the tiles its slots take
    signal = catalog.makeProduct(decl=entry.slots[0].product, name="signal", shape=(2, 3))
    normalized = catalog.makeProduct(decl=entry.slots[1].product, name="normalized", shape=(2, 3))
    # they are tiles of the right shape
    assert isinstance(signal, flow.Product)
    assert signal.shape == (2, 3)

    # a product of the wrong type binds nothing
    assert not normalizer.bind(slot="signal", product=normalized)
    # nor does a slot it does not have
    assert not normalizer.bind(slot="data", product=signal)
    # the right ones bind
    assert normalizer.bind(slot="signal", product=signal)
    assert normalizer.bind(slot="normalized", product=normalized)
    # and are where they belong
    assert normalizer.inputs["signal"] is signal
    assert normalizer.outputs["normalized"] is normalized

    # its interval
    assert normalizer.get(setting="interval") == (0, 1)
    # changes by name
    assert normalizer.set(setting="interval", value=(0, 10))
    assert normalizer.get(setting="interval") == (0, 10)
    # but not to a value of another type
    assert not normalizer.set(setting="interval", value=3.0)
    # and a setting it does not have has no value
    assert normalizer.get(setting="level") is None

    # take the graph apart
    assert normalizer.unbind(slot="signal")
    assert normalizer.unbind(slot="normalized")
    # leaving nothing bound
    assert normalizer.inputs == {} and normalizer.outputs == {}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
