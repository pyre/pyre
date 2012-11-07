#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise the partitioner
"""


def test():
    # access the package
    import mpigsl
    # make a partitioner
    partitioner = mpigsl.partitioner()
    # exercise it
    partitioner.partition(sampleSize=4, samplesPerTask=4)
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file 
