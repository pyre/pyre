# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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
    typename = "path"  # the name of my type
    complaint = "cannot cast {0.value!r} into a path"

    # magic values
    cwd = primitives.path.cwd
    root = primitives.path.root
    home = primitives.path.home()

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a path
        """
        # perhaps it is already a path
        if isinstance(value, primitives.path):
            # in which case, just leave it alone
            return value

        # the rest assume {value} is a string; if it isn't
        if not isinstance(value, str):
            # complain
            raise self.CastingError(value=value, description=self.complaint)

        # cast {value} into a path
        return primitives.path(value)

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # metamethods
    def __init__(self, default=object, **kwds):
        # adjust the default; carefully, so we don't all end up using the same global container
        # checking for {None} is not appropriate here; the user may want {None} as the default
        # value; we need a way to know that {default} was not supplied: use a TYPE (in this
        # case object) as the marker
        default = primitives.path() if default is object else default
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file
