#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Check catching of decoding errors when the input file has a bad tag
"""


def test():
    # package access
    import pyre.config
    # get the codec manager
    m = pyre.config.newCodecManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # open a stream with an error
    sample = open("sample-badNode.pml")
    # read the contents
    try:
        reader.decode(source=sample)
        assert False
    except reader.DecodingError as error:
        assert str(error) == (
            "decoding error in file='sample-badNode.pml', line=12, column=77: mismatched tag"
            )
 
    return m, reader


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
