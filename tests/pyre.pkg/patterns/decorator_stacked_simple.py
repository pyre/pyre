#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise {decorator}
"""


# simple decorator test
def single():
    """
    Build a decorator and use it on a class
    """
    # support
    import pyre
    import journal

    # make a decorator
    class threshold(pyre.patterns.decorator):
        """
        A decorator that checks whether the value a method received clears
        a compile time specified threshold
        """

        # metamethods
        def __init__(self, method=None, threshold=5):
            # chain up
            super().__init__(method=method)
            # save the threshold
            self.threshold = threshold
            # all done
            return

        def __call__(self, instance, value, **kwds):
            # verify that the value clears my threshold
            if value < self.threshold:
                # complain
                raise ValueError(f"value {value} does not clear {self.threshold}")
            # otherwise, invoke it
            return super().__call__(instance, value=value, **kwds)

    # and another one
    class even(pyre.patterns.decorator):
        """
        A decorator that checks whether the value a method received is even
        """

        # metamethods
        def __call__(self, instance, value, **kwds):
            # verify that the value is even
            if value % 2:
                # complain
                raise ValueError(f"value {value} is not even")
            # otherwise, invoke it
            return super().__call__(instance, value=value, **kwds)

    # make a class
    class Client:

        @even
        @threshold
        def simple(self, value):
            # make a channel
            channel = journal.debug("pyre.patterns.decorator")
            # show me
            channel.log(f"value: {value}")
            # all done
            return

    # instantiate
    client = Client()

    # invoke {simple}; this one should be ok
    client.simple(value=6)
    # this one
    try:
        # should fail
        client.simple(value=2)
    # with a value error
    except ValueError as error:
        # verify
        assert str(error) == "value 2 does not clear 5"
    # this one
    try:
        # should also fail
        client.simple(value=7)
    # with a value error
    except ValueError as error:
        # verify
        assert str(error) == "value 7 is not even"


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    single()


# end of file
