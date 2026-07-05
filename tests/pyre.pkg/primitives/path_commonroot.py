#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise {path.commonRoot}, the longest logical ancestor shared by two paths
"""


def test():
    # the home of the factory
    import pyre

    # a shorthand
    path = pyre.primitives.path

    # two absolute paths that share a leading portion
    mine = path("/Users/mga/dv/pyre")
    hers = path("/Users/mga/tmp/foo")
    # their common root is the shared prefix
    assert str(mine.commonRoot(hers)) == "/Users/mga"

    # when one path is a logical ancestor of the other
    ancestor = path("/Users/mga")
    child = path("/Users/mga/dv/pyre")
    # the common root is the ancestor itself
    assert str(child.commonRoot(ancestor)) == "/Users/mga"
    # regardless of the order of the operands
    assert str(ancestor.commonRoot(child)) == "/Users/mga"

    # a path is its own common root with itself
    assert str(child.commonRoot(child)) == str(child)

    # two absolute paths that diverge right after the root
    assert str(path("/Users/mga").commonRoot("/etc/hosts")) == "/"

    # the operation is symmetric
    left = path("/a/b/c")
    right = path("/a/x")
    assert str(left.commonRoot(right)) == str(right.commonRoot(left))

    # two relative paths that share a prefix
    assert str(path("a/b/c").commonRoot("a/b/d")) == "a/b"

    # two relative paths with nothing in common yield the empty path, i.e. the cwd
    assert str(path("a/b").commonRoot("x/y")) == "."

    # {other} is coerced, so a plain string works just like a path
    assert str(path("/a/b/c").commonRoot("/a/b/d")) == "/a/b"

    # and the result is a genuine path, not a bare tuple
    assert isinstance(mine.commonRoot(hers), pyre.primitives.path)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
