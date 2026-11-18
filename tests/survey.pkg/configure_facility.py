#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    {survey.configure} walks a component's facilities: it lets the user choose an
    implementation for each and recurses into the chosen component's own traits
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
        name="test.configure.facility.plain", istream=io.StringIO(), ostream=io.StringIO()
    )

    # a protocol with two implementations
    class Archive(pyre.protocol, family="test.survey.archive"):
        """
        A place where products live
        """

        @pyre.provides
        def locate(self, product):
            """
            Locate a {product}
            """

        @classmethod
        def pyre_default(cls, **kwds):
            """
            The implementation to use when the user names none
            """
            # the local one
            return Local

    # the default implementation, with a path property
    class Local(pyre.component, family="test.survey.archive.local", implements=Archive):
        """
        An archive on the local filesystem
        """

        # where it lives
        root = pyre.properties.path()
        root.default = "/data"

        @pyre.export
        def locate(self, product):
            """
            Locate a {product}
            """
            # it is wherever it was named
            return product

    # a second implementation, with a string property and a set-constrained one
    class S3(pyre.component, family="test.survey.archive.s3", implements=Archive):
        """
        An archive in a bucket
        """

        # the bucket
        bucket = pyre.properties.str()
        bucket.default = "b"

        # and the region it lives in, from a set
        region = pyre.properties.str()
        region.default = "us-west-2"
        region.validators = pyre.constraints.isMember("us-west-2", "us-east-1")

        @pyre.export
        def locate(self, product):
            """
            Locate a {product}
            """
            # it is wherever it was named
            return product

    # a component with a boolean property and an archive facility
    class App(pyre.component, family="test.survey.app"):
        """
        A component with a property and a facility
        """

        # a boolean
        verbose = pyre.properties.bool()
        verbose.default = False

        # and an archive
        archive = Archive()
        archive.doc = "where products live"

    # an instance to configure
    app = App(name="app")

    # scripted answers: verbose yes; pick the second implementation (s3) from the sorted menu;
    # then configure s3 through the recursion: bucket to my-bucket, region to the first choice,
    # which is us-east-1 once the menu is sorted
    answers = iter(["yes", "2", "my-bucket", "1"])
    # hand them out one prompt at a time
    builtins.input = lambda prompt="": next(answers)

    # run the wizard, swallowing the menu chatter so a passing test stays silent
    with contextlib.redirect_stdout(io.StringIO()):
        # over the instance
        survey.configure(app)

    # the property was set
    assert app.verbose is True, app.verbose
    # the facility resolved to S3
    assert type(app.archive).__name__ == "S3", type(app.archive).__name__
    # and its traits were configured through the recursion: the bucket
    assert app.archive.bucket == "my-bucket", app.archive.bucket
    # and the region
    assert app.archive.region == "us-east-1", app.archive.region

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
