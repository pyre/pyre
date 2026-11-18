#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the server's own name for what went wrong decides which exception reaches
    python, and that the exception is the very one {pyre.db} publishes, so that the {except}
    clauses client code has always written keep catching what they always did
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})

    # every case is a statement, the exception it must raise, and the SQLSTATE the server
    # names; the classification follows the code, not the message the server wrote for a human
    cases = [
        # a statement the parser cannot read
        ("SELECT FROM WHERE", exceptions.ProgrammingError, "42601"),
        # a table that is not there
        ("SELECT * FROM pyre_no_such_table", exceptions.ProgrammingError, "42P01"),
        # a division with no answer; the statement is well formed, and the data in it is not
        ("SELECT 1/0", exceptions.DataError, "22012"),
        # a value that is not what its type requires
        ("SELECT 'seven'::int", exceptions.DataError, "22P02"),
    ]

    # walk the cases
    for statement, expected, sqlstate in cases:
        # carefully
        try:
            # run the statement
            connection.exec(statement)
            # and complain if it succeeded
            assert False, f"{statement!r} did not raise"
        # the exception it must raise
        except expected as error:
            # the server named the condition
            assert error.sqlstate == sqlstate, f"{statement!r} -> {error.sqlstate}"
            # and the exception is one that derives from the framework's base
            assert isinstance(error, exceptions.FrameworkError)
            # and carries the statement that provoked it
            assert error.command == statement

    # a statement that would leave the database inconsistent is an {IntegrityError}; this is the
    # one that matters most, because correct code routinely expects it: an insert that collides
    # is how a program discovers a row is already there. make a table with a key
    connection.exec("CREATE TEMP TABLE unique_test (id int PRIMARY KEY)")
    # put a row in it
    connection.exec("INSERT INTO unique_test (id) VALUES (1)")
    # and try to put it in again
    try:
        # with the same key
        connection.exec("INSERT INTO unique_test (id) VALUES (1)")
        # and complain if the server took it
        assert False, "a unique violation did not raise"
    # the collision
    except exceptions.IntegrityError as error:
        # is a unique violation
        assert error.sqlstate == "23505"
        # and the server told us which constraint it was, and on which table, so that a caller
        # with two of them need not read english to tell them apart
        assert error.constraint
        # on this table
        assert error.table == "unique_test"
        # the family of the condition is the first two characters of its code
        assert error.category == "23"

    # every one of the above is a complaint from the server, so every one is catchable as the
    # base of that family
    try:
        # provoke one
        connection.exec("SELECT 1/0")
        # and complain if it did not raise
        assert False, "a division by zero did not raise"
    # catch it by the base
    except exceptions.DatabaseError:
        # which is what should happen, so there is nothing else to check
        pass

    # a message that contains braces must not break the rendering of the exception; the server
    # writes the offending text into its complaint, and {str} interpolates it rather than
    # treating it as a format string
    try:
        # name a table with braces in its name
        connection.exec('SELECT * FROM "tbl{0}"')
        # and complain if it did not raise
        assert False, "a bad identifier did not raise"
    # the complaint
    except exceptions.ProgrammingError as error:
        # must render without raising a second exception from inside the first
        assert "tbl{0}" in str(error)

    # a warning is not an error; the database api puts the two side by side, so a {catch} that
    # looks for a failure does not also catch a warning
    assert not issubclass(exceptions.Warning, exceptions.Error)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
