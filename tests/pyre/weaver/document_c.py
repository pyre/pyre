#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: instantiate a weaver and verify its configuration
"""


def test():
    # get the package
    import pyre.weaver
    # instantiate a weaver
    weaver = pyre.weaver.newWeaver(name="sanity")
    weaver.language = "C"

    text = list(weaver.weave())
    assert text == [
        '/*',
        ' * -*- C -*-',
        ' * ',
        ' * Michael A.G. Aïvázis',
        ' * California Institute of Technology',
        ' * (c) 1998-2011 All Rights Reserved',
        ' * ',
        ' */',
        '',
        '',
        '/* end of file */'
        ]

    return


# main
if __name__ == "__main__":
    test()


# end of file 
