# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# declaration
class Schema:
    """
    The base class for type declarators
    """

    # exception
    from .exceptions import CastingError

    # constants
    typename = "identity"
    isContainer = False

    # public data
    @property
    def default(self):
        """
        Grant access to my default value
        """
        # easy enough
        return self._default

    @default.setter
    def default(self, value):
        """
        Save {value} as my default
        """
        # also easy
        self._default = value
        # all done
        return

    # interface
    def process(self, value, **kwds):
        """
        Walk {value} through all steps necessary to become acceptable
        """
        # by default, punt to {coerce}
        return self.coerce(value=value, **kwds)

    def coerce(self, value, **kwds):
        """
        Convert the given value into a python native object
        """
        # just leave it alone
        return value

    def string(self, value):
        """
        Render value as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # my value knows
        return str(value)

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # by default, let the raw value through; the schemata that are not JSON representable
        # must override to provide something suitable
        return value

    def render(self, renderer, value, incognito=False, **kwds):
        """
        Render {value} using {renderer}
        """
        # render value
        entry = self.string(value)
        # if i'm incognito
        if incognito:
            # render just my value
            yield renderer.value(value=entry)
        # otherwise
        else:
            # render both my name and the value
            yield renderer.trait(name=self.name, value=entry)

        # all done
        return

    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my default value
        self._default = default
        # all done
        return


# end of file
