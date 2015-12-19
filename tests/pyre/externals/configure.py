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

    gsl = pyre.externals.gsl()
    gsl.doc = "the GSL installation"

    mpi = pyre.externals.mpi()
    mpi.doc = "the mpi installation"

    python = pyre.externals.python()
    python.doc = "the python installation"


    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # get my channel
        info = self.info
        # show me
        info.line("{.pyre_name}:".format(self))

        # get my python
        python = self.python
        # show me
        info.line("  python: {}".format(python))
        # if i have one
        if python:
            # version info
            info.line("    version: {.version}".format(python))
            # locations
            info.line("    locations:")
            info.line("      prefix: {.prefix}".format(python))
            info.line("      bindir: {.bindir}".format(python))
            info.line("      incdir: {.incdir}".format(python))
            info.line("      libdir: {.libdir}".format(python))
            info.line("      interpreter: {.interpreter}".format(python))
            # link line
            info.line("    link:")
            # info.log("      libraries: {}".format(tuple(python.libraries())))

            # get the configuration errors
            errors = python.pyre_configurationErrors
            # if there were any
            if errors:
                # tell me
                info.line("    configuration errors that were auto-corrected:")
                # and show me
                for index, error in enumerate(errors):
                    info.line("        {}: {}".format(index+1, error))
        # flush
        info.log()

        # get my mpi
        mpi = self.mpi
        # show me
        info.line("  mpi: {}".format(mpi))
        # if i have one
        if mpi:
            # version info
            info.line("    version: {.version}".format(mpi))
            # locations
            info.line("    locations:")
            info.line("      prefix: {.prefix}".format(mpi))
            info.line("      bindir: {.bindir}".format(mpi))
            info.line("      incdir: {.incdir}".format(mpi))
            info.line("      libdir: {.libdir}".format(mpi))
            info.line("      launcher: {.launcher}".format(mpi))
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

        # get my gsl
        gsl = self.gsl
        # show me
        info.line("  gsl: {}".format(gsl))
        # if i have one
        if gsl:
            # version info
            info.line("    version: {.version}".format(gsl))
            # locations
            info.line("    locations:")
            info.line("      prefix: {.prefix}".format(gsl))
            info.line("      incdir: {.incdir}".format(gsl))
            info.line("      libdir: {.libdir}".format(gsl))
            # link line
            info.line("    link:")
            # info.log("      libraries: {}".format(tuple(gsl.libraries())))

            # get the configuration errors
            errors = gsl.pyre_configurationErrors
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
