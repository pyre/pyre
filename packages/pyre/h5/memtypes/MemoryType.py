# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


class MemoryType:
    """
    A memory type specification
    """

    # data
    @property
    def tag(self):
        """
        Generate my type tag
        """
        # use my class name as the tag; this is currently consistent with the {pyre.memory}
        # bindings, so it can be interpolated into class names when requesting specific
        # template instantiations
        return type(self).__name__


# end of file
