# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import numbers
from . import libgsl as gsl  # the extension


# the class declaration
class Vector(gsl.Vector):
    """
    A vector of doubles

    The storage, the buffer protocol, the views, and the elementwise operations are the
    extension's; everything that reads more naturally in python -- the file i/o over {pyre}
    paths, the slicing, the arithmetic operators -- lives here
    """

    # types
    from .Permutation import Permutation as permutation

    # constants
    defaultFormat = "+16.7"

    # class methods
    # mpi support
    @classmethod
    def bcast(cls, vector=None, communicator=None, source=0):
        """
        Broadcast the given {vector} from {source} to all tasks in {communicator}
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi

            # use the world by default
            communicator = mpi.world
        # with a single process there is nobody to send to, and the source already holds the
        # answer; this is also the only path there is on a machine with no mpi, where the
        # extension was built without {bcastVector}
        if communicator.size == 1:
            # the lone process is the only one that can be the source
            if source != communicator.rank:
                raise ValueError(f"rank {source} cannot be the source: there is no such task")
            # and, just as in the parallel case, it must have brought a vector
            if vector is None:
                raise TypeError("the source task must supply a vector to broadcast")
            # which is already the answer
            return vector
        # get the vector capsule
        data = None if vector is None else vector.data
        # broadcast the data
        capsule, shape = gsl.bcastVector(communicator, source, data)
        # the source already owns the vector it broadcast, so it hands that back untouched;
        # rewrapping the capsule it borrows would hand its storage to a second owner
        if communicator.rank == source:
            return vector
        # everybody else dresses up the fresh storage they received as a vector
        result = cls(shape=shape, data=capsule)
        # and returns it
        return result

    @classmethod
    def collect(cls, vector, communicator=None, destination=0):
        """
        Gather the data in {vector} from each task in {communicator} into one big vector
        available at the {destination} task
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi

            # use the world by default
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
            return vector.clone()
        # gather the data
        result = gsl.gatherVector(communicator, destination, vector.data)
        # if i am not the destination task, nothing further to do
        if communicator.rank != destination:
            return
        # otherwise, unpack the result
        data, shape = result
        # dress up the result as a vector
        result = cls(shape=shape, data=data)
        # and return it
        return result

    def excerpt(self, communicator=None, source=0, vector=None):
        """
        Scatter {vector} held by the task {source} among all tasks in {communicator} and fill me
        with the partition values. Only {source} has to provide a {vector}; the other tasks can
        use the default value.
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi

            # use the world by default
            communicator = mpi.world
        # with a single process there is nobody to scatter to; my partition is all of {vector}
        if communicator.size == 1:
            # the lone process is the only one that can be the source
            if source != communicator.rank:
                raise ValueError(f"rank {source} cannot be the source: there is no such task")
            # and, just as in the parallel case, it must have brought a vector
            if vector is None:
                raise TypeError("the source task must supply a vector to scatter")
            # fill me with the whole of it
            return self.copy(vector)
        # get the vector capsule
        data = None if vector is None else vector.data
        # scatter the data
        gsl.scatterVector(communicator, source, self.data, data)
        # and return me
        return self

    # public data
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
        Set all my elements to {value}, which may be a scalar or an iterable of my shape
        """
        # attempt to read {value} as a single number
        try:
            # which the extension spreads across all my cells
            return gsl.Vector.fill(self, float(value))
        # if it is not a number
        except TypeError:
            # take it as an iterable, one entry per cell
            for index, entry in enumerate(value):
                # deposited in turn
                self.set(index, float(entry))
        # all done
        return self

    def random(self, pdf):
        """
        Fill me with random numbers using the probability distribution {pdf}
        """
        # the {pdf} knows how to do this
        return pdf.vector(vector=self)

    def clone(self):
        """
        Allocate a new vector and initialize it with my values
        """
        # a fresh vector of my shape, filled with my values
        return type(self)(shape=self.shape).copy(self)

    def view(self, start, shape):
        """
        Build a view of me from {start} to {start+shape}
        """
        # access the view object
        from .VectorView import VectorView

        # build and return one
        return VectorView(vector=self, start=start, shape=shape)

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
        # build the line
        line = " ".join([f"{indent}["] + [format.format(value) for value in self] + ["]"])
        # if we are in interactive mode
        if interactive:
            # print it out
            print(line)
        # all done
        return line

    def sortIndirect(self):
        """
        Construct the permutation that would sort me in ascending order
        """
        # allocate the permutation the sort will fill
        p = self.permutation(shape=self.shape)
        # have the extension fill it, leaving me untouched
        self.sortIndex(p)
        # and return it
        return p

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
    def __init__(self, shape, data=None, **kwds):
        # let the extension allocate my storage, or adopt the capsule {data} carries; {shape}
        # and {data} are its to consume, so the superclass gets them along with everything else
        super().__init__(shape=int(shape), data=data, **kwds)
        # all done
        return

    # container support
    def __iter__(self):
        # for each valid value of the index
        for index in range(len(self)):
            # produce the corresponding element
            yield self.get(index)
        # no more
        return

    def __contains__(self, value):
        # the extension scans faster than a python loop
        return self.contains(value)

    def __getitem__(self, index):
        # a slice yields a generator over the described values
        if type(index) is slice:
            # hand it off
            return self._slice(index)
        # otherwise, {index} must be convertible into an integer
        try:
            # so try
            index = int(index)
        # if it is not
        except TypeError:
            # we are out of ideas
            raise TypeError(f"vector indices must be integers, not {type(index).__name__}")
        # reflect a negative index about the end
        if index < 0:
            index += len(self)
        # and hand off to the extension
        return self.get(index)

    def __setitem__(self, index, value):
        # a slice assigns from a compatible iterable
        if type(index) is slice:
            # attempt to
            try:
                # iterate over the slice and the values together
                for i, v in zip(range(*index.indices(self.shape)), value):
                    # setting the corresponding cell
                    self.set(i, v)
            # if {value} was not iterable
            except TypeError:
                # say so
                raise TypeError("can only assign an iterable")
            # all done
            return
        # otherwise, {index} must be convertible into an integer
        try:
            # so try
            index = int(index)
        # if it is not
        except TypeError:
            # we are out of ideas
            raise TypeError(f"vector indices must be integers, not {type(index).__name__}")
        # reflect a negative index about the end
        if index < 0:
            index += len(self)
        # and set the cell
        self.set(index, value)
        # all done
        return

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
        # if other is a vector
        if isinstance(other, Vector):
            # do vector-vector addition
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
        # if other is a vector
        if isinstance(other, Vector):
            # do vector-vector subtraction
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
        # if other is a vector
        if isinstance(other, Vector):
            # do vector-vector multiplication
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
        In-place division with the elements of {other}
        """
        # if other is a vector
        if isinstance(other, Vector):
            # do vector-vector division
            self.div(other)
            # and return
            return self
        # if other is a number
        if isinstance(other, numbers.Number):
            # do scaling by the reciprocal
            self.scale(1 / float(other))
            # and return
            return self
        # otherwise, let the interpreter know
        raise NotImplemented

    # implementation details
    def _slice(self, index):
        """
        Build a generator that yields the values described in the {index}
        """
        # iterate over the indices
        for i in range(*index.indices(self.shape)):
            # yield the corresponding value
            yield self.get(i)
        # all done
        return


# end of file
