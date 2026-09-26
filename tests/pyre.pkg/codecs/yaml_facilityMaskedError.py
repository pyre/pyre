#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an error raised while instantiating a component that was resolved successfully
is not disguised as a failure to resolve the original specification

Resolving a facility specification includes instantiating the component it names. If that
instantiation fails because one of the component's own facilities is misconfigured, the
report must identify the misconfigured facility. Blaming the outer specification, which is
perfectly good, sends the reader looking in the wrong place.
"""


def test():
    import pyre

    # load the configuration file
    pyre.loadConfiguration("sample-facilityMaskedError.yaml")

    # N.B.: the protocols are named after their families, in the plural, so that their
    # names do not collide with the names of the traits they decorate; class bodies do not
    # see the locals of the enclosing scope

    # a protocol for the innermost component
    class discretizations(pyre.protocol, family="test.discretizations"):
        """the requirements of a discretization"""

        basis_order = pyre.properties.int()

        @classmethod
        def pyre_default(cls, **kwds):
            """the preferred implementation"""
            return uniform

    # and an implementation
    class uniform(
        pyre.component, family="test.discretizations.uniform", implements=discretizations
    ):
        """a trivial discretization"""

        basis_order = pyre.properties.int()

    # a protocol for the component that gets bound to a facility
    class fields(pyre.protocol, family="test.fields"):
        """the requirements of a field"""

        @classmethod
        def pyre_default(cls, **kwds):
            """the preferred implementation"""
            return basic

    # and an implementation that touches its nested component while it is being built, so
    # that the misconfiguration is discovered during instantiation
    class basic(pyre.component, family="test.fields.basic", implements=fields):
        """a field with a nested discretization"""

        discretization = discretizations(default=uniform)

        def __init__(self, **kwds):
            # chain up
            super().__init__(**kwds)
            # look at my nested component
            self.discretization
            # all done
            return

    # the component that owns the facility
    class subject(pyre.component, family="test.subject"):
        """the client"""

        field = fields()

    # instantiate the client
    s = subject(name="subject")
    # attempt to
    try:
        # get the bound field; this must fail
        s.field
        # if it doesn't, we have a bug in the test
        assert False, "the misconfigured facility went unnoticed"
    # it should complain about the nested facility
    except fields.ResolutionError as error:
        # the culprit is the value bound to the nested facility
        assert error.value == "no_such_discretization"
        # and the protocol it could not satisfy is the one of the nested facility
        assert error.protocol is discretizations

    # all done
    return s


# main
if __name__ == "__main__":
    test()


# end of file
