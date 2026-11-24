# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

# the base of the exceptions the framework raises
from ..framework.exceptions import FrameworkError

# db api 2.0 compliant exception hierarchy
# not my first choice for a classification strategy, but there you go...


class Diagnosed(FrameworkError):
    """
    The base of the hierarchy, and the carrier of whatever the back end had to say

    Postgres names every condition it raises with a five character SQLSTATE, and reports the
    object at fault alongside it. All of that arrives here, so that a caller need never read
    english to find out which constraint was violated, or whether a failure is worth retrying.
    A back end that names its conditions in a vocabulary of its own, as sqlite does with its
    result codes, puts that name in {code}
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
        internalQuery="",
        internalPosition=0,
        context="",
        schema="",
        table="",
        column="",
        datatype="",
        constraint="",
        code="",
        values=None,
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
        # the statement a function on the server ran, when the failure happened inside one
        self.internalQuery = internalQuery
        self.internalPosition = internalPosition
        # and where on the server that was: the function, the trigger, the cursor
        self.context = context
        # the object the complaint is about, which is how two unique indices are told apart
        self.schema = schema
        self.table = table
        self.column = column
        self.datatype = datatype
        self.constraint = constraint
        # the name the back end gives the condition in its own vocabulary, when it has one
        self.code = code
        # and the values of the slots of the run of a prepared statement that provoked it, when
        # it was one of many
        self.values = values

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
    other indications that the implementation engines have carried out a request in a perhaps
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


class LockError(OperationalError):
    """
    Exception raised when a lock is held by another session, and the session that asked for it
    would not wait, or gave up waiting
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
