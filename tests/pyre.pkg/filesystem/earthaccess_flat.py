#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Mount a filesystem over the page a granule query answers and check its contents
"""


def granule(name, size, begin, end):
    """
    Build a catalog record with the shape the common metadata repository uses
    """
    # assemble the record and return it
    return {
        "meta": {"native-id": name},
        "umm": {
            "TemporalExtent": {
                "RangeDateTime": {"BeginningDateTime": begin, "EndingDateTime": end}
            },
            "DataGranule": {
                "ArchiveAndDistributionInformation": [
                    {"Name": f"{name}.h5", "SizeInBytes": size},
                    {"Name": f"{name}.png", "SizeInBytes": 1},
                ]
            },
            "RelatedUrls": [
                {"URL": f"https://daac/{name}.h5", "Type": "GET DATA"},
                {"URL": f"s3://bucket/{name}/{name}.h5", "Type": "GET DATA VIA DIRECT ACCESS"},
                {"URL": f"s3://browse/{name}.png", "Type": "GET RELATED VISUALIZATION"},
            ],
        },
    }


def test():
    # support
    import pyre.filesystem

    # the page the query answers
    page = [
        granule(name="g1", size=10, begin="2026-01-01T00:00:00Z", end="2026-01-01T00:00:10Z"),
        granule(name="g2", size=20, begin="2026-01-02T00:00:00Z", end="2026-01-02T00:00:10Z"),
    ]

    # an engine that answers with the canned page
    def engine(query, count):
        # report more matches than the page carries, and the page
        return 5, page

    # mount the filesystem
    fs = pyre.filesystem.earthaccess(query={"short_name": "product"}, count=2, engine=engine)
    # before discovery, there is nothing on the tree and no sync
    assert not fs.contents
    assert fs.info(node=fs).sync is None
    assert fs.hits is None

    # discover
    fs.discover()
    # the catalog count is on record
    assert fs.hits == 5
    # the root is stamped
    assert fs.info(node=fs).sync is not None
    # the page hangs flat off the root
    assert sorted(fs.contents) == ["g1", "g2"]

    # get a granule
    node = fs["g2"]
    # it is a file
    assert not node.isFolder
    # located under the root
    assert str(node.uri) == "/g2"
    # get its metadata
    info = node.info
    # the whole record is there
    assert info.record is page[1]
    # the payload size adds up the files
    assert info.size == 21
    # only the direct access links are kept
    assert info.links == ["s3://bucket/g2/g2.h5"]
    # the acquisition window is there
    assert info.begin == "2026-01-02T00:00:00Z"
    assert info.end == "2026-01-02T00:00:10Z"
    # and the sync stamp matches the root's
    assert info.sync == fs.info(node=fs).sync

    # all done
    return fs


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
