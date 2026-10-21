#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A path accepts whatever the path constructor accepts, iterables of strings and paths included,
and refuses what the constructor refuses, with the constructor's reason; maps are refused, even
though they are iterable
"""


def test() -> None:
    """
    Give a path the values its constructor knows, and some it does not
    """
    # support
    import pyre

    # make a path
    schema = pyre.schemata.path()
    # and get the path factory
    path = pyre.primitives.path

    # the values, and the path each one must become
    accepted = [
        # a tuple of strings
        (("a", "b"), path("a", "b")),
        # a list that starts at the root
        (["/tmp", "a"], path("/tmp", "a")),
        # nested iterables, with a path among them
        (["a", ("b", path("c"))], path("a", "b", "c")),
        # a generator
        ((name for name in ["a", "b"]), path("a", "b")),
        # an empty list, which is the current directory
        ([], path()),
    ]
    # go through them
    for value, expected in accepted:
        # coerce each one
        held = schema.coerce(value=value)
        # it must be a path
        assert isinstance(held, path), f"{value!r}: {held!r}"
        # the expected one
        assert held == expected, f"{value!r}: {held!r}"

    # values the constructor refuses
    for value in [5, [5], ["a", 1.5]]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # with the reason the constructor gave
            assert isinstance(error.error, TypeError), f"{value!r}: {error.error!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # maps, empty or not
    for value in [{"k": "v"}, {"k": None}, {}]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # by the schema, before the constructor sees it
            assert error.error is None, f"{value!r}: {error.error!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
