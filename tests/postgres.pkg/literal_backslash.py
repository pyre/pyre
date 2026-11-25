#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that text with a backslash before a quote stays text, even on a server set up to read
backslashes as escapes, where the server can still be set up that way
"""


def test():
    """
    Quote a value that would end its literal early if backslashes were escapes, select it, and
    check it comes back as it was
    """
    # externals
    import os

    # access the package
    import pyre.db

    # connect
    db = pyre.db.postgres(name="backslash").attach()
    # a server before postgres 19 may be set up to read backslashes as escapes
    if db.connection.server < 190000:
        # so disconnect
        db.detach()
        # and start the session again that way, as a server or a role may be set up
        os.environ["PGOPTIONS"] = "-c standard_conforming_strings=off"
        # by connecting anew
        db.attach()
    # a value that carries a statement of its own past an escaped quote
    value = "\\'; SELECT 42 AS injected; --"
    # select it as a literal
    result = db.execute(f"SELECT {db.sql.quote(text=value)} AS value")
    # the answer is one column
    assert result.headers == ("value",), result.headers
    # holding the value as it was
    assert [tuple(row) for row in result] == [(value,)], list(result)
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
