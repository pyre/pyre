#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
An insertion into the store that is interrupted while its node is being built leaves the store
as it was: a new name gets no metadata, and an existing one keeps its locator, its priority and
its node factory, whether its value is being replaced or its trait is being configured
"""


def test() -> None:
    """
    Interrupt the building of a new node, of the replacement of an existing one, and of the
    node of a trait being configured
    """
    # support
    import pyre

    # get the store
    nameserver = pyre.executive.nameserver
    # make a priority
    priority = nameserver.priority.explicit()

    # a node factory that is interrupted
    def interrupt(**kwds) -> None:
        """
        Act as if the user hit Ctrl-C while the node is being built
        """
        # by raising the interrupt
        raise KeyboardInterrupt()

    # a new name
    name = "pyre.tests.framework.nameserver.interrupted.new"
    # carefully
    try:
        # insert a value whose node is interrupted
        nameserver.insert(
            name=name,
            value="1",
            priority=priority,
            locator=pyre.tracking.simple(source="interrupted"),
            factory=interrupt,
        )
    # the interrupt must get through
    except KeyboardInterrupt:
        # as itself
        pass
    # and if it doesn't
    else:
        # say so
        assert False, "the interrupt did not get through"
    # the name must not be left with metadata whose factory is the interrupted one, so a plain
    # assignment now works
    nameserver[name] = "2"
    # and holds the new value
    assert nameserver[name] == "2", nameserver[name]

    # an existing name
    name = "pyre.tests.framework.nameserver.interrupted.old"
    # where it was set
    original = pyre.tracking.simple(source="original")
    # set it
    key, _, _ = nameserver.insert(name=name, value="1", priority=priority, locator=original)
    # and remember the factory that built its node
    factory = nameserver.getInfo(key).factory
    # carefully
    try:
        # replace its value with one whose node is interrupted
        nameserver.insert(
            name=name,
            value="2",
            priority=nameserver.priority.explicit(),
            locator=pyre.tracking.simple(source="interrupted"),
            factory=interrupt,
        )
    # the interrupt must get through
    except KeyboardInterrupt:
        # as itself
        pass
    # and if it doesn't
    else:
        # say so
        assert False, "the interrupt did not get through"
    # get the metadata
    info = nameserver.getInfo(key)
    # the name must still be attributed to where it was set
    assert info.locator is original, info.locator
    # and its nodes must still be built by the factory it had
    assert info.factory is factory, info.factory
    # so a plain assignment now works
    nameserver[name] = "3"
    # and holds the new value
    assert nameserver[name] == "3", nameserver[name]

    # an existing name
    name = "pyre.tests.framework.nameserver.interrupted.configured"
    # set it
    key, _, _ = nameserver.insert(name=name, value="1", priority=priority, locator=original)
    # and remember the factory that built its node
    factory = nameserver.getInfo(key).factory
    # carefully
    try:
        # configure a trait by that name, with a node factory that is interrupted
        nameserver.insert(
            name=name,
            value="2",
            priority=nameserver.priority.defaults(),
            locator=pyre.tracking.simple(source="interrupted"),
            factory=interrupt,
        )
    # the interrupt must get through
    except KeyboardInterrupt:
        # as itself
        pass
    # and if it doesn't
    else:
        # say so
        assert False, "the interrupt did not get through"
    # the nodes of the name must still be built by the factory it had
    assert nameserver.getInfo(key).factory is factory, nameserver.getInfo(key).factory
    # so a plain assignment now works
    nameserver[name] = "3"
    # and holds the new value
    assert nameserver[name] == "3", nameserver[name]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
