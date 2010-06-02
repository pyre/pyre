#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that thepyre implementation of the Singleton pattern works as advertised
"""

  
from pyre.patterns.Singleton import Singleton


class singleton(metaclass=Singleton):

    def __init__(self):
        self.value = 1
        return


def test():
    a = singleton()
    a.value = 2
    b = singleton()

    assert a.value == 2
    assert b.value == 2

    return singleton


# main
if __name__ == "__main__":
    test()


# end of file 
