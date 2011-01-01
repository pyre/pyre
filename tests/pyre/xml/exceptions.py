#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""

def test():

    from pyre.xml.exceptions import (
        ParsingError, UnsupportedFeatureError, DTDError, ProcessingError
        )

    try:
        raise ParsingError(description="some error")
    except ParsingError as error:
        pass

    try:
        raise UnsupportedFeatureError(features=[])
    except UnsupportedFeatureError as error:
        pass

    try:
        raise DTDError(description="some error")
    except DTDError as error:
        pass

    try:
        raise ProcessingError(description="some error")
    except ProcessingError as error:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
