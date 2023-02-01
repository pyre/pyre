#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Exercise assignments to class attributes
"""


# the driver
def test():
    # support
    import pyre

    # make a group with some data
    class Meta(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something boring
        flag = pyre.h5.schema.bool()
        flag.default = True
        flag.doc = "a boolean"

        # something simple
        answer = pyre.h5.schema.int()
        answer.default = 42
        answer.doc = "the answer to the ultimate question"

        # a compatible container
        pols = pyre.h5.schema.list(schema=pyre.h5.schema.str())
        pols.default = ["HH", "HV", "VH", "VV"]
        pols.doc = "the list of polarizations"

    # embed it in another group
    class Group(pyre.h5.schema.group):
        """
        A group that contains a subgroup
        """

        # the subgroup
        meta = Meta()

    # instantiate
    g1 = Group(name="g1")

    # verify the state of the subgroup; as a side effect, this adds {meta} to the {g1} inventory
    # however, it does not create entries for the fields of meta, which are resolved against their
    # default values
    assert g1.meta.flag.default == True
    assert g1.meta.answer.default == 42
    assert g1.meta.pols.default == ["HH", "HV", "VH", "VV"]
    # and that the inventories are in the expected state
    assert len(g1._pyre_descriptors) == 1
    assert len(g1.meta._pyre_descriptors) == 3

    # get the {meta} instance from {g1}
    m1 = g1.meta
    # make some changes
    m1.flag = False
    m1.answer = 0
    m1.pols = ["HH"]
    # check
    assert g1.meta.flag.default == False
    assert g1.meta.answer.default == 0
    assert g1.meta.pols.default == ["HH"]
    assert len(g1.meta._pyre_descriptors) == 3

    # make a second group
    g2 = Group(name="g2")
    # verify it is at the default state
    assert g2.meta.flag.default == True
    assert g2.meta.answer.default == 42
    assert g2.meta.pols.default == ["HH", "HV", "VH", "VV"]
    # and that the inventories are in the expected state
    assert len(g2._pyre_descriptors) == 1
    assert len(g2.meta._pyre_descriptors) == 3

    # get the {meta} instance from {g2}
    m2 = g2.meta
    # make some changes
    m2.flag = False
    m2.answer = 1
    m2.pols = ["VV"]
    # check
    assert g2.meta.flag.default == False
    assert g2.meta.answer.default == 1
    assert g2.meta.pols.default == ["VV"]
    assert len(g2.meta._pyre_descriptors) == 3

    # verify there is no crosstalk with {g1}
    assert g1.meta.flag.default == False
    assert g1.meta.answer.default == 0
    assert g1.meta.pols.default == ["HH"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
