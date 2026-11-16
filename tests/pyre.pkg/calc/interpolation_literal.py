#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a pair of braces with nothing between them stands for itself, and that escaped text
interpolates back to what it was
"""


def test():
    # support
    import pyre.calc

    # build a model
    model = pyre.calc.model()

    # an empty pair of braces names no node
    node = model.interpolation("{}")
    # so the text is a plain variable
    assert type(node) is model.node.variable
    # that holds it
    assert node.value == "{}"
    # wherever it appears
    assert model.interpolation("a {} b").value == "a {} b"

    # a node to refer to
    model["production"] = 80
    # an empty pair next to a reference
    node = model.interpolation("{production} {}")
    # leaves the reference alone
    assert type(node) is model.node.interpolation
    # and stands for itself
    assert node.value == "80 {}"

    # text that holds braces of every kind
    for text in ("{production}", "{}", "}{", "{{", "a{b}c{{d}}", "{'band': 'L'}"):
        # once escaped
        escaped = model.node.interpolation.escape(text)
        # interpolates back to itself
        assert model.interpolation(escaped).value == text, text

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
