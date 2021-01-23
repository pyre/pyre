#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Tests for all the exceptions raised by this package
    """

    # get the exception
    from pyre.constraints.exceptions import ConstraintViolationError

    # exercise it
    try:
        # raise it
        raise ConstraintViolationError(constraint=None, value=None)
    # catch it
    except ConstraintViolationError as error:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
