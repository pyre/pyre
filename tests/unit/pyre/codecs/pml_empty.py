#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    # package access
    import pyre.codecs
    import pyre.config
    # get the codec manager
    m = pyre.codecs.newManager()
    # ask for a pml codec
    reader = m.newCodec(encoding="pml")
    # build a configurator to store the harvested venets
    c = pyre.config.newConfigurator()
    # open a stream
    sample = open("sample-empty.pml")
    # read the contents
    configuration = reader.decode(configurator=c, stream=sample)
    # check that we got a real instance back
    assert configuration is not None
    # check that it is an instance of the right type
    from pyre.codecs.pml.Configuration import Configuration
    assert isinstance(configuration, Configuration)

    return m, reader, configuration


# main
if __name__ == "__main__":
    test()


# end of file 
