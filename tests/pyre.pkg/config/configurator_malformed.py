#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A malformed configuration file, in any encoding, is reported as a decoding error that says
where the file goes wrong, and none of its settings are applied
"""


def test() -> None:
    """
    Load a malformed file of each encoding, and check what is reported and what is applied
    """
    # support
    import journal
    import pyre
    from pyre.config.exceptions import DecodingError

    # get the executive
    executive = pyre.executive
    # and its nameserver
    nameserver = executive.nameserver
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.config.malformed")

    # go through the encodings
    for encoding in ["cfg", "pfg", "yaml", "pml"]:
        # the file
        uri = f"malformed.{encoding}"
        # count the errors
        errors = len(executive.errors)
        # load it
        executive.loadConfiguration(uri=uri)
        # get the errors it added
        found = executive.errors[errors:]
        # there must be exactly one decoding error
        if len(found) != 1 or not isinstance(found[0], DecodingError):
            # if not, say so
            channel.line(f"loading {uri!r} did not report one decoding error")
            # and the details
            channel.indent()
            channel.line(f"errors: {[f'{type(error).__name__}: {error}' for error in found]}")
            channel.line(f"look in: config/{encoding}, the codec and its parser")
            channel.outdent()
        # that names the file and a line in it
        elif uri not in str(found[0]) or "line=" not in str(found[0]):
            # if not, say so
            channel.line(f"the error from {uri!r} does not say where the file goes wrong")
            # and the details
            channel.indent()
            channel.line(f"error: {found[0]}")
            channel.outdent()
        # carefully
        try:
            # look up the setting in the file
            value = nameserver[f"malformed.{encoding}.applied"]
        # if it is not there
        except nameserver.UnresolvedNodeError:
            # all is well
            pass
        # if it is
        else:
            # say so
            channel.line(f"the malformed {uri!r} set 'applied' to {value!r}")

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
