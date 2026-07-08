#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Sanity check: verify that the package is accessible
    """
    # access the package
    import survey

    # the text prompt is published
    assert survey.Input
    # the yes/no prompt is published
    assert survey.Confirm
    # the menu prompt is published
    assert survey.Select

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
