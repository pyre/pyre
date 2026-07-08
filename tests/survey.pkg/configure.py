#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    {survey.configure} walks a component's properties, prompting per trait type, and coerces and
    validates each answer before applying it
    """
    # get the package and a few helpers
    import builtins
    import contextlib
    import io
    import pyre
    import survey

    # a non-interactive terminal so the prompts fall back to their cooked and numbered paths
    from pyre.terminals.Plain import Plain

    pyre.executive.terminal = Plain(
        name="test.configure.plain", istream=io.StringIO(), ostream=io.StringIO()
    )

    # a component with a boolean, a constrained integer, a set-valued string, and a path
    class Demo(pyre.component, family="test.survey.configure"):
        verbose = pyre.properties.bool()
        verbose.default = False
        count = pyre.properties.int()
        count.default = 3
        count.validators = pyre.constraints.isGreater(value=0)
        mode = pyre.properties.str()
        mode.default = "fast"
        mode.validators = pyre.constraints.isMember("fast", "slow")
        where = pyre.properties.path()
        where.default = "/tmp"

    # an instance to configure
    demo = Demo(name="demo")

    # scripted answers: verbose yes; count rejects -1 (constraint) and 'nope' (coercion) before it
    # accepts 7; mode picks the second option (slow) through the numbered menu; where is kept by a
    # blank reply, which takes the default
    answers = iter(["yes", "-1", "nope", "7", "2", ""])
    builtins.input = lambda prompt="": next(answers)

    # run the wizard, swallowing the menu and error chatter so a passing test stays silent
    with contextlib.redirect_stdout(io.StringIO()):
        survey.configure(demo)

    # every trait ended up with the expected, validated value
    assert demo.verbose is True, demo.verbose
    assert demo.count == 7, demo.count
    assert demo.mode == "slow", demo.mode
    assert str(demo.where) == "/tmp", str(demo.where)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
