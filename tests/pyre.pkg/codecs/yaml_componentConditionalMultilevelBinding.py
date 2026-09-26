#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that conditional assignments whose keys reach inside a nested component are applied
to the correct trait

The configuration file binds a facility to a named instance of a specific implementation
and, in the same breath, configures a trait of a component that is nested inside that
implementation. The assignment must land on the nested trait, not on the facility that
holds the nested component.
"""


def test():
    # access the framework
    import pyre

    # load the configuration file
    pyre.loadConfiguration("sample-componentConditionalMultilevel.yaml")

    # N.B.: the protocols are named after their families, in the plural, so that their
    # names differ from the names of the traits they decorate: a class body that assigns a
    # name looks it up among the globals, not among the locals of the enclosing function

    # a protocol for the innermost component
    class discretizations(pyre.protocol, family="test.discretizations"):
        """the requirements of a discretization"""

        # the trait our configuration file reaches for
        basis_order = pyre.properties.int()

        # nominate the preferred implementation
        @classmethod
        def pyre_default(cls, **kwds):
            """the preferred implementation"""
            # which is the only one
            return uniform

    # and an implementation
    class uniform(
        pyre.component, family="test.discretizations.uniform", implements=discretizations
    ):
        """a trivial discretization"""

        # the trait our configuration file reaches for
        basis_order = pyre.properties.int()

    # a protocol for the component that gets bound to a facility
    class fields(pyre.protocol, family="test.fields"):
        """the requirements of a field"""

        # nominate the preferred implementation
        @classmethod
        def pyre_default(cls, **kwds):
            """the preferred implementation"""
            # which is the only one
            return basic

    # and an implementation that has a nested component of its own
    class basic(pyre.component, family="test.fields.basic", implements=fields):
        """a field with a nested discretization"""

        # a trait of my own
        alias = pyre.properties.str()
        # and the facility that holds my nested component
        discretization = discretizations(default=uniform)

    # the component that owns the facility
    class subject(pyre.component, family="test.subject"):
        """the client"""

        # the facility the configuration file binds
        field = fields()

    # instantiate the client; this resolves the {basic#dotted} specification in the
    # configuration file, which builds and configures the nested instance
    s = subject(name="subject")
    # get the bound field
    dotted = s.field
    # check that the binding picked the right implementation
    assert isinstance(dotted, basic)
    # and gave it the right name
    assert dotted.pyre_name == "dotted"
    # the single level assignment is applied
    assert dotted.alias == "dotted_alias"
    # the nested component is named after its owner and the facility that holds it
    assert dotted.discretization.pyre_name == "dotted.discretization"
    # and receives the assignment that reaches inside it
    assert dotted.discretization.basis_order == 2

    # repeat for the component that is configured using a nested mapping, this time
    # instantiating it explicitly rather than through facility resolution
    nested = basic(name="nested")
    # the single level assignment is applied
    assert nested.alias == "nested_alias"
    # and so is the one that reaches inside the nested component
    assert nested.discretization.basis_order == 3

    # the two nested components are distinct, so the assignments must not have leaked
    assert dotted.discretization is not nested.discretization

    # all done
    return s, dotted, nested


# main
if __name__ == "__main__":
    test()


# end of file
