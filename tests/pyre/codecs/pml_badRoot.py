#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check catching of decoding errors when the input file has an unrecognized root tag
"""


def test():
    # package access
    import pyre.config
    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream with an error
    sample = open("sample-badRoot.pml")
    # read the contents
    try:
        reader.decode(source=sample)
        assert False
    except reader.DecodingError as error:
        assert str(error) == (
            "decoding error in file='sample-badRoot.pml', line=11, column=0:"
            " unknown tag 'Config'")
 
    return m, reader


# main
if __name__ == "__main__":
    test()


# end of file 
