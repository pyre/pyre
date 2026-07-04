#! /usr/bin/env python3
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

    # and confirm it published the prompts we expect
    assert survey.Input
    assert survey.Confirm
    assert survey.Select

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
