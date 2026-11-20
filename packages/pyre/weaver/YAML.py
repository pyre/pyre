# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the interpolation of configuration values, whose markers text must escape
from ..calc.Interpolation import Interpolation


# my declaration
class YAML:
    """
    A renderer of the values of schemata into the plain values of a yaml configuration file:
    {None}, truth values, numbers, strings, lists and tables with string keys

    The schemata identify themselves to me, and i reduce each value to the plainest form that its
    schema reads back when the file is loaded: truth values and numbers stay as they are,
    containers keep their shape, and everything else becomes the text of its schema. The file is
    interpolated when it is read, so every text i write has its braces escaped
    """

    # interface
    def render(self, schema, value):
        """
        Reduce {value}, a value of {schema}, to plain values
        """
        # {None} is {null}, whatever the schema
        if value is None:
            # so leave it alone
            return None
        # otherwise, let the schema say what it is
        return schema._pyre_identify(authority=self, value=value)

    # the values taken as they are, which can be anything at all
    def _pyre_onSchema(self, schema, value, **kwds):
        """
        Reduce {value}, which no schema has interpreted, to plain values
        """
        # walk it
        return self._raw(value=value)

    # values that yaml holds as they are
    def _pyre_onNumber(self, schema, value, **kwds):
        """
        Truth values, integers and floats
        """
        # are scalars in yaml too
        return value

    def _pyre_onString(self, schema, value, **kwds):
        """
        Strings, and the values of environment variables
        """
        # are text, which must survive interpolation
        return Interpolation.escape(value)

    # values that travel as the text of their schema
    def _pyre_onBytes(self, schema, value, **kwds):
        """
        Strings of octets
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onCell(self, schema, value, **kwds):
        """
        The types of the cells of grids
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onChannel(self, schema, value, **kwds):
        """
        Channels to other processes
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onComplex(self, schema, value, **kwds):
        """
        Complex numbers, which yaml has no number for
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onComponent(self, schema, value, **kwds):
        """
        Components
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onDate(self, schema, value, **kwds):
        """
        Dates
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Fixed point numbers, which a yaml float would round
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onDimensional(self, schema, value, **kwds):
        """
        Quantities with units
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onEnum(self, schema, value, **kwds):
        """
        Members of enumerations
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onFraction(self, schema, value, **kwds):
        """
        Fractions, which a yaml float would round
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onINet(self, schema, value, **kwds):
        """
        Internet addresses
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onInputStream(self, schema, value, **kwds):
        """
        Streams to read from
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onOutputStream(self, schema, value, **kwds):
        """
        Streams to write to
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onPath(self, schema, value, **kwds):
        """
        Filesystem paths
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Times of day
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Moments in time
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onURI(self, schema, value, **kwds):
        """
        Resource identifiers
        """
        # as their text
        return self._text(schema=schema, value=value)

    def _pyre_onUUID(self, schema, value, **kwds):
        """
        Universally unique identifiers
        """
        # as their text
        return self._text(schema=schema, value=value)

    # containers
    def _pyre_onSequence(self, schema, value, **kwds):
        """
        Lists, sets, tuples and the other sequences
        """
        # become lists of their entries, each rendered the way the schema of the entries says
        return [self.render(schema=schema.schema, value=entry) for entry in value]

    def _pyre_onArray(self, schema, value, **kwds):
        """
        Arrays
        """
        # become nested lists, as deep as the array
        return self._level(schema=schema.schema, level=value)

    def _pyre_onMapping(self, schema, value, **kwds):
        """
        Maps from strings to the values of a schema
        """
        # become tables, with each value rendered the way the schema of the entries says
        return {
            str(key): self.render(schema=schema.schema, value=item) for key, item in value.items()
        }

    # implementation details
    def _text(self, schema, value):
        """
        Render {value} as the text of {schema}, escaped so that it survives interpolation
        """
        # get the text and escape it
        return Interpolation.escape(schema.string(value))

    def _level(self, schema, level):
        """
        Render {level}, an entry or a level of an array whose entries are values of {schema}
        """
        # a level is a tuple of entries or of deeper levels
        if isinstance(level, tuple):
            # each of which is rendered the same way
            return [self._level(schema=schema, level=entry) for entry in level]
        # and anything else is an entry
        return self.render(schema=schema, value=level)

    def _raw(self, value):
        """
        Reduce {value}, which no schema has interpreted, to plain values
        """
        # text
        if isinstance(value, str):
            # must survive interpolation
            return Interpolation.escape(value)
        # the other scalars yaml holds as they are
        if value is None or isinstance(value, (bool, int, float)):
            # stay as they are
            return value
        # tables
        if isinstance(value, dict):
            # keep their shape, with string keys
            return {str(key): self._raw(value=item) for key, item in value.items()}
        # sequences of every kind
        if isinstance(value, (list, tuple, set, frozenset)):
            # become lists
            return [self._raw(value=item) for item in value]
        # and anything else becomes its text, which must survive interpolation
        return Interpolation.escape(str(value))


# end of file
