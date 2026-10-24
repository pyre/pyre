#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that declaring a dimensional with units that are not a quantity, or a quantity that is not a
name, fires a firewall, since the mistake is in the code that declares it
"""


def test() -> None:
    """
    Declare dimensionals with bad units and quantities
    """
    # the journal
    import journal

    # and the schemata
    import pyre.schemata
    from pyre.units.SI import newton

    # the firewall fires on purpose here; keep its report out of the way
    journal.firewall("pyre.schemata").device = journal.trash()
    # each of these
    for kwds in (
        {"units": "newton"},
        {"units": 1},
        {"units": True},
        {"quantity": 5},
        {"quantity": ""},
        {"quantity": "  "},
        {"units": newton, "quantity": newton},
    ):
        # attempt to
        try:
            # declare a dimensional
            pyre.schemata.dimensional(**kwds)
            # which should be unreachable
            assert False, kwds
        # if the firewall fires, as expected
        except journal.FirewallError:
            # all good
            pass
    # while a consistent declaration is fine
    schema = pyre.schemata.dimensional(units=newton, quantity="force")
    # and keeps its units
    assert schema.units is newton, schema.units
    # and the name of what it measures
    assert schema.quantity == "force", schema.quantity

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
