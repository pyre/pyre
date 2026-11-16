#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Check the values of attributes: a complex number travels through its own accessors, the
    value of an attribute comes back in its own terms, one value or a list of them, and the
    accessors of a single value refuse an attribute that holds several
    """
    # get the bindings
    from pyre.extensions import libh5

    # and the journal
    import journal

    # for the scratch files
    import os

    # a scratch file
    uri = "h5_ext_attribute_values.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)
    # make it
    f = libh5.File(uri=uri, mode="w")
    # and a group to decorate
    g = f.create(path="product")
    # a scalar space, which is what a single value lives on
    scalar = libh5.DataSpace()
    # and a space for three values
    triple = libh5.DataSpace(shape=[3])

    # a complex number, stored the way most files hold one, as a compound of two reals
    fill = g.createAttribute(name="fill", type=libh5.types.native.complexFloat, space=scalar)
    # save one
    fill.complex(complex(1.5, -2))
    # it comes back through its own accessor
    assert fill.complex() == complex(1.5, -2)
    # and as its value
    assert g.getAttribute(name="fill").value == complex(1.5, -2)
    # a nan survives the trip, part by part
    fill.complex(complex(float("nan"), float("nan")))
    value = fill.value
    assert value != value

    # an integer comes back as an integer
    count = g.createAttribute(name="count", type=libh5.types.native.int32, space=scalar)
    count.int(255)
    assert count.value == 255
    # a real as a real
    scale = g.createAttribute(name="scale", type=libh5.types.native.double, space=scalar)
    scale.double(0.25)
    assert scale.value == 0.25

    # an attribute that holds several values comes back as a list
    bounds = g.createAttribute(name="bounds", type=libh5.types.native.int64, space=triple)
    # which the accessors of a single value refuse to fill; quietly, for this test
    channel = journal.error("pyre.hdf5")
    channel.device = journal.trash()
    channel.fatal = False
    # so an attempt to save a single value into it is refused, and leaves it as it was made
    bounds.int(7)
    # the refusal did not read past the single value either
    assert bounds.int() == 0
    # the list is what the library laid down, which is zeros
    assert bounds.value == [0, 0, 0]
    # a complex accessor refuses an attribute that does not hold complex numbers
    assert count.complex() == 0j

    # close the file, and leave it behind for inspection
    f.close()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
