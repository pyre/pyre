#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that deleting a trait an instance has read makes it follow its class again, as with a python
cached property
"""


def test() -> None:
    """
    Make an instance, read its trait, change the class, delete the trait, and read the instance
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # an instance
    b = base(name="b")
    # that reads its trait
    assert b.t == "class"
    # change the class
    base.t = "changed"
    # forget what the instance read
    del b.t
    # so it sees the class again
    assert b.t == "changed"
    # forget it again
    del b.t
    # and change the class once more
    base.t = "again"
    # the instance follows
    assert b.t == "again"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
