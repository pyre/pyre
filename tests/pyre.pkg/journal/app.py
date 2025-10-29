#! /usr/bin/env python3
# -*- python -*-


# support
import pyre
import journal


# the app
class App(pyre.application):
    """
    The app app
    """

    # the main entry point\
    @pyre.export
    def main(self, *args, **kwds):
        # check the global journal state
        self.check_journal()
        # check my channels
        self.check_debug()
        self.check_firewall()
        self.check_error()
        self.check_warning()
        self.check_info()
        # all done
        return 0

    # framework hooks
    def pyre_journalChannels(self):
        """
        Generate a sequence of (severity, section) pairs to enable user control over the application
        specific journal channels
        """
        # chain up
        yield from super().pyre_journalChannels()
        # add my channels
        yield "debug", "app.test"
        yield "firewall", "app.test"
        yield "error", "app.test"
        yield "warning", "app.test"
        yield "info", "app.test"
        # all done
        return

    # testers
    def check_journal(self):
        """
        Verify that the global journal state reflects the configuration file
        """
        # check
        assert journal.decor() == 3
        assert journal.detail() == 5
        assert journal.margin() == "    "
        # all done
        return

    def check_debug(self):
        """
        Verify that my debug channel is configured as expected
        """
        # build the channel
        channel = journal.debug("app.test")
        # verify
        assert channel.active is True
        assert channel.fatal is True
        # all done
        return

    def check_firewall(self):
        """
        Verify that my firewall is configured as expected
        """
        # build the channel
        channel = journal.firewall("app.test")
        # verify
        assert channel.active is False
        assert channel.fatal is False
        # all done
        return

    def check_error(self):
        """
        Verify that my error channel is configured as expected
        """
        # build the channel
        channel = journal.error("app.test")
        # verify
        assert channel.active is False
        assert channel.fatal is False
        # all done
        return

    def check_warning(self):
        """
        Verify that my warning channel is configured as expected
        """
        # build the channel
        channel = journal.warning("app.test")
        # verify
        assert channel.active is False
        assert channel.fatal is True
        # all done
        return

    def check_info(self):
        """
        Verify that my info channel is configured as expected
        """
        # build the channel
        channel = journal.info("app.test")
        # verify
        assert channel.active is False
        assert channel.fatal is True
        # all done
        return


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = App(name="app")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file
