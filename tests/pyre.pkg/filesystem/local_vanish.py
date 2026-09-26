#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that exploring a local filesystem copes with a folder that disappears while it is being
explored, and that every folder is listed exactly once

A live filesystem is entitled to change under a traversal: a folder that was listed as part of
its parent can be removed before the traversal gets to it. The traversal must forget such a
folder rather than fail, while a folder that is still there but cannot be read is reported
"""


def test():
    """
    Explore a tree whose walker removes a folder right after listing its parent
    """
    # externals
    import collections
    import os
    import shutil

    # get the package
    import pyre.filesystem

    # and the walker class, which is what a custom walker specializes
    from pyre.filesystem.Walker import Walker

    # the scratch tree
    top = os.path.abspath("local_vanish")
    # make sure a stale one is not lying around
    shutil.rmtree(top, ignore_errors=True)
    # lay out a few folders, one of which is about to disappear
    for path in ("keep/inner", "gone/inner", "other"):
        # make each one
        os.makedirs(os.path.join(top, path))
    # and a file, so there is something that is not a folder
    open(os.path.join(top, "keep", "file"), "w").close()

    # a walker that counts the listings, and removes {gone} just as it is about to list it,
    # after its parent listed it and the traversal recognized it as a folder
    class Vanishing(Walker):
        """
        A walker whose filesystem changes under it
        """

        # the listings, by folder
        listings = collections.Counter()

        @classmethod
        def walk(cls, path):
            """
            List {path}, unless it is {gone}, which disappears first
            """
            # count the listing
            cls.listings[str(path)] += 1
            # if this is the folder that is about to disappear
            if str(path) == os.path.join(top, "gone"):
                # take it away
                shutil.rmtree(path)
            # list the folder, which fails for the one that is gone
            return super().walk(path)

    # mount a filesystem there
    fs = pyre.filesystem.local(root=top)
    # and explore it with the vanishing walker
    fs.discover(walker=Vanishing)

    # the folder that disappeared is forgotten
    assert "gone" not in fs.contents
    # and the rest of the tree is there
    assert "keep" in fs.contents and "other" in fs.contents
    assert "inner" in fs["keep"].contents and "file" in fs["keep"].contents
    # every folder was listed exactly once, the one that disappeared included
    assert all(count == 1 for count in Vanishing.listings.values()), Vanishing.listings
    # and they were all listed
    assert set(Vanishing.listings) >= {
        top,
        os.path.join(top, "gone"),
        os.path.join(top, "keep"),
        os.path.join(top, "keep", "inner"),
        os.path.join(top, "other"),
    }

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
