#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


"""
Exercise the linker
"""


def test():
    import pyre.framework
    # get the linker
    linker = pyre.framework.executive().linker

    # check the registered codecs
    assert tuple(linker.codecs.keys()) == ('import', 'vfs', 'file')

    # all done
    return linker


# main
if __name__ == "__main__":
    test()


# end of file 
