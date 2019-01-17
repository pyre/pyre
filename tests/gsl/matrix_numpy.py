#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Lijun Zhu
# Caltech
# (c) 1998-2019 all rights reserved
#


"""
Test numpy wrapper for gsl.matrix
"""


def test():
    # package access
    import gsl
    import numpy
    # make a gsl.matrix and initialize it
    rows = 100
    cols = 6
    m = gsl.matrix(shape=(rows,cols)).fill(value=0)

    # test the numpy wrapper
    np_array_ref = m.asnumpy()
    # reassign values with numpy function
    np_array_ref.fill(1.0)
    # check the values of gsl.matrix and numpy.array are the same (they use the same data)
    assert np_array_ref[10,3] ==  m[10,3]

    # test the numpy copier
    np_array = m.tonumpy()
    # check the data is copied over correctly
    assert np_array[10,3] == m[10,3]
    # reassign values
    np_array.fill(2.0)
    # verify their values are different now
    assert np_array[10,3] != m[10,3]
    # all done
    return m

# main
if __name__ == "__main__":
    test()


# end of file
