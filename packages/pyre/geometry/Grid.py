# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


class Grid(list):
    """
    A logically Cartesian grid implemented as a list with a custom indexing function
    """


    # meta-methods
    def __init__(self, shape, *args, **kwds):
        # chain up
        super().__init__(*args, **kwds)
        # save my dimensions
        self.shape = tuple(shape)
        # all done
        return


    def __getitem__(self, index):
        """
        Support structured access to the cells
        """
        # attempt to
        try:
            # realize the index
            index = self.project(index)
        # if this fails
        except TypeError:
            # convert it into an integer
            index = int(index)

        # chain up
        return super().__getitem__(index)


    # implementation details
    def project(self, index):
        """
        Convert the {index} into an offset
        """
        # to start off
        offset = 0
        product = 1
        # loop over the indices
        for i, s in zip(index, self.shape):
            # yield the current addend
            offset += i*product
            # adjust the coefficient
            product *= s
        # all done
        return offset


# end of file
