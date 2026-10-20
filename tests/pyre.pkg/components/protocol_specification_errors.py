#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A protocol asked to resolve text that is not a component specification raises a
{FacilitySpecificationError}, which is the {ResolutionError} of text that cannot be a uri
"""


def test() -> None:
    """
    Ask a protocol to resolve blank text, and check what its error says
    """
    # support
    import journal
    import pyre
    from pyre.components.exceptions import FacilitySpecificationError, ResolutionError
    from pyre.schemata.exceptions import CastingError

    # a protocol
    class Parts(pyre.protocol, family="pyre.tests.components.specifications.parts"):
        """
        The protocol that resolves the text
        """

    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.specifications")

    # go through texts that are not component specifications
    for spec in ["", "  "]:
        # carefully
        try:
            # ask the protocol to resolve one
            Parts.pyre_resolveSpecification(spec=spec)
        # it must be refused
        except FacilitySpecificationError as error:
            # get the complaint
            complaint = str(error)
            # find what it leaves out
            missing = [
                text
                for text in [repr(spec), "pyre.tests.components.specifications.parts"]
                if text not in complaint
            ]
            # the ways the error is wrong
            flaws = [
                # it names something other than the protocol that was asked
                "protocol" if error.protocol is not Parts else None,
                # or something other than the text it was given
                "value" if error.value != spec else None,
                # it does not carry the error that refused the text as a uri
                "error" if not isinstance(error.error, CastingError) else None,
                # or it would escape the handlers of failed resolutions
                "type" if not isinstance(error, ResolutionError) else None,
            ]
            # keep the real ones
            flaws = [flaw for flaw in flaws if flaw]
            # if anything is amiss
            if missing or flaws:
                # say what went wrong
                channel.line(f"the protocol refused {spec!r}, but its error is wrong")
                # and the details
                channel.indent()
                channel.line(f"error: {complaint}")
                channel.line(f"lacks: {', '.join(map(repr, missing))}")
                channel.line(f"wrong: {', '.join(flaws)}")
                channel.line("look in: components/Protocol.py, components/exceptions.py")
                channel.outdent()
        # if it is refused some other way
        except pyre.PyreError as error:
            # say what went wrong
            channel.line(f"the protocol refused {spec!r} with the wrong error")
            # and the details
            channel.indent()
            channel.line("expected: FacilitySpecificationError")
            channel.line(f"got: {type(error).__name__}: {error}")
            channel.line("look in: components/Protocol.py, Protocol.pyre_resolveSpecification")
            channel.outdent()
        # if it is not refused at all
        else:
            # say so
            channel.line(f"the protocol resolved {spec!r}")

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
