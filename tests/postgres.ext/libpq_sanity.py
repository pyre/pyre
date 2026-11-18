#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Sanity check: verify that the extension module is accessible, and that it publishes the
    entities its clients are told to expect
    """
    # access the bindings
    from pyre.extensions import libpq

    # the entities the module publishes: sessions
    assert libpq.Connection is not None
    # transactions
    assert libpq.Transaction is not None
    # the results of statements
    assert libpq.Result is not None
    # their rows
    assert libpq.Row is not None
    # and their fields
    assert libpq.Field is not None
    # the server's diagnostics
    assert libpq.Diagnostic is not None
    # and the notifications it delivers
    assert libpq.Notification is not None

    # the enumerations: the state of a session
    assert libpq.ConnectionStatus.ok is not None
    # the outcome of a statement
    assert libpq.ExecStatus.tuplesOk is not None
    # the state of a transaction
    assert libpq.TransactionStatus.idle is not None
    # and the format of a value
    assert libpq.Format.text is not None

    # the client library it is linked against, which is a number: 16.2 is 160002
    assert libpq.version() > 0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
