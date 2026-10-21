# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc  # for container identification

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
        # a map is not a path, even though the constructor would take its keys as the parts of
        # one; in a configuration file, it is most likely a macro that was not quoted
        if isinstance(value, collections.abc.Mapping):
            # so complain
            raise self.CastingError(value=value, description=self.complaint)
        # attempt to
        try:
            # let the constructor do its job; it knows paths, strings, and iterables of them
            path = primitives.path(value)
        # if it can't make sense of {value}
        except TypeError as error:
            # complain
            raise self.CastingError(value=value, description=self.complaint, error=error)
        # if all goes well, return the {path}
        return path

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

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a path
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onPath
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)


# end of file
