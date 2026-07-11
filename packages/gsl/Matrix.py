# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import numbers
import itertools
from . import libgsl as gsl  # the extension


# the class declaration
class Matrix(gsl.Matrix):
    """
    A matrix of doubles

    The storage, the buffer protocol, and the views are the extension's; everything that reads
    more naturally in python -- the file i/o, the arithmetic operators, the statistics -- lives
    here
    """

    # types
    from .Vector import Vector as vector

    # constants
    defaultFormat = "+16.7"

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
        # with a single process there is nobody to send to, and the source already holds the
        # answer; this is also the only path there is on a machine with no mpi, where the
        # extension was built without {bcastMatrix}
        if communicator.size == 1:
            # the lone process is the only one that can be the source
            if source != communicator.rank:
                raise ValueError(f"rank {source} cannot be the source: there is no such task")
            # and, just as in the parallel case, it must have brought a matrix
            if matrix is None:
                raise TypeError("the source task must supply a matrix to broadcast")
            # which is already the answer
            return matrix
        # broadcast; the source passes its own matrix, everybody else passes nothing
        result = gsl.bcastMatrix(communicator, source, matrix)
        # the source already holds the answer, in the right subclass
        if communicator.rank == source:
            return matrix
        # everybody else received a plain bound matrix, so we copy it into our subclass
        return cls(shape=result.shape).copy(result)

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

            # use the {world} by default
            communicator = mpi.world
        # with a single process there is nobody to collect from; the one contribution is the
        # whole answer, and the parallel path hands back fresh storage, so we clone
        if communicator.size == 1:
            # the lone process is the only one that can be the destination
            if destination != communicator.rank:
                raise ValueError(
                    f"rank {destination} cannot be the destination: there is no such task"
                )
            # its contribution is the entire collection
            return matrix.clone()
        # gather the contributions; the destination gets a plain bound matrix, everybody else None
        result = gsl.gatherMatrix(communicator, destination, matrix)
        # if i am not the destination task, nothing further to do
        if communicator.rank != destination:
            return
        # otherwise, copy the plain bound matrix into our subclass
        return cls(shape=result.shape).copy(result)

    def excerpt(self, communicator=None, source=0, matrix=None):
        """
        Scatter {matrix} held by the task {source} among all tasks in {communicator} and fill me
        with the partition values. Only {source} has to provide a {matrix}; the other tasks can
        use the default value.
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi

            # use the world by default
            communicator = mpi.world
        # with a single process there is nobody to scatter to; my partition is all of {matrix}
        if communicator.size == 1:
            # the lone process is the only one that can be the source
            if source != communicator.rank:
                raise ValueError(f"rank {source} cannot be the source: there is no such task")
            # and, just as in the parallel case, it must have brought a matrix
            if matrix is None:
                raise TypeError("the source task must supply a matrix to scatter")
            # fill me with the whole of it
            return self.copy(matrix)
        # scatter; the source passes its own matrix, everybody else passes nothing, and the
        # extension fills me with my block of rows
        gsl.scatterMatrix(communicator, source, self, matrix)
        # and return me
        return self

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

    @property
    def elements(self):
        """
        Iterate over all my elements
        """
        # i'm already accessible as an iterator
        yield from self
        # all done
        return

    # initialization
    def fill(self, value):
        """
        Set all my elements to {value}, which may be a scalar or an iterable in row-major order
        """
        # attempt to read {value} as a single number
        try:
            # which the extension spreads across all my cells
            return gsl.Matrix.fill(self, float(value))
        # if it is not a number
        except TypeError:
            # take it as an iterable, one entry per cell, in row-major order
            for index, entry in zip(itertools.product(*map(range, self.shape)), value):
                # deposited in turn
                self.set(index, float(entry))
        # all done
        return self

    def view(self, start, shape):
        """
        Build a view to my data anchored at {start} with the given {shape}
        """
        # access the view object
        from .MatrixView import MatrixView

        # build one and return it
        return MatrixView(matrix=self, start=start, shape=shape)

    # file i/o over {pyre} paths
    def load(self, filename, binary=None):
        """
        Read my values from {filename}

        This method attempts to distinguish between text and binary representations of the
        data, based on the parameter {binary}, or the {filename} extension if it is absent
        """
        # if the caller asked for binary mode
        if binary is True:
            # pick the binary representation
            return self.read(filename)
        # if the caller asked for ascii mode
        if binary is False:
            # pick ascii
            return self.scanf(filename)
        # otherwise, a {.bin} extension means binary
        if filename.suffix == ".bin":
            # go binary
            return self.read(filename)
        # anything else is ascii
        return self.scanf(filename)

    def save(self, filename, binary=None, format=defaultFormat):
        """
        Write my values to {filename}

        This method attempts to distinguish between text and binary representations of the
        data, based on the parameter {binary}, or the {filename} extension if it is absent
        """
        # if the caller asked for binary mode
        if binary is True:
            # pick the binary representation
            return self.write(filename)
        # if the caller asked for ascii mode
        if binary is False:
            # pick ascii
            return self.printf(filename=filename, format=format)
        # otherwise, a {.bin} extension means binary
        if filename.suffix == ".bin":
            # go binary
            return self.write(filename)
        # anything else is ascii
        return self.printf(filename=filename, format=format)

    def read(self, filename):
        """
        Read my values from the binary file {filename}
        """
        # hand the path to the extension as a string
        return self.fread(str(filename.path))

    def write(self, filename):
        """
        Write my values to the binary file {filename}
        """
        # hand the path to the extension as a string
        return self.fwrite(str(filename.path))

    def scanf(self, filename):
        """
        Read my values from the text file {filename}
        """
        # hand the path to the extension as a string
        return self.fscanf(str(filename.path))

    def printf(self, filename, format=defaultFormat):
        """
        Write my values to the text file {filename}, using the given {format}
        """
        # build the c format specifier, and hand the path over as a string
        return self.fprintf(str(filename.path), "%" + format + "e")

    def print(self, format="{:+13.4e}", indent="", interactive=True):
        """
        Print my values using the given {format}
        """
        # initialize the display
        lines = []
        # for each row
        for i in range(self.rows):
            # initialize the line
            fragments = []
            # print the left margin: a '[[' on the first row, nothing on the others
            fragments.append("{}{}".format(indent, "[[" if i == 0 else "  "))
            # the row entries
            for j in range(self.columns):
                fragments.append(format.format(self[i, j]))
            # the right margin
            fragments.append("{}".format("]]" if i == self.rows - 1 else "  "))
            # add the line to the pile
            lines.append(" ".join(fragments))

        # if we are in interactive mode
        if interactive:
            # print all this out
            print("\n".join(lines))

        # all done
        return lines

    def random(self, pdf):
        """
        Fill me with random numbers using the probability distribution {pdf}
        """
        # the {pdf} knows how to do this
        return pdf.matrix(matrix=self)

    def clone(self):
        """
        Allocate a new matrix and initialize it with my values
        """
        # a fresh matrix of my shape, filled with my values
        return type(self)(shape=self.shape).copy(self)

    # slicing
    def getRow(self, index):
        """
        Return the {index}th row as a new vector
        """
        # allocate a vector of my width
        v = self.vector(shape=self.columns)
        # have the extension copy the row into it
        gsl.Matrix.getRow(self, int(index), v)
        # and return it
        return v

    def getColumn(self, index):
        """
        Return the {index}th column as a new vector
        """
        # allocate a vector of my height
        v = self.vector(shape=self.rows)
        # have the extension copy the column into it
        gsl.Matrix.getColumn(self, int(index), v)
        # and return it
        return v

    def setRow(self, index, v):
        """
        Set the {index}th row to the contents of the vector {v}
        """
        # coerce the index and hand off to the extension
        return gsl.Matrix.setRow(self, int(index), v)

    def setColumn(self, index, v):
        """
        Set the {index}th column to the contents of the vector {v}
        """
        # coerce the index and hand off to the extension
        return gsl.Matrix.setColumn(self, int(index), v)

    # eigensystems
    def symmetricEigensystem(self, order=gsl.EigenOrder.valueAscending):
        """
        Compute my eigenvalues and eigenvectors, assuming i am a real symmetric matrix
        """
        # allocate the vector the eigenvalues will fill
        λ = self.vector(shape=self.rows)
        # and the matrix the eigenvectors will fill
        x = type(self)(shape=self.shape)
        # have the extension solve the eigenproblem into them
        self.eigenSymmetric(order, λ, x)
        # and return the pair
        return λ, x

    # statistics
    def mean(self, axis=None, out=None):
        """
        Compute the mean values of a matrix
        axis = None, 0, or 1, along which the mean are computed
        """
        # check axis
        if axis is not None and axis != 0 and axis != 1:
            raise IndexError("axis is out of range")
        # check whether output vector is already allocated
        if out is None:
            # mean, sd over flattened matrix
            if axis is None:
                mean = self.vector(shape=1)
            # mean, sd along row
            elif axis == 0:
                mean = self.vector(shape=self.columns)
            # mean, sd along column
            elif axis == 1:
                mean = self.vector(shape=self.rows)
        else:
            # use pre-allocated vectors
            mean = out
            # assuming correct dimension, skip error checking

        # call gsl function
        gsl.stats_matrix_mean(self, axis, mean)

        # return the result
        return mean

    def mean_sd(self, axis=None, out=None, sample=True):
        """
        Compute the mean values of matrix
        axis: int or None
             axis along which the means are computed. None for all elements
        out: tuple of two vectors (mean, sd)
             vector size is 1 (axis=None),  columns(axis=0), rows(axis=1)
        sample: True or False
             when True, the sample standard deviation is computed 1/(N-1)
             when False, the population standard deviation is computed 1/N
        """
        # check axis
        if axis is not None and axis != 0 and axis != 1:
            raise IndexError("axis is out of range")

        if out is None:
            # mean, sd over flattened matrix
            if axis is None:
                mean = self.vector(shape=1)
                sd = self.vector(shape=1)
            # mean, sd along row
            elif axis == 0:
                mean = self.vector(shape=self.columns)
                sd = self.vector(shape=self.columns)
            # mean, sd along column
            elif axis == 1:
                mean = self.vector(shape=self.rows)
                sd = self.vector(shape=self.rows)
        else:
            # use pre-allocated vectors
            mean, sd = out
            # assuming correct dimension, skip error checking

        # call gsl function
        if sample:
            gsl.stats_matrix_mean_sd(self, axis, mean, sd)
        else:
            gsl.stats_matrix_mean_std(self, axis, mean, sd)

        # return (mean, sd)
        return mean, sd

    def std(self, axis=None, sample=False):
        """
        Compute the standard deviation of a matrix
        """
        mean, sd = self.mean_sd(axis=axis, out=None, sample=sample)
        return sd

    def ndarray(self, copy=False):
        """
        Return a numpy array over my data: a view that shares my storage when {copy} is False,
        or an independent copy when {copy} is True
        """
        # numpy reads me through the buffer protocol the extension exposes
        import numpy

        # a copy when asked, a zero-copy view otherwise
        return numpy.array(self) if copy else numpy.asarray(self)

    # meta methods
    def __init__(self, shape, **kwds):
        # let the extension allocate my storage; {shape} is its to consume, so the superclass
        # gets it along with everything else
        super().__init__(shape=tuple(map(int, shape)), **kwds)
        # all done
        return

    # container support
    def __iter__(self):
        """
        Iterate over all my elements in row-major order
        """
        # go over all index pairs
        for index in itertools.product(*map(range, self.shape)):
            # grab the value
            yield self.get(index)
        # all done
        return

    def __contains__(self, value):
        # the extension scans faster than a python loop
        return self.contains(value)

    def __getitem__(self, index):
        # get and return the element at the {row, column} {index}
        return self.get(index)

    def __setitem__(self, index, value):
        # set the element at the {row, column} {index}
        return self.set(index, value)

    # comparisons
    def __eq__(self, other):
        # type check
        if type(self) is not type(other):
            return NotImplemented
        # hand the request off to the extension
        return self.equal(other)

    def __ne__(self, other):
        return not (self == other)

    # in-place arithmetic
    def __iadd__(self, other):
        """
        In-place addition with the elements of {other}
        """
        # if other is a matrix
        if isinstance(other, Matrix):
            # do matrix-matrix addition
            self.add(other)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do constant addition
            self.shift(float(other))
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented

    def __isub__(self, other):
        """
        In-place subtraction with the elements of {other}
        """
        # if other is a matrix
        if isinstance(other, Matrix):
            # do matrix-matrix subtraction
            self.sub(other)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do constant subtraction
            self.shift(-float(other))
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented

    def __imul__(self, other):
        """
        In-place multiplication with the elements of {other}
        """
        # if other is a matrix
        if isinstance(other, Matrix):
            # do matrix-matrix multiplication
            self.mul(other)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do scaling by constant
            self.scale(float(other))
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented

    def __itruediv__(self, other):
        """
        In-place addition with the elements of {other}
        """
        # if other is a matrix
        if isinstance(other, Matrix):
            # do matrix-matrix division
            self.div(other)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do scaling by constant
            self.scale(1 / float(other))
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented


# end of file
