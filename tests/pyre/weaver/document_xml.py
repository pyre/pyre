#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
Exercise an XML weaver
"""


def test():
    # get the package
    import pyre.weaver
    # instantiate a weaver
    weaver = pyre.weaver.weaver(name="sanity")
    weaver.language = "xml"

    text = list(weaver.weave())
    assert text == [
        '<?xml version="1.0"?>',
        '<!--',
        ' ! ',
        ' ! Michael A.G. Aïvázis',
        ' ! Orthologue',
        ' ! (c) 1998-2015 All Rights Reserved',
        ' ! ',
        ' -->',
        '',
        '',
        '<!-- end of file -->'
        ]

    return


# main
if __name__ == "__main__":
    test()


# end of file
