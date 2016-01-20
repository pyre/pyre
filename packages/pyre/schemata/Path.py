# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# support
from .. import primitives
# superclass
from .Schema import Schema


# my declaration
class Path(Schema):
    """
    A type declarator for paths
    """


    # constants
    typename = 'path' # the name of my type

    # magic values
    cwd = primitives.path.cwd
    root = primitives.path.root
    home = primitives.path.home()


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a path
        """
        # respect None
        if value is None:
            # by leaving it alone
            return None

        # perhaps it is already a path
        if isinstance(value, primitives.path):
            # in which case, just leave it alone
            return value

        # the rest assume {value} is a string; if it isn't
        if not isinstance(value, str):
            # build the error message
            msg = "cannot cast {!r} into a path".format(value)
            # and complain
            raise self.CastingError(value=value, description=msg)

        # strip
        value = value.strip()
        # check for "none"
        if value.lower() == "none":
            # do as told
            return None

        # cast {value} into a path
        return primitives.path(value)


# end of file
