#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A plain symbol table stores named nodes, replaces them, and reports what it did
"""


def test() -> None:
    """
    Insert, replace and evaluate nodes in a plain symbol table
    """
    # support
    import pyre.calc.SymbolTable

    # make a symbol table
    table = pyre.calc.SymbolTable.SymbolTable()

    # make a node
    first = table.variable(value=1)
    # insert it under a new name
    name, new, old = table.insert(name="a", node=first)
    # the table reports the name, the node it stored, and that there was none before it
    assert (name, new, old) == ("a", first, None)
    # and the value is there
    assert table["a"] == 1

    # an expression that refers to it
    table.insert(name="b", node=table.expression(value="{a} + 1"))
    # follows its value
    assert table["b"] == 2
    # and so does an interpolation, which is what assigning text makes
    table["c"] = "a is {a}"
    # with the text of the value
    assert table["c"] == "a is 1"

    # make another node
    second = table.variable(value=5)
    # and insert it under the same name
    name, new, old = table.insert(name="a", node=second)
    # the table reports the new node and the one it replaced
    assert name == "a" and new is second and old is first
    # the name now holds the new value
    assert table["a"] == 5
    # and the expression follows it
    assert table["b"] == 6
    # as does the interpolation
    assert table["c"] == "a is 5"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
