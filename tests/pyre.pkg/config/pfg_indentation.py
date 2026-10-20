#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The pfg codec reports bad indentation as a decoding error that says where it is, rather than
letting the parser crash
"""


def test() -> None:
    """
    Decode pfg text with bad indentation, and check what is raised
    """
    # support
    import io
    import journal
    import pyre
    from pyre.config.exceptions import DecodingError

    # get the codec
    codec = pyre.executive.configurator.codec(encoding="pfg")
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.config.pfg")

    # the texts, and the line where each goes wrong
    cases = [
        # an assignment indented deeper than its siblings, with no section above it
        ("a:\n  b = 1\n    c = 2\n", 3),
        # a dedent to a level that matches no open block
        ("a:\n    b = 1\n  c = 2\n", 3),
    ]
    # go through them
    for text, line in cases:
        # carefully
        try:
            # decode the text
            codec.decode(uri="pfg_indentation.pfg", source=io.StringIO(text), locator=None)
        # it must be refused
        except DecodingError as error:
            # by an error that says where
            if f"line={line}" not in str(error):
                # if not, say so
                channel.line(f"the error for {text!r} does not point to line {line}")
                # and the details
                channel.indent()
                channel.line(f"error: {error}")
                channel.outdent()
        # if it is accepted
        else:
            # say so
            channel.line(f"decoding {text!r} succeeded")

    # if anything went wrong
    if channel.page:
        # complain
        channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
