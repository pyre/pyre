# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from . import libgsl as gsl  # the extension


# the class declaration
class Permutation(gsl.Permutation):
    """
    A permutation of the integers [0, n)

    The permutation itself -- its storage, its operations, its validity -- is the extension's;
    this subclass adds the python indexing and iteration protocols
    """

    # container support
    def __iter__(self):
        """
        Iterate over the permutations in my sequence, starting from me
        """
        # as long as {next} succeeds
        while self.next():
            # the step happened in place, so i am the next one
            yield self
        # no more
        return

    def __getitem__(self, index):
        """
        Return the value at {index}, honouring negative indices
        """
        # reflect a negative index about the end
        if index < 0:
            index += self.shape
        # bounds check
        if index < 0 or index >= self.shape:
            # and complain
            raise IndexError(f"permutation index {index} out of range")
        # hand off to the extension
        return self.get(index)


# end of file
