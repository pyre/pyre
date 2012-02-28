#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Fill a vector with a constant value
"""


def test():
    # package access
    import gsl
    # make a vector
    v = gsl.vector(shape=100)
    # set it to some value
    v.random(pdf=gsl.pdf.uniform(support=(-1,1), rng=gsl.rng()))
    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file 
