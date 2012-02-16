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
class Vector:
    """
    A wrapper over a gsl vector
    """

    # initialization
    def zero(self):
        """
        Set all my elements to zero
        """
        # zero me out
        gsl.vector_zero(self.data)
        # and return
        return self


    def fill(self, value):
        """
        Set all my elements to {value}
        """
        # fill
        gsl.vector_fill(self.data, value)
        # and return
        return self


    def basis(self, index):
        """
        Initialize me as a basis vector: all elements are set to zero except {index}, which is
        set to one
        """
        # initialize
        gsl.vector_basis(self.data, index)
        # and return
        return self


    # meta methods
    def __init__(self, size, **kwds):
        super().__init__(**kwds)
        self.size = size
        self.data = gsl.vector_allocate(size)
        return


    # container support
    def __len__(self): return self.size


    def __iter__(self):
        # for each valid value of the index
        for index in range(self.size):
            # produce the corresponding element
            yield gsl.vector_get(self.data, index)
        # no more
        return


    def __contains__(self, value):
        # faster than checking every element in python
        return gsl.vector_contains(self.data, value)


    def __getitem__(self, index):
        # reflect negative indices around the end of the vector
        if index < 0: index = self.size - index
        # bounds check
        if index < 0 or index >= self.size:
            # and complain
            raise IndexError('vector index {} out of range'.format(index))
        # get and return the element
        return gsl.vector_get(self.data, index)


    def __setitem__(self, index, value):
        # reflect negative indices around the end of the vector
        if index < 0: index = self.size - index
        # bounds check
        if index < 0 or index >= self.size:
            # and complain
            raise IndexError('vector index {} out of range'.format(index))
        # set the element to the rquested value
        gsl.vector_set(self.data, int(index), value)
        # and return
        return self


    # in-place arithmetic
    def __iadd__(self, other):
        """
        In-place addition with the elements of {other}
        """
        # if other is a vector
        if type(other) is type(self):
            # do vector-vector addition
            gsl.vector_add(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do constant addition
            gsl.vector_shift(self.data, other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    def __isub__(self, other):
        """
        In-place subtraction with the elements of {other}
        """
        # if other is a vector
        if type(other) is type(self):
            # do vector-vector subtraction
            gsl.vector_sub(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do constant subtraction
            gsl.vector_shift(self.data, -other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    def __imul__(self, other):
        """
        In-place multiplication with the elements of {other}
        """
        # if other is a vector
        if type(other) is type(self):
            # do vector-vector multiplication
            gsl.vector_mul(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do scaling by constant
            gsl.vector_scale(self.data, other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    def __itruediv__(self, other):
        """
        In-place addition with the elements of {other}
        """
        # if other is a vector
        if type(other) is type(self):
            # do vector-vector division
            gsl.vector_div(self.data, other.data)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do scaling by constant
            gsl.vector_scale(self.data, 1/other)
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    # private data
    data = None


# end of file 
