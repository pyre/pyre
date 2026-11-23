# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the special values {NULL} and {DEFAULT}
from . import literals

# superclass
from ... import records
from ... import schemata


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
        """
        Mixin for truth values
        """

    class bytes(measure):
        """
        Mixin for strings of octets
        """

    class date(measure):
        """
        Mixin for dates
        """

    class decimal(measure):
        """
        Mixin for fixed point numbers
        """

        # meta-methods
        def __init__(self, precision, scale, **kwds):
            # chain up
            super().__init__(**kwds)
            # the number of my digits
            self.precision = precision
            # and how many of them follow the point
            self.scale = scale
            # all done
            return

    class float(measure):
        """
        Mixin for floating point numbers
        """

        # meta-methods
        def __init__(self, bits=None, **kwds):
            # chain up
            super().__init__(**kwds)
            # my width in bits; {None} for the width the back end prefers
            self.bits = bits
            # all done
            return

    class int(measure):
        """
        Mixin for integers
        """

        # meta-methods
        def __init__(self, bits=None, **kwds):
            # chain up
            super().__init__(**kwds)
            # my width in bits; {None} for the width the back end prefers
            self.bits = bits
            # all done
            return

    class json(measure):
        """
        Mixin for json documents
        """

        # declaration decorations
        def verbatim(self):
            """
            Keep the text of my documents as it was written, rather than in the form the back end
            prefers
            """
            # mark
            self._verbatim = True
            # and return
            return self

        def asText(self):
            """
            Read my documents as their text, rather than as documents
            """
            # mark
            self._asText = True
            # and return
            return self

        # private data
        _verbatim = None  # do i keep the text of my documents as it was written?

    class str(measure):
        """
        Mixin for strings
        """

        # meta-methods
        def __init__(self, maxlen=None, **kwds):
            # chain up
            super().__init__(**kwds)
            # my maximum length; {None} for text of any length
            self.maxlen = maxlen
            # all done
            return

    class time(measure):
        """
        Mixin for times of day
        """

    class timestamp(measure):
        """
        Mixin for moments in time
        """

    class uuid(measure):
        """
        Mixin for universally unique identifiers
        """

    class array(measure):
        """
        Mixin for arrays, whose entries are values of another column type
        """

        # meta-methods
        def __init__(self, **kwds):
            # chain up
            super().__init__(**kwds)
            # my entries are values of a column type of their own
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

    # value processing
    def isNone(self, value):
        """
        Decide whether {value} stands for the absence of a value: in a column, only {None} does,
        and text is text, whatever it says
        """
        # easy enough
        return value is None

    # meta-methods
    def __init__(self, default=None, **kwds):
        # chain up; a column has a default only when it is given one
        super().__init__(default=default, **kwds)
        # all done
        return

    # private data
    # the following markers interpret {None} as 'unspecified'
    _primary = None  # am i a primary key?
    _unique = None  # are my values unique across the rows of the table?
    _notNull = None  # do i refuse NULL as a value?
    _foreign = None  # foreign key: the {ForeignKey} that describes what i refer to
    _asText = None  # am i read as my text?


# end of file
