#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the description of an error renders without fail: the fields that refer to the error
are resolved, and everything else, e.g. the braces of text that was never meant to be a template,
appears as it was written
"""


def test():
    # support
    import pyre
    from pyre.framework.exceptions import PyreError

    # an error with some context
    class Error(PyreError):
        """
        An error that carries a value, a width and a table
        """

        # meta-methods
        def __init__(self, value="L", width=4, table=None, **kwds):
            # chain up
            super().__init__(**kwds)
            # store the context
            self.value = value
            self.width = width
            self.table = {"band": "S"} if table is None else table
            # all done
            return

    # templates
    for description, expected in [
        # a reference to an attribute
        ("value {0.value}", "value L"),
        # with the position left implied
        ("value {.value}", "value L"),
        # with a conversion
        ("value {0.value!r}", "value 'L'"),
        # an item
        ("band {0.table[band]}", "band S"),
        # with a format specification
        ("[{0.value:>4}]", "[   L]"),
        # whose own fields refer to the error
        ("[{0.value:>{0.width}}]", "[   L]"),
        # the representation of the error itself
        ("{0!r}", repr(Error(description="x"))),
        # and escaped braces
        ("{{0.value}} is {0.value}", "{0.value} is L"),
    ]:
        # render as templates
        assert str(Error(description=description)) == expected, description

    # text that happens to hold braces
    for text in [
        # an empty pair, which would refer to the error itself, and render it again
        "no dataset matches {}",
        # the same, by position
        "no dataset matches {0}",
        # and as a string
        "no dataset matches {0!s}",
        # the rendering of a dictionary
        "no dataset matches {'band': 'L', 'frequency': 'A'}",
        # an empty dictionary
        "no dataset matches the selector {}",
        # a named field
        "unresolved {name}",
        # another position
        "position {1}",
        # an attribute the error does not have
        "missing {0.nothing}",
        # an item it does not have
        "missing {0.table[nothing]}",
        # a format specification that does not apply
        "bad {0.width:q}",
        # lone braces
        "a lone } brace",
        "a lone { brace",
    ]:
        # renders as it was written
        assert str(Error(description=text)) == text, text

    # the text of an error with braces, wrapped by another
    wrapped = PyreError(description=str(KeyError({"band": "L"})))
    # renders as the text of the original
    assert str(wrapped) == str(KeyError({"band": "L"}))

    # a locator
    locator = pyre.tracking.simple("the test")
    # leads the description
    assert str(Error(description="{0.value} {}", locator=locator)) == f"{locator}: L {{}}"

    # the casting errors of the schemata, whose templates come from the schema
    try:
        # convert something that is not an integer
        pyre.schemata.int().coerce(value="no")
        # must fail
        assert False, "'no' was converted into an integer"
    # with a casting error
    except pyre.schemata.int.CastingError as error:
        # that renders its template
        assert str(error) == "could not coerce 'no' into an integer", str(error)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
