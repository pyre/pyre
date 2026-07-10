#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the extension module is accessible, and that it publishes the entities
its clients are told to expect
"""


def test():
    # access the bindings
    from pyre.extensions import libpq

    # the entities the module publishes
    assert libpq.Connection is not None
    assert libpq.Transaction is not None
    assert libpq.Result is not None
    assert libpq.Row is not None
    assert libpq.Field is not None
    assert libpq.Diagnostic is not None
    assert libpq.Notification is not None

    # the enumerations
    assert libpq.ConnectionStatus.ok is not None
    assert libpq.ExecStatus.tuplesOk is not None
    assert libpq.TransactionStatus.idle is not None
    assert libpq.Format.text is not None

    # the client library it is linked against, which is a number: 16.2 is 160002
    assert libpq.version() > 0

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
