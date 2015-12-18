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

    mpi = pyre.externals.mpi()
    mpi.doc = "the mpi installation to use"


    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # get my channel
        info = self.info
        # show me
        info.line("{.pyre_name}:".format(self))

        # get my mpi
        # print("--------------------------------------------------")
        mpi = self.mpi
        # print("--------------------------------------------------")
        # show me
        info.line("  mpi: {}".format(mpi))
        # if i have one
        if mpi:
            # locations
            info.line("    locations:")
            info.line("      prefix: {}".format(mpi.prefix))
            info.line("      bindir: {}".format(mpi.bindir))
            info.line("      incdir: {}".format(mpi.incdir))
            info.line("      libdir: {}".format(mpi.libdir))
            info.line("      launcher: {}".format(mpi.launcher))
            # link line
            info.line("    link:")
            # info.log("      libraries: {}".format(tuple(mpi.libraries())))

            # get the configuration errors
            errors = mpi.pyre_configurationErrors
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
