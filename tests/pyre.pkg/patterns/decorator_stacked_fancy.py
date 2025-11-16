#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


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
    class parity(pyre.patterns.decorator):
        """
        A decorator that checks whether the value a method received is even
        """

        # metamethods
        def __init__(self, method=None, parity=0):
            # chain up
            super().__init__(method=method)
            # save the {parity}
            self.parity = parity
            # all done
            return

        def __call__(self, instance, value, **kwds):
            # verify that the value is even
            if value % 2 != self.parity:
                # complain
                raise ValueError(f"value {value} != {self.parity} mod 2")
            # otherwise, invoke it
            return super().__call__(instance, value=value, **kwds)

    # make a class
    class Client:
        """
        A class with a decorated method
        """

        @threshold(threshold=3)
        @parity(parity=1)
        def fancy(self, value):
            # make a channel
            channel = journal.debug("pyre.patterns.decorator")
            # show me
            channel.log(f"value: {value}")
            # all done
            return

    # instantiate
    client = Client()

    # invoke {fancy}; the first one should be ok
    client.fancy(value=3)
    # the second one
    try:
        # should fail
        client.fancy(value=1)
    # with a value error
    except ValueError as error:
        # verify
        assert str(error) == "value 1 does not clear 3"
    # this one
    try:
        # should also fail
        client.fancy(value=4)
    # with a value error
    except ValueError as error:
        # verify
        assert str(error) == "value 4 != 1 mod 2"


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    single()


# end of file
