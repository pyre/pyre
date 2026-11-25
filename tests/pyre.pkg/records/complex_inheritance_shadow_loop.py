#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse a record whose shadowing derivation makes its derivations depend on themselves
"""


def test():
    """
    Derive a record that redeclares an operand of a derivation of its base as a derivation of
    that same derivation, and check that the declaration is refused
    """
    # access the package
    import pyre.records

    # and the journal
    import journal

    # the base record
    class item(pyre.records.record):
        """
        An item whose price is its cost plus its overhead
        """

        # the cost
        cost = pyre.records.float()
        # the overhead
        overhead = pyre.records.float()
        # and the price
        price = cost + overhead

    # the refusal is expected, so its report goes nowhere
    journal.firewall("pyre.records").device = journal.trash()
    # attempt to
    try:
        # derive a record whose cost is computed from its price, which is computed from its cost
        class circular(item):
            """
            An item whose cost depends on its price
            """

            # the cost
            cost = 0.5 * item.price

        # which must not be built
        assert False, "unreachable"
    # it fails
    except journal.FirewallError as error:
        # with a report that names the fields around the loop
        report = "\n".join(error.page)
        # the cost
        assert "'cost'" in report, report
        # and the price
        assert "'price'" in report, report

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
