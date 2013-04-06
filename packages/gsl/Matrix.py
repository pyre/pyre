# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import numbers
from . import gsl # the extension


# the class declaration
class Matrix:
    """
    A wrapper over a gsl matrix
    """

    # types
    from .Vector import Vector as vector

    # constants
    upperTriangular = 1
    lowerTriangular = 0

    # flag that controls whether the diagonal entries are assumed to be unity
    unitDiagonal = 1
    nonUnitDiagonal = 0

    # operation flags for some of the blas primitives
    opNoTrans = 0
    opTrans = 1
    opConjTrans = 2

    # flag to control the order of operands in some matrix multiplication routines
    sideRight = 1
    sideLeft = 0

    # sort type for eigensystems
    sortValueAscending = 0
    sortValueDescending = 1
    sortMagnitudeAscending = 2
    sortMagnitudeDescending = 3


    # class methods
    # mpi support
    @classmethod
    def bcast(cls, matrix=None, communicator=None, source=0):
        """
        Broadcast the given {matrix} from {source} to all tasks in {communicator}
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi
            # use the world by default
            communicator = mpi.world
        # get the matrix capsule
        data = None if matrix is None else matrix.data
        # scatter the data
        capsule, shape = gsl.bcastMatrix(communicator.capsule, source, data)
        # dress up my local portion as a matrix
        result = cls(shape=shape, data=capsule)
        # and return it
        return result


    @classmethod
    def collect(cls, matrix, communicator=None, destination=0):
        """
        Gather the data in {matrix} from each task in {communicator} into one big matrix
        available at the {destination} task
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi
            # use the world by default
            communicator = mpi.world
        # gather the data
        result = gsl.gatherMatrix(communicator.capsule, destination, matrix.data)
        # if i am not the destination task, nothing further to do
        if communicator.rank != destination: return
        # otherwise, unpack the result
        data, shape = result
        # dress up the result as a matrix
        result = cls(shape=shape, data=data)
        # and return it
        return result


    @classmethod
    def partition(cls, taskload, communicator=None, source=0, matrix=None):
        """
        Scatter {matrix} held by the task {source} among all tasks in {communicator}. Only
        {source} has to provide a {matrix}; the other tasks can use the default value. Each
        task gets a matrix whose layout is described by {taskload}.
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi
            # use the world by default
            communicator = mpi.world
        # get the matrix capsule
        data = None if matrix is None else matrix.data
        # scatter the data
        partition = gsl.scatterMatrix(communicator.capsule, source, data, taskload)
        # dress up my local portion as a matrix
        result = cls(shape=taskload, data=partition)
        # and return it
        return result


    # public data
    @property
    def columns(self):
        """
        Get the number of columns
        """
        return self.shape[1]

    @property
    def rows(self):
        """
        Get the number of rows
        """
        return self.shape[0]


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


    def read(self, filename):
        """
        Read my values from {filename}
        """
        # read
        gsl.matrix_read(self.data, filename)
        # and return
        return self


    def write(self, filename):
        """
        Write my values to {filename}
        """
        # write
        gsl.matrix_write(self.data, filename)
        # and return
        return self


    def print(self, format='{:+12.5e}', width=100, indent=''):
        """
        Print my values using the given {format}
        """
        # for each row
        for i in range(self.rows):
            # print the left margin: a '[[' on the first row, nothing on the others
            print('{}{}'.format(indent, '[[' if i==0 else '  '), end=' ')
            # the row entries
            for j in range(self.columns):
                print(format.format(self[i,j]), end=' ')
            # the right margin
            print('{}'.format(']]' if i==self.rows-1 else '  '))
        # all done
        return


    def identity(self):
        """
        Initialize me as an identity matrix: all elements are set to zero except along the
        diagonal, which are set to one
        """
        # initialize
        gsl.matrix_identity(self.data)
        # and return
        return self


    def random(self, pdf):
        """
        Fill me with random numbers using the probability distribution {pdf}
        """
        # the {pdf} knows how to do this
        return pdf.matrix(matrix=self)


    def clone(self):
        """
        Allocate a new matrix and initialize it using my values
        """
        # build the clone
        clone = type(self)(shape=self.shape)
        # have the extension initialize the clone
        gsl.matrix_copy(clone.data, self.data)
        # and return it
        return clone

    # matrix operations
    def transpose(self, destination=None):
        """
        Compute the transpose of a matrix. 

        If {destination} is {None} and the matrix is square, the operation happens
        in-place. Otherwise, the transpose is stored in {destination}, which is assumed to be
        shaped correctly.
        """
        # if we have a {destination}
        if destination is not None:
            # do the transpose
            gsl.matrix_transpose(self.data, destination.data)
            # and return the destination matrix
            return destination
        # otherwise
        gsl.matrix_transpose(self.data, None)
        # and return myself
        return self


    # slicing
    def getRow(self, index):
        """
        Return a view to the requested row
        """
        # let the extension do its thing
        capsule = gsl.matrix_get_row(self.data, int(index))
        # build a vector and return it
        return self.vector(shape=self.columns, data=capsule)


    def getColumn(self, index):
        """
        Return a view to the requested column
        """
        # let the extension do its thing
        capsule = gsl.matrix_get_col(self.data, int(index))
        # build a vector and return it
        return self.vector(shape=self.rows, data=capsule)


    def setRow(self, index, v):
        """
        Set the row at {index} to the contents of the given vector {v}
        """
        # let the extension do its thing
        gsl.matrix_set_row(self.data, int(index), v.data)
        # and return
        return self


    def setColumn(self, index, v):
        """
        Set the column at {index} to the contents of the given vector {v}
        """
        # let the extension do its thing
        gsl.matrix_set_col(self.data, int(index), v.data)
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


    # eigensystems
    def symmetricEigensystem(self, order=sortValueAscending):
        """
        Computed my eigenvalues and eigenvectors assuming i am a real symmetric matrix
        """
        # compute the eigenvalues and eigenvectors
        values, vectors = gsl.matrix_eigen_symmetric(self.data, order)
        # dress up the results
        λ = self.vector(shape=self.rows, data=values)
        x = type(self)(shape=self.shape, data=vectors)
        # and return
        return λ, x


    # meta methods
    def __init__(self, shape, data=None, **kwds):
        super().__init__(**kwds)
        self.shape = shape
        self.data = gsl.matrix_alloc(shape) if data is None else data
        return


    # container support
    def __iter__(self):
        # unpack the shape
        index0, index1 = self.shape
        # iterate over all the elements
        for i in range(index0):
            for j in range(index1):
                yield gsl.matrix_get(self.data, (i, j))
        # all done
        return


    def __contains__(self, value):
        # faster than checking every element in python
        return gsl.matrix_contains(self.data, value)


    def __getitem__(self, index):
        # get and return the element
        return gsl.matrix_get(self.data, index)


    def __setitem__(self, index, value):
        # set the element to the requested value
        return gsl.matrix_set(self.data, index, value)


    # comparisons
    def __eq__(self, other):
        # type check
        if type(self) is not type(other): return NotImplemented
        # hand the request off to the extension module
        return gsl.matrix_equal(self.data, other.data)


    def __ne__(self, other):
        return not (self == other)


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
            gsl.matrix_shift(self.data, float(other))
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
            gsl.matrix_shift(self.data, -float(other))
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
            gsl.matrix_scale(self.data, float(other))
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
            gsl.matrix_scale(self.data, 1/float(other))
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


    # private data
    data = None
    shape = (0,0)


# end of file 
