#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Exercise an SVG weaver
"""


def test():
    # get the package
    import pyre.weaver
    # instantiate a weaver
    weaver = pyre.weaver.newWeaver(name="sanity")
    weaver.language = "svg"

    text = list(weaver.weave())
    assert text == [
        '<?xml version="1.0"?>',
        '<!--',
        ' ! ',
        ' ! Michael A.G. Aïvázis',
        ' ! California Institute of Technology',
        ' ! (c) 1998-2014 All Rights Reserved',
        ' ! ',
        ' -->',
        '',
        '<svg version="1.1" xmlns="http://www.w3.org/2000/svg">',
        '',
        '',
        '</svg>',
        '',
        '<!-- end of file -->'
        ]

    return


# main
if __name__ == "__main__":
    test()


# end of file 
