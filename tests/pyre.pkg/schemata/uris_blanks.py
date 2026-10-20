#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The uri schema keeps the blanks inside its text, so addresses name the files they were typed
with, and refuses text that is blank
"""


def test() -> None:
    """
    Convert text with blanks into uris, and check what they hold
    """
    # support
    import journal
    import pyre

    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.schemata.uris")
    # the schema
    schema = pyre.schemata.uri()

    # the texts, and the address and fragment each must yield
    cases = [
        ("file:///tmp/my file.txt", "/tmp/my file.txt", None),
        ("  /tmp/my file.txt  ", "/tmp/my file.txt", None),
        ("vfs:/local/my shapes.py/box", "/local/my shapes.py/box", None),
        ("pkg.mod.box # mine", "pkg.mod.box ", " mine"),
    ]
    # go through them
    for text, address, fragment in cases:
        # convert the text
        uri = schema.coerce(value=text)
        # if it holds something else
        if (uri.address, uri.fragment) != (address, fragment):
            # say what went wrong
            channel.line(f"the uri schema mangled {text!r}")
            # and the details
            channel.indent()
            channel.line(f"expected: address {address!r}, fragment {fragment!r}")
            channel.line(f"made: address {uri.address!r}, fragment {uri.fragment!r}")
            channel.line("look in: schemata/URI.py, URI.coerce")
            channel.outdent()

    # go through blank texts
    for text in ["", "   "]:
        # carefully
        try:
            # convert one
            uri = schema.coerce(value=text)
        # it must be refused
        except schema.CastingError as error:
            # by an error that says what was refused
            if repr(text) not in str(error):
                # if not, say so
                channel.line(f"the uri schema refused {text!r} without saying what it was")
                # and the details
                channel.indent()
                channel.line(f"error: {error}")
                channel.line("look in: schemata/URI.py, URI.coerce")
                channel.outdent()
        # if it is not refused
        else:
            # say so
            channel.line(f"the uri schema accepted {text!r} as {uri}")

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
