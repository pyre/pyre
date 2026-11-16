#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The errors the configuration and initialization hooks of a component report do not stop it
from being built: they are recorded in the pile of the executive, where the instance sees
them, and each is logged as a warning as it is recorded
"""


def test() -> None:
    """
    Build components whose hooks complain, and check where the complaints go
    """
    # support
    import journal
    import pyre
    from pyre.components.exceptions import ConfigurationError, InitializationError

    # a device that keeps the pages of the entries it receives
    class Capture(journal.device):
        """
        Keep the entries instead of showing them
        """

        # meta-methods
        def __init__(self, **kwds):
            # chain up
            super().__init__(name="capture", **kwds)
            # nothing received yet
            self.pages = []
            # all done
            return

        # interface
        def alert(self, entry):
            """
            Keep a user facing entry
            """
            # keep its page
            self.pages.append("\n".join(entry.page))
            # all done
            return self

        def memo(self, entry):
            """
            Keep a developer facing entry
            """
            # keep its page
            self.pages.append("\n".join(entry.page))
            # all done
            return self

        def help(self, entry):
            """
            Keep a help screen
            """
            # keep its page
            self.pages.append("\n".join(entry.page))
            # all done
            return self

    # a component whose hooks complain
    class Grumpy(pyre.component, family="pyre.tests.components.hooks.grumpy"):
        """
        A component that finds fault with its configuration and its resources
        """

        # framework hooks
        def pyre_configured(self):
            """
            Find fault with my configuration
            """
            # chain up
            yield from super().pyre_configured()
            # and complain
            yield "the configuration is wrong"
            # all done
            return

        def pyre_initialized(self):
            """
            Find fault with my resources
            """
            # chain up
            yield from super().pyre_initialized()
            # and complain
            yield "the resources are missing"
            # all done
            return

    # a component that is content
    class Content(pyre.component, family="pyre.tests.components.hooks.content"):
        """
        A component whose hooks find nothing wrong
        """

    # get the executive
    executive = pyre.executive
    # capture the warnings about configuration errors
    warnings = Capture()
    # by sending them to my device
    journal.warning("pyre.configuration").device = warnings
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.hooks")

    # go through a named and a nameless instance of each
    for name in ["grumpy", None]:
        # count the pile
        recorded = len(executive.errors)
        # carefully
        try:
            # build a grumpy one
            grumpy = Grumpy(name=name)
        # if the complaints stop it
        except pyre.PyreError as error:
            # say so
            channel.line(f"a complaint stopped the instance '{name}': {error}")
            # and move on
            continue
        # the pile must have grown by the two complaints
        added = executive.errors[recorded:]
        # one by each hook, attributed to the instance
        kinds = [type(error) for error in added]
        # if not
        if kinds != [ConfigurationError, InitializationError] or any(
            error.configurable is not grumpy for error in added
        ):
            # say what went wrong
            channel.line(f"the complaints of '{name}' are not in the pile, attributed to it")
            # and the details
            channel.indent()
            channel.line(f"added: {[f'{type(error).__name__}: {error}' for error in added]}")
            channel.line("look in: components/Component.py, components/Actor.py")
            channel.outdent()
        # the instance must see them
        if grumpy.pyre_configurationErrors != added:
            # say what went wrong
            channel.line(f"the instance '{name}' does not see its complaints")
            # and the details
            channel.indent()
            channel.line(f"sees: {[str(error) for error in grumpy.pyre_configurationErrors]}")
            channel.line("look in: components/Component.py, Component.pyre_configurationErrors")
            channel.outdent()
        # and each must have been logged with what it says
        for complaint in ["the configuration is wrong", "the resources are missing"]:
            # if not
            if not any(complaint in page for page in warnings.pages):
                # say so
                channel.line(f"the complaint {complaint!r} of '{name}' was not logged")

    # a content instance
    content = Content(name="content")
    # sees nothing
    if content.pyre_configurationErrors:
        # say so
        channel.line(f"'content' sees errors: {content.pyre_configurationErrors}")

    # if anything went wrong
    if channel.page:
        # complain
        channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
