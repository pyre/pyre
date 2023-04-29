# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import time
# base class
from .Timer import Timer


# a timer that measure elapsed wall clock time
class ProcessTimer(Timer):
    """
    Use a monotonic wall clock to provide timing info
    """


    # interface
    def sec(self):
        """
        Convert the elapsed time into seconds
        """
        # my clock uses seconds internally
        return self.read()


    def ms(self):
        """
        Convert the elapsed time into milliseconds
        """
        # my clock uses seconds internally
        return 1000 * self.read()


    def us(self):
        """
        Convert the elapsed time into microseconds
        """
        return 1000 * 1000 * self.read()


    # implementation details
    def clock(self):
        """
        Generate a time stamp
        """
        # use the per-process high resolution clock to get a time stamp
        return time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)


# end of file
