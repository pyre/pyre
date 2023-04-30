# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import merlin


# declaration
class About(merlin.shells.command, family='merlin.cli.about'):
    """
    Display information about this application
    """


    @merlin.export(tip="print the copyright note")
    def copyright(self, plexus, **kwds):
        """
        Print the copyright note of the merlin package
        """
        # show the copyright note
        plexus.info.log(merlin.meta.copyright)
        # all done
        return


    @merlin.export(tip="print out the acknowledgments")
    def credits(self, plexus, **kwds):
        """
        Print out the license and terms of use of the merlin package
        """
        # make some space
        plexus.info.log(merlin.meta.header)
        # all done
        return


    @merlin.export(tip="print out the license and terms of use")
    def license(self, plexus, **kwds):
        """
        Print out the license and terms of use of the merlin package
        """
        # make some space
        plexus.info.log(merlin.meta.license)
        # all done
        return


    @merlin.export(tip="print the version number")
    def version(self, plexus, **kwds):
        """
        Print the version of the merlin package
        """
        # make some space
        plexus.info.log(merlin.meta.header)
        # all done
        return


# end of file
