#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Impose a hierarchy on the page a granule query answers, and check that discovering a folder
below the root is answered from the page in hand
"""


def granule(name, stack, date):
    """
    Build a catalog record that carries the attributes a layout groups on
    """
    # assemble the record and return it
    return {
        "meta": {"native-id": name},
        "umm": {
            "AdditionalAttributes": [{"Name": "STACK_ID", "Values": [stack]}],
            "TemporalExtent": {"RangeDateTime": {"BeginningDateTime": f"{date}T00:00:00Z"}},
        },
    }


def test():
    # support
    import pyre.filesystem

    # the page the query answers
    page = [
        granule(name="g1", stack="004_A_018", date="2026-01-01"),
        granule(name="g2", stack="004_A_018", date="2026-01-13"),
        granule(name="g3", stack="011_D_003", date="2026-01-01"),
    ]
    # a tally of the queries that were run
    runs = []

    # an engine that answers with the canned page and counts its invocations
    def engine(query, count):
        # tally
        runs.append(query)
        # and answer
        return len(page), page

    # a layout that groups by stack, then by date
    def layout(granule):
        # dig out the stack
        stack = granule["umm"]["AdditionalAttributes"][0]["Values"][0]
        # and the date of the acquisition
        date = granule["umm"]["TemporalExtent"]["RangeDateTime"]["BeginningDateTime"][:10]
        # place the granule under both
        return stack, date, granule["meta"]["native-id"]

    # mount the filesystem and discover its contents
    fs = pyre.filesystem.earthaccess(query={}, layout=layout, engine=engine).discover()
    # the query ran once
    assert len(runs) == 1
    # the first level is the stacks
    assert sorted(fs.contents) == ["004_A_018", "011_D_003"]
    # the second level is the dates
    assert sorted(fs["004_A_018"].contents) == ["2026-01-01", "2026-01-13"]
    assert sorted(fs["011_D_003"].contents) == ["2026-01-01"]
    # and the granules are the leaves
    assert list(fs["004_A_018/2026-01-13"].contents) == ["g2"]
    assert str(fs["004_A_018/2026-01-13/g2"].uri) == "/004_A_018/2026-01-13/g2"
    # the folders are stamped with the sync
    assert fs["004_A_018"].info.sync == fs.info(node=fs).sync
    assert fs["004_A_018/2026-01-13"].info.sync == fs.info(node=fs).sync

    # discovering a folder below the root is answered from the page in hand
    folder = fs["004_A_018"].discover(levels=1)
    # so the query did not run again
    assert len(runs) == 1
    # and the folder is unchanged
    assert sorted(folder.contents) == ["2026-01-01", "2026-01-13"]
    # a folder deeper down is on the tree already, so reaching it runs no query either
    node = fs["011_D_003/2026-01-01"].discover(levels=1)
    assert list(node.contents) == ["g3"]
    assert len(runs) == 1

    # discovering the root runs the query again
    fs.discover()
    assert len(runs) == 2

    # all done
    return fs


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
