#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    {survey.configure} walks a component's facilities: it lets the user choose an implementation for
    each and recurses into the chosen component's own traits
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
        name="test.configure.facility.plain", istream=io.StringIO(), ostream=io.StringIO()
    )

    # a protocol with two implementations
    class Archive(pyre.protocol, family="test.survey.archive"):
        @pyre.provides
        def locate(self, product):
            """locate a product"""

        @classmethod
        def pyre_default(cls, **kwds):
            return Local

    # the default implementation, with a path property
    class Local(pyre.component, family="test.survey.archive.local", implements=Archive):
        root = pyre.properties.path()
        root.default = "/data"

        @pyre.export
        def locate(self, product):
            return product

    # a second implementation, with a string property and a set-constrained one
    class S3(pyre.component, family="test.survey.archive.s3", implements=Archive):
        bucket = pyre.properties.str()
        bucket.default = "b"
        region = pyre.properties.str()
        region.default = "us-west-2"
        region.validators = pyre.constraints.isMember("us-west-2", "us-east-1")

        @pyre.export
        def locate(self, product):
            return product

    # a component with a boolean property and an archive facility
    class App(pyre.component, family="test.survey.app"):
        verbose = pyre.properties.bool()
        verbose.default = False
        archive = Archive()
        archive.doc = "where products live"

    # an instance to configure
    app = App(name="app")

    # scripted answers: verbose yes; pick the second implementation (s3) from the sorted menu; then
    # configure s3 through the recursion — bucket to my-bucket, region to the first choice, which is
    # us-east-1 once the menu is sorted
    answers = iter(["yes", "2", "my-bucket", "1"])
    builtins.input = lambda prompt="": next(answers)

    # run the wizard, swallowing the menu chatter so a passing test stays silent
    with contextlib.redirect_stdout(io.StringIO()):
        survey.configure(app)

    # the facility resolved to S3, and its traits were configured through the recursion
    assert app.verbose is True, app.verbose
    assert type(app.archive).__name__ == "S3", type(app.archive).__name__
    assert app.archive.bucket == "my-bucket", app.archive.bucket
    assert app.archive.region == "us-east-1", app.archive.region

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
