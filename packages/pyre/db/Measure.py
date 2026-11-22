# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the special values {NULL} and {DEFAULT}
from . import literals

# superclass
from .. import records
from .. import schemata


# declaration
@schemata.typed
class Measure(records.measure):
    """
    The base class for table field descriptors
    """

    # types
    from .ForeignKey import ForeignKey as foreign

    # field decorations
    def setDefault(self, value):
        """
        Set a new default value
        """
        # install the new default
        self.default = value
        # enable chaining
        return self

    def primary(self):
        """
        Mark a field as a primary key
        """
        # mark
        self._primary = True
        # primary keys do not get default values
        self.default = None
        # and return
        return self

    def unique(self):
        """
        Mark a field as containing values that are unique across the table rows
        """
        # mark
        self._unique = True
        # and return
        return self

    def notNull(self):
        """
        Mark a field as not accepting a NULL value
        """
        # mark
        self._notNull = True
        # and return
        return self

    def references(self, **kwds):
        """
        Mark a field as a foreign key
        """
        # use the specification to create a field reference object and record it
        self._foreign = self.foreign(**kwds)
        # and return
        return self

    # the base class of the local mixins
    class measure:
        """
        The base class of the local mixins.

        Its purpose is to trap value coercion and skip it for the special values {NULL} and
        {DEFAULT} that show up as {literals} instances
        """

        # interface
        def coerce(self, value, **kwds):
            # the literals
            if value is literals.null or value is literals.default:
                # require no processing
                return value
            # for the rest, chain up...
            return super().coerce(value=value, **kwds)

    # mixins for the various supported types
    class bool(measure):
        """Mixin for booleans"""

        # public data
        decl = "BOOLEAN"  # SQL rendering of my type name

        # interface
        def sql(self, value):
            """SQL rendering of {value}"""
            # easy enough
            return "true" if value else "false"

    class bytes(measure):
        """
        Mixin for strings of octets
        """

        # public data
        decl = "BYTEA"  # SQL rendering of my type name

        # interface
        def sql(self, value):
            """
            SQL rendering of {value}
            """
            # the octets, as the hexadecimal digits the server reads them from
            return f"'\\x{self.coerce(value=value).hex()}'"

    class date(measure):
        """
        Mixin for dates
        """

        # public data
        decl = "DATE"  # SQL rendering of my type name

        # interface
        def sql(self, value):
            """
            SQL rendering of {value}
            """
            # the text of the date, quoted
            return f"'{self.string(self.coerce(value=value))}'"

    class decimal(measure):
        """Mixin for fixed point numbers"""

        # public data
        @property
        def decl(self):
            """SQL rendering of my type name"""
            # easy enough
            return "DECIMAL({}, {})".format(self.precision, self.scale)

        # interface
        def sql(self, value):
            """SQL rendering of {value}"""
            # convert the decimal into a string
            return str(value)

        # meta-methods
        def __init__(self, precision, scale, **kwds):
            # chain up
            super().__init__(**kwds)
            # save my parts
            self.scale = scale
            self.precision = precision
            # all done
            return

    class float(measure):
        """Mixin for floating point numbers"""

        # public data
        decl = "DOUBLE PRECISION"  # SQL rendering of my type name

        # interface
        def sql(self, value):
            """SQL rendering of my value"""
            # easy enough
            return str(value)

    class int(measure):
        """Mixin for integers"""

        # public data
        decl = "INTEGER"  # SQL rendering of my type name

        # interface
        def sql(self, value):
            """SQL rendering of my value"""
            # easy enough
            return str(value)

    class str(measure):
        """Mixin for strings"""

        # public data
        @property
        def decl(self):
            """SQL rendering of my type name"""
            # get my size
            size = self.maxlen
            # build a size dependent representation
            return "TEXT" if size is None else "VARCHAR({})".format(size)

        # interface
        def sql(self, value):
            """SQL rendering of my value"""
            # if the value is None
            if value is None:
                # convert it
                return "'None'"
            # otherwise, escape any embedded single quotes
            return "'{}'".format(value.replace("'", "''"))

        # meta-methods
        def __init__(self, maxlen=None, **kwds):
            # chain up
            super().__init__(**kwds)
            # save my size
            self.maxlen = maxlen
            # all done
            return

    class time(measure):
        """
        Mixin for times of day
        """

        # public data
        @property
        def decl(self):
            """
            SQL rendering of my type name
            """
            # a time of day carries its offset only when i insist that it has one
            return "TIME WITH TIME ZONE" if self.timezone is True else "TIME"

        # interface
        def sql(self, value):
            """
            SQL rendering of {value}
            """
            # the text of the time, quoted
            return f"'{self.string(self.coerce(value=value))}'"

    class timestamp(measure):
        """
        Mixin for moments in time
        """

        # public data
        @property
        def decl(self):
            """
            SQL rendering of my type name
            """
            # a moment carries its time zone only when i insist that it has one
            return "TIMESTAMP WITH TIME ZONE" if self.timezone is True else "TIMESTAMP"

        # interface
        def sql(self, value):
            """
            SQL rendering of {value}
            """
            # the text of the moment, quoted
            return f"'{self.string(self.coerce(value=value))}'"

    class uuid(measure):
        """
        Mixin for universally unique identifiers
        """

        # public data
        decl = "UUID"  # SQL rendering of my type name

        # interface
        def sql(self, value):
            """
            SQL rendering of {value}
            """
            # the canonical text of the identifier, quoted
            return f"'{self.string(self.coerce(value=value))}'"

    class array(measure):
        """
        Mixin for arrays, whose entries are values of another column type
        """

        # public data
        @property
        def decl(self):
            """
            SQL rendering of my type name
            """
            # the type of my entries, marked as an array; the server ignores the rank
            return f"{self.schema.decl}[]"

        # interface
        def sql(self, value):
            """
            SQL rendering of {value}
            """
            # build the array, whole or not at all, and render it level by level
            return self._level(level=self.coerce(value=value))

        # meta-methods
        def __init__(self, **kwds):
            # chain up
            super().__init__(**kwds)
            # my entries are rendered and declared by their own column type
            if not isinstance(self.schema, Measure):
                # so anything else is a mistake in the declaration
                self._firewall(
                    message=(
                        "the entries of an array column must be a column type, "
                        f"not {self.schema!r}"
                    )
                )
            # all done
            return

        # implementation details
        def _level(self, level):
            """
            Render {level}, an entry or a level of the array
            """
            # a level is a tuple of entries or of deeper levels
            if isinstance(level, tuple):
                # an empty one
                if not level:
                    # is the empty array, which takes the type of its column
                    return "'{}'"
                # the others list what they hold
                return "ARRAY[" + ", ".join(self._level(level=entry) for entry in level) + "]"
            # anything else is an entry, which its column type renders
            return self.schema.sql(value=level)

    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up; a column has a default only when it is given one
        super().__init__(default=default, **kwds)
        # all done
        return

    # sql rendering
    def decldefault(self):
        """
        Invoked by the SQL mill to create the declaration of the default value
        """
        # get my default value
        value = self.default
        # if one was not specified
        if value is None:
            # return an empty string
            return ""
        # build an SQL representation for the default value
        value = "NULL" if value is literals.null else self.sql(value)
        # render
        return " DEFAULT {}".format(value)

    # private data
    # the following markers interpret {None} as 'unspecified'
    _primary = None  # am i a primary key?
    _unique = None  # are my values unique across the rows of the table?
    _notNull = None  # do i refuse NULL as a value?
    _foreign = None  # foreign key: the {ForeignKey} that describes what i refer to


# end of file
