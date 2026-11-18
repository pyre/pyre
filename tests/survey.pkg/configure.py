#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    {survey.configure} walks a component's properties, prompting per trait type, and coerces and
    validates each answer before applying it
    """
    # for scripting the replies and silencing the chatter
    import builtins
    import contextlib
    import io

    # get the framework and the package
    import pyre
    import survey

    # a non-interactive terminal so the prompts fall back to their cooked and numbered paths
    from pyre.terminals.Plain import Plain

    # make it the terminal the prompts ride
    pyre.executive.terminal = Plain(
        name="test.configure.plain", istream=io.StringIO(), ostream=io.StringIO()
    )

    # a component with a boolean, a constrained integer, a set-valued string, and a path
    class Demo(pyre.component, family="test.survey.configure"):
        """
        A component with one trait of each kind the wizard prompts for
        """

        # a boolean
        verbose = pyre.properties.bool()
        verbose.default = False

        # an integer that must be positive
        count = pyre.properties.int()
        count.default = 3
        count.validators = pyre.constraints.isGreater(value=0)

        # a string drawn from a set
        mode = pyre.properties.str()
        mode.default = "fast"
        mode.validators = pyre.constraints.isMember("fast", "slow")

        # and a path
        where = pyre.properties.path()
        where.default = "/tmp"

    # an instance to configure
    demo = Demo(name="demo")

    # scripted answers: verbose yes; count rejects -1 (constraint) and 'nope' (coercion) before it
    # accepts 7; mode picks the second option (slow) through the numbered menu; where is kept by a
    # blank reply, which takes the default
    answers = iter(["yes", "-1", "nope", "7", "2", ""])
    # hand them out one prompt at a time
    builtins.input = lambda prompt="": next(answers)

    # run the wizard, swallowing the menu and error chatter so a passing test stays silent
    with contextlib.redirect_stdout(io.StringIO()):
        # over the instance
        survey.configure(demo)

    # every trait ended up with the expected, validated value: the boolean
    assert demo.verbose is True, demo.verbose
    # the integer
    assert demo.count == 7, demo.count
    # the string
    assert demo.mode == "slow", demo.mode
    # and the path
    assert str(demo.where) == "/tmp", str(demo.where)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
