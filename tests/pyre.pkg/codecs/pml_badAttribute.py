#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2025 all rights reserved
#


"""
Check catching of decoding errors when the input file has a tag with a bad attribute
"""


def test():
    # package access
    import pyre.config
    # get the codec manager
    m = pyre.config.newConfigurator()
    # ask for a pml codec
    reader = m.codec(encoding="pml")
    # the configuration file
    uri = "sample-badAttribute.pml"
    # open a stream with an error
    sample = open(uri)
    # read the contents
    try:
        reader.decode(uri=uri, source=sample, locator=None)
        assert False
    except reader.DecodingError as error:
        assert str(error) == (
            "file='sample-badAttribute.pml', line=12, column=2: decoding error:"
            " node 'bind': unknown attribute 'property'"
            )

    return m, reader


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
