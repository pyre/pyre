# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# externals
from . import gsl
# superclass
from .Matrix import Matrix


# declaration
class MatrixView(Matrix):
    """
    A view into the data of another matrix
    """


    # meta-methods
    def __init__(self, matrix, start, shape, **kwds):
        # adjust the parameters, just in case
        start = tuple(map(int, start))
        shape = tuple(map(int, shape))
        # store a reference to the underlying matrix so it lives long enough
        self.matrix = matrix
        # build the view
        self.view, data = gsl.matrix_view_alloc(matrix.data, start, shape)
        # chain up
        super().__init__(shape=shape, data=data, **kwds)
        # all done
        return


# end of file
