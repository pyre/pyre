#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a protocol names the role of its implementers after its class, unless it says
otherwise, and that the role is independent of its family
"""


def test() -> None:
    """
    Check the default role, an override, and that a subclass gets its own default
    """
    # support
    import pyre

    # a protocol that relies on the default
    class Reader(pyre.protocol, family="test.protocols.readers"):
        """a protocol whose role is the name of its class"""

    # a protocol whose public names are not in english
    class Writer(pyre.protocol, family="test.protocols.writers"):
        """a protocol that names its role itself"""

        # the role of its implementers
        @classmethod
        def pyre_role(cls) -> str:
            """
            The word for what one of my implementers does
            """
            # in greek
            return "γραφέας"

    # a refinement that does not say
    class Scanner(Reader, family="test.protocols.scanners"):
        """a refinement of the reader that relies on the default"""

    # the default is the name of the class in lower case, not anything derived from the family
    assert Reader.pyre_role() == "reader", Reader.pyre_role()
    # an override is what the protocol says it is
    assert Writer.pyre_role() == "γραφέας", Writer.pyre_role()
    # a refinement gets the default from its own class, not the role of its ancestor
    assert Scanner.pyre_role() == "scanner", Scanner.pyre_role()
    # and none of this disturbs the family
    assert Reader.pyre_family() == "test.protocols.readers", Reader.pyre_family()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
