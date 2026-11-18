#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Run statements through the low level interface, and verify that the result reads as a
    sequence of rows whose column names live on the result, rather than masquerading as its
    first row
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})

    # run something with a shape we know
    result = connection.exec("SELECT 1 AS one, 'two' AS two")
    # the server ran it
    assert result.ok
    # and it returned rows
    assert result.status == libpq.ExecStatus.tuplesOk
    # one of them
    assert len(result) == 1
    # holding two values
    assert result.columns == 2
    # the names live on the result, not in a first row every caller has to skip
    assert result.headers == ("one", "two")
    # and the values are what the server sent, as strings
    assert tuple(result[0]) == ("1", "two")

    # a row reads
    row = result[0]
    # by position
    assert row[0] == "1"
    # and by name
    assert row["two"] == "two"
    # and the field behind a value knows its own column
    assert row.field(0).name == "one"

    # a result may be walked, and each row is a sequence of its values
    series = connection.exec("SELECT n FROM generate_series(1, 5) AS n")
    # there are five of them
    assert len(series) == 5
    # and they add up
    assert sum(int(record[0]) for record in series) == 15

    # a value the server did not send is {None}, and not the empty string; this is the database
    # api's rule, and the one the sqlite back end follows
    absent = connection.exec("SELECT NULL::int AS nothing")
    # check it
    assert absent[0][0] is None
    # while a value of zero length is the empty string, and not {None}
    blank = connection.exec("SELECT ''::text AS blank")
    # check it too
    assert blank[0][0] == ""

    # the values travel beside the statement rather than inside it, so nothing in them can
    # change what the statement does
    parameterized = connection.execute("SELECT $1::int + $2::int AS sum", 20, 22)
    # and the server combined them
    assert parameterized[0][0] == "42"

    # a statement that changes something reports how much, and comes back tagged as what it
    # was: make a table
    connection.exec("CREATE TEMP TABLE counted (id int)")
    # put a few rows in it
    inserted = connection.exec("INSERT INTO counted (id) VALUES (1), (2), (3)")
    # the statement ran
    assert inserted.status == libpq.ExecStatus.commandOk
    # and reports how many rows it added
    assert inserted.affected == 3
    # and what it was
    assert inserted.command.startswith("INSERT")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
