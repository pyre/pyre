#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Lijun Zhu
# Caltech
# (c) 1998-2019 all rights reserved
#


"""
Exercise computing the mean value and standard deviation for each row/column of a matrix
"""


def test():
    # package access
    import gsl
    import math
    # make a matrix
    rows = 100
    cols = 6
    m = gsl.matrix(shape=(rows,cols))
    # initial values as [ [0,0,0...],[1,1,1...],[0,0,0...], [1,1,1....],...]
    v = gsl.vector(shape=cols)
    for i in range(rows):
        v.fill(value=i%2)
        m.setRow(i, v)
    # compute mean/sd by row
    mean, sdev = m.mean_sd(byrow=True)
    # check it: each row is a constant and sdev=0
    assert mean[0] == 0 and sdev[0] == 0
    assert mean[1] == 1 and sdev[0] == 0
    # compute mean/sd by column
    mean, sdev = m.mean_sd()
    # check it
    # each col is 0,1,0,1... and mean=0.5, sdev^2 = sum_i(x_i-mean)^2/(n-1)
    assert mean[0] == 0.5 and sdev[0] == math.sqrt(rows*0.25/(rows-1))
    # all done
    return m


# main
if __name__ == "__main__":
    test()


# end of file
