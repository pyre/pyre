# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

from ..framework.exceptions import FrameworkError

# db api 2.0 compliant exception hierarchy
# not my first choice for a classification strategy, but there you go...


class Diagnosed(FrameworkError):
    """
    The base of the hierarchy, and the carrier of whatever the back end had to say

    Postgres names every condition it raises with a five character SQLSTATE, and reports the
    object at fault alongside it. All of that arrives here, so that a caller need never read
    english to find out which constraint was violated, or whether a failure is worth retrying
    """

    # public data
    # note that the explanation is interpolated into this template rather than becoming one; a
    # message from the server may well contain braces, and {str} would choke on it otherwise
    description = "{0.diagnostic}"

    # meta-methods
    def __init__(
        self,
        diagnostic="",
        sqlstate="",
        command="",
        severity="",
        detail="",
        hint="",
        position=0,
        schema="",
        table="",
        column="",
        datatype="",
        constraint="",
        **kwds,
    ):
        # chain up
        super().__init__(**kwds)

        # the one line explanation the server wrote, for a human
        self.diagnostic = diagnostic
        # the five character code that names the condition; the only portable part of a complaint
        self.sqlstate = sqlstate
        # the statement that provoked it
        self.command = command
        # how bad the server thinks this is
        self.severity = severity
        # the elaborations, each of which is empty when the server chose not to supply it
        self.detail = detail
        self.hint = hint
        self.position = position
        # and the object the complaint is about, which is how two unique indices are told apart
        self.schema = schema
        self.table = table
        self.column = column
        self.datatype = datatype
        self.constraint = constraint

        # all done
        return

    # interface
    @property
    def category(self):
        """
        The first two characters of my {sqlstate}, which name the family of the condition
        """
        # the first two of the five, when the server sent five
        return self.sqlstate[:2]


class Warning(Diagnosed):
    """
    Exception raised for important warnings, such as data truncation, loss of precision and
    other idications that the implementation engines have carried out a request in a perhaps
    incorrect way
    """


class Error(Diagnosed):
    """
    Base class for all exceptions that are raised by this module to indicate an unrecoverable
    error
    """


class InterfaceError(Error):
    """
    Base class for exceptions raised by the database client code, not the database back end
    """


class DatabaseError(Error):
    """
    Base class for exceptions raised by the database back end
    """


class DataError(DatabaseError):
    """
    Exception raised when a data processing error occurs
    """


class OperationalError(DatabaseError):
    """
    An exception that indicates environmental problems that are generally not related to the
    program itself
    """


class IntegrityError(DatabaseError):
    """
    Exception raised when an operation violates the referential integrity of the data store
    """


class InternalError(DatabaseError):
    """
    Exception raised when the back end reports an internal error
    """


class ProgrammingError(DatabaseError):
    """
    Exception raised when there is a problem with the SQL statement being executed
    """

    # public data
    # a syntax error is meaningless without the statement that provoked it
    description = "while executing {0.command!r}: {0.diagnostic}"


class NotSupportedError(DatabaseError):
    """
    Exception raised when a method or database API was used that is not supported by the
    database client
    """


# end of file
