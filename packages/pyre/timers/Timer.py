# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# for my superclass and metaclass
import pyre


# the base class that sets up the interface and instance registry
class Timer(pyre.patterns.named, metaclass=pyre.patterns.unique):
    """
    Abstract base class for pyre timers

    Subclasses must provide access to a functioning {clock} and implement the convenience
    time unit conversions
    """


    # interface
    def start(self):
        """
        Start the timer
        """
        # if i'm already active
        if self.active:
            # go no further
            return self.mark
        # otherwise, activate me
        self.active = True
        # read and store the clock
        mark = self.clock()
        # store the mark
        self.mark = mark
        # and return it
        return mark


    def stop(self):
        """
        Stop the timer
        """
        # if i'm inactive
        if not self.active:
            # do nothing
            return self.elapsed
        # otherwise, compute the time elapsed since the last {start}
        elapsed = self.clock() - self.mark
        # mark me as inactive
        self.active = False
        # update the elapsed time
        self.elapsed += elapsed
        # and return the new adjustment
        return elapsed


    def reset(self):
        """
        Reset the timer: mark it as inactive and set the accumulated time back to zero
        """
        # deactivate
        self.active = False
        # reset the time mark
        self.mark = None
        # and the accumulator
        self.elapsed = 0
        # all done
        return


    def read(self):
        """
        Get the accumulated time
        """
        # if this is an inactive timer
        if not self.active:
            # return the accumulated time
            return self.elapsed
        # otherwise, non-destructively compute the time accumulated since the last {start}
        elapsed = self.clock() - self.mark
        # and return the total accumulated time
        return self.elapsed + elapsed


    def sec(self):
        """
        Convert the accumulated time into seconds
        """
        # subclasses must provide
        raise NotImplementedError(f"class '{type(self).__name__}' must provide 'sec'")


    def ms(self):
        """
        Convert the accumulated time into milliseconds
        """
        # subclasses must provide
        raise NotImplementedError(f"class '{type(self).__name__}' must provide 'ms'")


    def us(self):
        """
        Convert the accumulated time into microseconds
        """
        # subclasses must provide
        raise NotImplementedError(f"class '{type(self).__name__}' must provide 'us'")


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # mark me as inactive
        self.active = False
        # initialize my time mark
        self.mark = None
        # and my time accumulator
        self.elapsed = 0
        # all done
        return


    def __bool__(self):
        # check with my status
        return self.active


    # implementation details
    def clock(self):
        """
        The provider of timestamps
        """
        # subclasses must provide
        raise NotImplementedError(f"class '{type(self).__name__}' must provide 'clock'")


# end of file
