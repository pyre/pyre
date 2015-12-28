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

        # get my gsl
        gsl = self.gsl
        # show me
        info.line("gsl:")
        info.line("  package: {}".format(gsl))
        # if i have one
        if gsl:
            # version info
            info.line("  version: {.version}".format(gsl))
            # locations
            info.line("  locations:")
            info.line("    prefix: {.prefix}".format(gsl))
            info.line("    incdir: {.incdir}".format(gsl))
            info.line("    libdir: {.libdir}".format(gsl))
            # link line
            info.line("  link:")
            # info.log("    libraries: {}".format(tuple(gsl.libraries())))

            # get the configuration errors
            errors = gsl.pyre_configurationErrors
            # if there were any
            if errors:
                # tell me
                info.line("  configuration errors that were auto-corrected:")
                # and show me
                for index, error in enumerate(errors):
                    info.line("      {}: {}".format(index+1, error))
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
