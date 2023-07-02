#!/usr/bin/env python.pyre
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

# the framework
import pyre
import journal


# the app
class configure(pyre.application):
    """
    A sample configuration utility
    """

    hdf5 = pyre.externals.hdf5()
    hdf5.doc = "the HDF5 installation"

    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # get my channel
        channel = journal.debug("pyre.externals.hdf5")
        # show me
        channel.line(f"{self.pyre_name}:")
        channel.indent()

        channel.line(f"user: {self.pyre_user}")
        channel.indent()
        channel.line(f"name: {self.pyre_user.name}")
        channel.line(f"email: {self.pyre_user.email}")
        channel.line(f"externals: {self.pyre_user.externals}")
        channel.outdent()

        channel.line(f"host: {self.pyre_host}")
        channel.indent()
        channel.line(f"package manager: {self.pyre_host.packager}")
        channel.line(f"externals: {self.pyre_host.externals}")

        channel.outdent(levels=2)
        # flush
        channel.log()

        # attempt to
        try:
            # get my hdf5
            hdf5 = self.hdf5
        # if something went wrong
        except self.ConfigurationError as error:
            # show me
            self.error.log(str(error))
            # and bail
            return 0

        # show me
        channel.line("hdf5:")
        channel.line("  package: {}".format(hdf5))
        # if i have one
        if hdf5:
            # how did i get this
            channel.line("  locator: {}".format(hdf5.pyre_where()))
            # version info
            channel.line("  version: {.version}".format(hdf5))
            channel.line("  prefix: {.prefix}".format(hdf5))
            # compile line
            channel.line("  compile:")
            channel.line("    defines: {}".format(hdf5.join(hdf5.defines)))
            channel.line("    headers: {}".format(hdf5.join(hdf5.incdir)))
            # link line
            channel.line("  link:")
            channel.line("    paths: {}".format(hdf5.join(hdf5.libdir)))
            channel.line("    libraries: {}".format(hdf5.join(hdf5.libraries)))

            # get the configuration errors
            errors = hdf5.pyre_configurationErrors
            # if there were any
            if errors:
                # tell me
                channel.line("  configuration errors that were auto-corrected:")
                # and show me
                for index, error in enumerate(errors):
                    channel.line("      {}: {}".format(index + 1, error))
        # flush
        channel.log()

        # all done
        return 0


# main
if __name__ == "__main__":
    # get the journal
    import journal

    # activate the debug channel
    # journal.debug("app").activate()
    # make one
    app = configure(name="configure")
    # drive
    status = app.run()
    # all done
    raise SystemExit(status)


# end of file
