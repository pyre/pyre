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
    class Meta(pyre.h5.group):
        """
        A group of datasets in some HDF5 file
        """

        # something boring
        flag = pyre.h5.bool()
        flag.default = True
        flag.pyre_doc = "a boolean"

        # something simple
        answer = pyre.h5.int()
        answer.default = 42
        answer.pyre_doc = "the answer to the ultimate question"

        # a compatible container
        pols = pyre.h5.list(schema=pyre.h5.str())
        pols.default = "HH", "HV", "VH", "VV"
        pols.pyre_doc = "the list of polarizations"

    # embed it in another group
    class Group(pyre.h5.group):
        """
        A group that contains a subgroup
        """

        # the subgroup
        meta = Meta()

    # instantiate
    g1 = Group()

    # verify the state of the subgroup; as a side effect, this adds {meta} to the {g1} inventory
    # however, it does not create entries for the fields of meta, which are resolved against their
    # default values
    assert g1.meta.flag.value == True
    assert g1.meta.answer.value == 42
    assert g1.meta.pols.value == ["HH", "HV", "VH", "VV"]
    # and that the inventories are in the expected state
    assert len(g1.pyre_inventory) == 1
    assert len(g1.meta.pyre_inventory) == 3

    # get the {meta} instance from {g1}
    m1 = g1.meta
    # make some changes
    m1.flag.value = False
    m1.answer.value = 0
    m1.pols.value = ["HH"]
    # check
    assert g1.meta.flag.value == False
    assert g1.meta.answer.value == 0
    assert g1.meta.pols.value == ["HH"]
    assert len(g1.meta.pyre_inventory) == 3

    # make a second group
    g2 = Group()
    # verify it is at the default state
    assert g2.meta.flag.value == True
    assert g2.meta.answer.value == 42
    assert g2.meta.pols.value == ["HH", "HV", "VH", "VV"]
    # and that the inventories are in the expected state
    assert len(g2.pyre_inventory) == 1
    assert len(g2.meta.pyre_inventory) == 3

    # get the {meta} instance from {g2}
    m2 = g2.meta
    # make some changes
    m2.flag.value = False
    m2.answer.value = 1
    m2.pols.value = ["VV"]
    # check
    assert g2.meta.flag.value == False
    assert g2.meta.answer.value == 1
    assert g2.meta.pols.value == ["VV"]
    assert len(g2.meta.pyre_inventory) == 3

    # verify there is no crosstalk with {g1}
    assert g1.meta.flag.value == False
    assert g1.meta.answer.value == 0
    assert g1.meta.pols.value == ["HH"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
