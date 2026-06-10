#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the design invariant that holds {exitCode} together: every document in {pyre.http.documents}
that aborts the process derives from {Exit}, so the abort flag and its exit code come from one place
"""

# the document types
from pyre.http import documents


def test():
    # the single carrier of the abort behavior
    exit = documents.Exit

    # go through every name the documents module exposes
    for entity in vars(documents).values():
        # skip anything that is not a class
        if not isinstance(entity, type):
            # move on
            continue
        # skip names imported from elsewhere; only audit classes declared in this module
        if entity.__module__ != documents.__name__:
            # move on
            continue
        # a document that aborts the process must derive from {Exit}, or it sidesteps the one place
        # that carries an {exitCode}
        if getattr(entity, "abort", False):
            # enforce the invariant
            assert issubclass(entity, exit)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
