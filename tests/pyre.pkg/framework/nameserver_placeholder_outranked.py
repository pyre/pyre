#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the placeholder a reference leaves behind ranks below every source, so the value
that arrives later replaces it
"""


def test():
    """
    Refer to a name nobody has set, then set it at the lowest rank a source uses, and check
    that the value lands and the reference sees it
    """
    # access the package
    import pyre

    # and the nameserver
    nameserver = pyre.executive.nameserver

    # refer to a name that nobody has set yet
    nameserver["placeholder.label"] = "{placeholder.count} items"
    # which leaves a placeholder under that name
    key = nameserver.hash("placeholder.count")
    # whose rank
    rank = nameserver.getInfo(key).priority
    # is the one that marks a missing setting
    assert rank.category == nameserver.priority.uninitialized.category
    # which is below the rank of the defaults of traits
    assert rank < nameserver.priority.defaults()

    # set the name at the rank of the settings made at boot, the lowest one any source uses
    _, new, _ = nameserver.insert(
        name="placeholder.count", value="16", priority=nameserver.priority.boot(), locator=None
    )
    # the store accepts it
    assert new is not None
    # the value lands
    assert nameserver["placeholder.count"] == "16"
    # and the reference sees it
    assert nameserver["placeholder.label"] == "16 items"

    # all done
    return nameserver


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
