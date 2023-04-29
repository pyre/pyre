#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# driver
def test():
    """
    Verify that the attribute harvesting happens correctly
    """

    # get the attribute filter
    from pyre.patterns.AttributeFilter import AttributeFilter


    # establish a descriptor class
    class Descriptor:
        """
        Resting place of attribute metadata
        """

        # marker
        harvested = False


    # the metaclass that does the harvesting
    class Metaclass(AttributeFilter):
        """
        A simple metaclass that looks through its instances for attributes that are instances of
        {Descriptor} and puts them on a pile
        """

        # ignore attributes with these names
        pyre_reservedNames = {"skip"}

        # class record initializer
        def __init__(self, name, bases, attributes, **kwds):
            # chain up
            super().__init__(name, bases, attributes, **kwds)
            # go through the descriptors
            for name, attribute in self.pyre_harvest(attributes, descriptor=Descriptor):
                # make sure the name is not my reserved list
                assert name not in self.pyre_reservedNames
                # mark the rest
                attribute.harvested = True

            # all done
            return


    # here is the client class; its declaration contains extra keywords that should be swallowed by
    # the pyre base metaclass
    class Client(metaclass=Metaclass, extra=True):
        """
        A simple client class
        """

        # a regular attribute
        regular = True
        # an instance of descriptor
        descriptor = Descriptor()
        # an attribute with a reserved name
        skip = Descriptor()


    # check that the non-descriptor attribute survived the process
    assert Client.regular is True
    # verify that {Client.descriptor} is marked correctly
    assert Client.descriptor.harvested is True
    # and that the one with the reserved name is not
    assert Client.skip.harvested is False
    # all done
    return Client


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
