# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# class declaration
class Recognizer:
    """
    Abstract base class for filesystem entry recognition
    """

    # interface
    def recognize(self, entry):
        """
        Given a filesystem {entry}, build a filesystem specific structure and decorate it with
        the available metadata
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'recognize'"
        )


# end of file
