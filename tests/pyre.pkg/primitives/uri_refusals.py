#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the parser says why it refuses text that is not a uri: empty text, text that holds a
control character, and text that starts with an ampersand each get their own reason
"""


def test() -> None:
    """
    Parse text the parser refuses, and check the reason it gives for each
    """
    # the home of the parser
    from pyre.primitives import uri

    # the text the parser refuses, and the reason it should give
    cases = (
        ("", "'' is not a uri: it is empty"),
        ("/tmp/a\nb", "'/tmp/a\\nb' is not a uri: it holds a control character"),
        ("&x=1", "'&x=1' is not a uri: it starts with '&'"),
    )
    # go through them
    for text, reason in cases:
        # attempt to
        try:
            # parse the text
            uri.parse(text)
            # which should be unreachable
            assert False, text
        # if it is refused, as expected
        except uri.ParsingError as error:
            # the reason it gives, the way it reads
            given = error.description.format(error)
            # must be the one for this text
            assert given == reason, (text, given)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
