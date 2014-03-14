#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Exercise a Bourne shell weaver
"""


def test():
    # get the package
    import pyre.weaver
    # instantiate a weaver
    weaver = pyre.weaver.newWeaver(name="sanity")
    weaver.language = "sh"

    text = list(weaver.weave())
    assert text == [
        '#!/bin/bash',
        '#',
        '# Michael A.G. Aïvázis',
        '# California Institute of Technology',
        '# (c) 1998-2014 All Rights Reserved',
        '#',
        '',
        '',
        '# end of file',
        ]

    return


# main
if __name__ == "__main__":
    test()


# end of file 
