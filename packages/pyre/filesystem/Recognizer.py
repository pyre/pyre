# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Recognizer:
    """
    Abstract base class for filesystem entry recognition.
    """


    def recognize(self, entry):
        """
        The most basic file recognition: convert the name of a file into a File descendant
        and decorate it with all the metadata available.
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'recognize'".format(self))


# end of file 
