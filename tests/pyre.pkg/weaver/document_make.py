#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#


"""
Exercise a makefile weaver
"""


def test():
    # get the package
    import pyre.weaver
    # instantiate a weaver
    weaver = pyre.weaver.weaver(name="sanity")
    weaver.language = "make"

    text = list(weaver.weave())
    assert text == [
        '# -*- Makefile -*-',
        '#',
        '# Michael A.G. Aïvázis',
        '# Orthologue',
        '# (c) 1998-2021 All Rights Reserved',
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
