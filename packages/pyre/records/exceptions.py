# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

# superclass
from ..framework.exceptions import FrameworkError


# the local base
class RecordError(FrameworkError):
    """
    The base class of all exceptions raised by this package
    """

    # implementation details
    @staticmethod
    def phrase(noun: str, names) -> str:
        """
        Phrase {names} as things of kind {noun}, as in "field 'a'" or "fields 'a', 'b'"
        """
        # quote the names
        quoted = ", ".join(f"'{name}'" for name in names)
        # one of them, or several
        return f"{noun} {quoted}" if len(names) == 1 else f"{noun}s {quoted}"


# something's wrong with an input source
class SourceSpecificationError(RecordError):
    """
    Exception raised when a reader of records is given no source to read from
    """

    # public data
    description = "invalid input source specification"


# a field that matches more than one column of a source
class AmbiguousColumnError(RecordError):
    """
    Exception raised when a field of a record matches more than one column of a source
    """

    # public data
    description = "field '{0.field}' of '{0.name}' matches {0.columns}"

    # meta-methods
    def __init__(self, record, field, columns, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the record
        self.record = record
        # by name
        self.name = record.pyre_name
        # the field, by name
        self.field = field.name
        # and the columns it matches, as pairs of their offsets and names
        self.matches = tuple(columns)
        # phrased for the description, counting the columns from one
        self.columns = "more than one column: " + ", ".join(
            f"'{header}' (column {offset + 1})" for offset, header in self.matches
        )
        # all done
        return


# a row with too few or too many values
class RowLengthError(RecordError):
    """
    Exception raised when a row does not hold as many values as a record takes
    """

    # public data
    description = "a row of '{0.name}' has {0.given}, instead of {0.expected}"

    # meta-methods
    def __init__(self, record, expected: int, given: int, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the record
        self.record = record
        # by name
        self.name = record.pyre_name
        # and the two counts, phrased as amounts of values
        self.expected = self.values(count=expected)
        self.given = self.values(count=given)
        # all done
        return

    # implementation details
    @staticmethod
    def values(count: int) -> str:
        """
        Phrase {count} as an amount of values
        """
        # one value, or several
        return f"{count} value" if count == 1 else f"{count} values"


# keywords that name no field
class UnknownFieldError(RecordError):
    """
    Exception raised when a record is built from keywords that name none of its fields
    """

    # public data
    description = "'{0.name}' has no {0.fields}"

    # meta-methods
    def __init__(self, record, names, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the record
        self.record = record
        # by name
        self.name = record.pyre_name
        # the names that matched nothing
        self.names = tuple(names)
        # phrased for the description
        self.fields = self.phrase(noun="field", names=self.names)
        # all done
        return


# keywords that name fields whose values are computed
class ComputedFieldError(RecordError):
    """
    Exception raised when a record is built from keywords that name fields whose values are
    computed from other fields
    """

    # public data
    description = "'{0.name}' computes its {0.fields}, and takes no value for {0.pronoun}"

    # meta-methods
    def __init__(self, record, names, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the record
        self.record = record
        # by name
        self.name = record.pyre_name
        # the names of the computed fields
        self.names = tuple(names)
        # phrased for the description
        self.fields = self.phrase(noun="field", names=self.names)
        # along with the pronoun that refers to them
        self.pronoun = "it" if len(self.names) == 1 else "them"
        # all done
        return


# end of file
