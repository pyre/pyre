#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Re-run a granule query and check that the tree keeps the granules that are still on the page,
drops the ones that vanished along with the folders they leave empty, and adds the newcomers
"""


def granule(name, folder):
    """
    Build a catalog record that names the folder it belongs to
    """
    # assemble the record and return it
    return {"meta": {"native-id": name}, "umm": {"AdditionalAttributes": [{"Values": [folder]}]}}


def test():
    # support
    import pyre.filesystem

    # the page the query answers, replaced between runs
    pages = [
        [
            granule(name="g1", folder="a"),
            granule(name="g2", folder="a"),
            granule(name="g3", folder="b"),
        ],
        [granule(name="g1", folder="a"), granule(name="g4", folder="c")],
    ]

    # an engine that answers with the next page
    def engine(query, count):
        # hand out the pages in order
        page = pages.pop(0)
        # and answer
        return len(page), page

    # a layout that groups by the folder named in the record
    def layout(granule):
        # place the granule under its folder
        return granule["umm"]["AdditionalAttributes"][0]["Values"][0], granule["meta"]["native-id"]

    # mount the filesystem and discover its contents
    fs = pyre.filesystem.earthaccess(query={}, layout=layout, engine=engine).discover()
    # check the first page
    assert sorted(fs.contents) == ["a", "b"]
    assert sorted(fs["a"].contents) == ["g1", "g2"]
    assert sorted(fs["b"].contents) == ["g3"]
    # hold on to a survivor, a casualty, and the folder that empties
    survivor = fs["a/g1"]
    casualty = fs["a/g2"]
    emptied = fs["b"]
    # and the stamp of the first sync
    first = fs.info(node=fs).sync

    # refresh
    fs.discover()
    # the vanished folder is gone, the new one is there
    assert sorted(fs.contents) == ["a", "c"]
    # the survivor is the same node
    assert fs["a/g1"] is survivor
    # with metadata refreshed from the new page
    assert survivor.info.record is not None
    assert survivor.info.sync == fs.info(node=fs).sync
    # the casualty is gone from its folder
    assert sorted(fs["a"].contents) == ["g1"]
    # and forgotten by the filesystem
    assert casualty not in fs.vnodes
    assert emptied not in fs.vnodes
    # the newcomer is in place
    assert sorted(fs["c"].contents) == ["g4"]
    # the new folder carries the stamp of the second sync
    assert fs["c"].info.sync == fs.info(node=fs).sync
    # the surviving folder keeps the stamp of the sync that made it
    assert fs["a"].info.sync == first
    # the count is current
    assert fs.hits == 2

    # all done
    return fs


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
