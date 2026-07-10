#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Run statements through the low level interface, and verify that the result reads as a sequence
of rows whose column names live on the result, rather than masquerading as its first row
"""


def test():
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})

    # run something with a shape we know
    result = connection.exec("SELECT 1 AS one, 'two' AS two")
    # the server ran it, and it returned rows
    assert result.ok
    assert result.status == libpq.ExecStatus.tuplesOk
    # one of them, holding two values
    assert len(result) == 1
    assert result.columns == 2
    # the names live on the result, not in a first row every caller has to skip
    assert result.headers == ("one", "two")
    # and the values are what the server sent, as strings
    assert tuple(result[0]) == ("1", "two")

    # a row reads by position and by name
    row = result[0]
    assert row[0] == "1"
    assert row["two"] == "two"
    # and the field behind a value knows its own column
    assert row.field(0).name == "one"

    # a result may be walked, and each row is a sequence of its values
    series = connection.exec("SELECT n FROM generate_series(1, 5) AS n")
    assert len(series) == 5
    assert sum(int(r[0]) for r in series) == 15

    # a value the server did not send is {None}, and not the empty string; this is the database
    # api's rule, and the one the sqlite back end already follows
    absent = connection.exec("SELECT NULL::int AS nothing")
    assert absent[0][0] is None
    # while a value of zero length is the empty string, and not {None}
    blank = connection.exec("SELECT ''::text AS blank")
    assert blank[0][0] == ""

    # the values travel beside the statement rather than inside it, so nothing in them can
    # change what the statement does
    parameterized = connection.execute("SELECT $1::int + $2::int AS sum", 20, 22)
    assert parameterized[0][0] == "42"

    # a statement that changes something reports how much, and comes back tagged as what it was
    connection.exec("CREATE TEMP TABLE counted (id int)")
    inserted = connection.exec("INSERT INTO counted (id) VALUES (1), (2), (3)")
    assert inserted.status == libpq.ExecStatus.commandOk
    assert inserted.affected == 3
    assert inserted.command.startswith("INSERT")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
