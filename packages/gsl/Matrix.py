# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import numbers
from . import gsl # the extension


# the class declaration
class Matrix:
    """
    A wrapper over a gsl matrix
    """


    # initialization
    def zero(self):
        """
        Set all my elements to zero
        """
        # zero me out
        gsl.matrix_zero(self.data)
        # and return
        return self


    def fill(self, value):
        """
        Set all my elements to {value}
        """
        # fill
        gsl.matrix_fill(self.data, value)
        # and return
        return self


    def identity(self):
        """
        Initialize me as an identity matrix: all elements are set to zero except along the
        diagonal, which are set to one
        """
        # initialize
        gsl.matrix_identity(self.data)
        # and return
        return self


    # maxima and minima
    def max(self):
        """
        Compute my maximum value
        """
        # easy enough
        return gsl.matrix_max(self.data)


    def min(self):
        """
        Compute my maximum value
        """
        # easy enough
        return gsl.matrix_min(self.data)


    def minmax(self):
        """
        Compute my minimum and maximum values
        """
        # easy enough
        return gsl.matrix_minmax(self.data)


    # meta methods
    def __init__(self, shape, **kwds):
        super().__init__(**kwds)
        self.shape = shape
        self.data = gsl.matrix_alloc(shape)
        return


    # container support
    def __iter__(self):
        # unpack the shape
        index0, index1 = self.shape
        # iterate over all the elements
        for i in range(index0):
            for j in range(index1):
                yield gsl.matrix_get(self.data, i, j)
        # all done
        return


    def __contains__(self, value):
        # faster than checking every element in python
        return gsl.matrix_contains(self.data, value)


    def __getitem__(self, index):
        # unpack the index
        index0, index1 = index
        # unpack the shape
        size0, size1 = self.shape
        # reflect negative indices around the end of the matrix
        if index0 < 0: index0 = size0 - index0
        if index1 < 0: index1 = size1 - index1
        # bounds check index0
        if index0 < 0 or index0 >= size0:
            # and complain
            raise IndexError('matrix index {} out of range'.format(index0))
        # bounds check index1
        if index1 < 0 or index1 >= size1:
            # and complain
            raise IndexError('matrix index {} out of range'.format(index1))
        # get and return the element
        return gsl.matrix_get(self.data, index0, index1)


    def __setitem__(self, index, value):
        # unpack the index
        index0, index1 = index
        # unpack the shape
        size0, size1 = self.shape
        # reflect negative indices around the end of the matrix
        if index0 < 0: index0 = size0 - index0
        if index1 < 0: index1 = size1 - index1
        # bounds check index0
        if index0 < 0 or index0 >= size0:
            # and complain
            raise IndexError('matrix index {} out of range'.format(index0))
        # bounds check index1
        if index1 < 0 or index1 >= size1:
            # and complain
            raise IndexError('matrix index {} out of range'.format(index1))
        # set the element to the requested value
        gsl.matrix_set(self.data, int(index0), int(index1), value)
        # and return
        return self


    # in-place arithmetic
    def __iadd__(self, other):
        """
        In-place addition with the elements of {other}
        """
        # if other is a matrix
        if type(other) is type(self):
            # do matrix-matrix addition
            gsl.matrix_add(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do constant addition
            gsl.matrix_shift(self.data, other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    def __isub__(self, other):
        """
        In-place subtraction with the elements of {other}
        """
        # if other is a matrix
        if type(other) is type(self):
            # do matrix-matrix subtraction
            gsl.matrix_sub(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do constant subtraction
            gsl.matrix_shift(self.data, -other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    def __imul__(self, other):
        """
        In-place multiplication with the elements of {other}
        """
        # if other is a matrix
        if type(other) is type(self):
            # do matrix-matrix multiplication
            gsl.matrix_mul(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do scaling by constant
            gsl.matrix_scale(self.data, other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    def __itruediv__(self, other):
        """
        In-place addition with the elements of {other}
        """
        # if other is a matrix
        if type(other) is type(self):
            # do matrix-matrix division
            gsl.matrix_div(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do scaling by constant
            gsl.matrix_scale(self.data, 1/other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    # private data
    data = None
    shape = (0,0)


# end of file 
