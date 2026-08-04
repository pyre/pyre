#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the attribute creation property list and the base it shares with the link
    creation list: both lay down a name, so both answer for the character set it is
    recorded in
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "h5_ext_acpl.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # a fresh attribute creation property list
    acpl = libh5.properties.acpl()
    # everything it governs is inherited from the list that lays down names
    assert isinstance(acpl, libh5.properties.strcpl)
    # the link creation list shares that base, and so answers the same question
    assert isinstance(libh5.properties.lcpl(), libh5.properties.strcpl)

    # names are recorded as ascii, by default
    assert acpl.charEncoding == libh5.CharacterSet.ascii
    # an attribute whose name is not plain ascii says so
    acpl.charEncoding = libh5.CharacterSet.utf8
    assert acpl.charEncoding == libh5.CharacterSet.utf8

    # make a file
    f = libh5.File(uri=uri, mode="w")
    # and a group to decorate
    g = f.create(path="product")

    # a scalar space, which is what a single-valued attribute lives on
    space = libh5.DataSpace()
    # lay an attribute down with my property list
    g.createAttribute(
        name="units", type=libh5.types.native.double, space=space, acpl=acpl
    )
    # it is there
    assert g.hasAttribute(name="units")

    # and one taking the library defaults, to confirm the argument is optional
    g.createAttribute(name="scale", type=libh5.types.native.double, space=space)
    assert g.hasAttribute(name="scale")

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
