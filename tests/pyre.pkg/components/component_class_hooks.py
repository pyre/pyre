#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The class hooks of protocols and components run once each, in the order configured, initialized,
registered, whether or not the class has a family
"""


def test() -> None:
    """
    Declare a protocol and components that record their class hooks, and check what ran
    """
    # support
    import pyre

    # the hooks that ran, by class name
    calls = {}

    # a mix-in that records the class hooks
    class Recorder:
        """
        Record each class hook as it runs
        """

        @classmethod
        def pyre_classConfigured(cls):
            """
            Record the configuration hook
            """
            # note it
            calls.setdefault(cls.__name__, []).append("configured")
            # and chain up
            return super().pyre_classConfigured()

        @classmethod
        def pyre_classInitialized(cls):
            """
            Record the initialization hook
            """
            # note it
            calls.setdefault(cls.__name__, []).append("initialized")
            # and chain up
            return super().pyre_classInitialized()

        @classmethod
        def pyre_classRegistered(cls):
            """
            Record the registration hook
            """
            # note it
            calls.setdefault(cls.__name__, []).append("registered")
            # and chain up
            return super().pyre_classRegistered()

    # a protocol
    class Protocol(Recorder, pyre.protocol, family="pyre.tests.components.hooks"):
        """
        A protocol that records its class hooks
        """

    # a component with a family, whose class is configured from the store
    class Public(Recorder, pyre.component, family="pyre.tests.components.hooks.public"):
        """
        A component with a family that records its class hooks
        """

    # and one without, whose class is not
    class Private(Recorder, pyre.component):
        """
        A component without a family that records its class hooks
        """

    # every one of them
    for name in ("Protocol", "Public", "Private"):
        # ran each hook once, in order
        assert calls.get(name) == ["configured", "initialized", "registered"], (name, calls)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
