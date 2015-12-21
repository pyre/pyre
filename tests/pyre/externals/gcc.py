#!/usr/bin/env python.pyre
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#

# the framework
import pyre


# the app
class configure(pyre.application):
    """
    A sample configuration utility
    """

    gcc = pyre.externals.gcc()
    gcc.doc = "the GCC installation"


    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # get my channel
        info = self.info
        # show me
        info.line("{.pyre_name}:".format(self))
        info.line("  host: {.pyre_host}".format(self))
        info.line("  package manager: {.pyre_externals}".format(self))
        # flush
        info.log()

        # get my gcc
        gcc = self.gcc
        # show me
        info.line("  gcc: {}".format(gcc))
        # if i have one
        if gcc:
            # version info
            info.line("    version: {.version}".format(gcc))
            # locations
            info.line("    locations:")
            info.line("      prefix: {.prefix}".format(gcc))
            info.line("      bindir: {.bindir}".format(gcc))
            info.line("      wrapper: {.wrapper}".format(gcc))

            # get the configuration errors
            errors = gcc.pyre_configurationErrors
            # if there were any
            if errors:
                # tell me
                info.line("    configuration errors that were auto-corrected:")
                # and show me
                for index, error in enumerate(errors):
                    info.line("        {}: {}".format(index+1, error))
        # flush
        info.log()

        # all done
        return 0


# main
if __name__ == "__main__":
    # get the journal
    import journal
    # activate the debug channel
    # journal.debug("app").activate()
    # make one
    app = configure(name='configure')
    # drive
    status = app.run()
    # all done
    raise SystemExit(status)


# end of file
