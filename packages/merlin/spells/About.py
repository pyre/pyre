# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import merlin


# declaration
class About(merlin.spell, family='merlin.spells.about'):
    """
    Display information about this application
    """


    # user configurable state
    prefix = merlin.properties.str()
    prefix.tip = "specify the portion of the namespace to display"


    # class interface
    @merlin.export(tip="print the copyright note")
    def copyright(self, plexus):
        """
        Print the copyright note of the merlin package
        """
        # leave some space
        plexus.info.line()
        # get the lines
        for line in merlin._merlin_header.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @merlin.export(tip="print out the acknowledgments")
    def credits(self, plexus):
        """
        Print out the license and terms of use of the merlin package
        """
        # make some space
        plexus.info.line()
        # get the lines
        for line in merlin._merlin_acknowledgments.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @merlin.export(tip="print out the license and terms of use")
    def license(self, plexus):
        """
        Print out the license and terms of use of the merlin package
        """
        # make some space
        plexus.info.line()
        # get the lines
        for line in merlin._merlin_license.splitlines():
            # and push them to the plexus info channel
            plexus.info.line(line)
        # flush
        plexus.info.log()
        # all done
        return


    @merlin.export(tip='dump the application configuration namespace')
    def nfs(self, plexus):
        """
        Dump the application configuration namespace
        """
        # get the prefix
        prefix = self.prefix or 'merlin'
        # show me
        plexus.pyre_nameserver.dump(prefix)
        # all done
        return


    @merlin.export(tip="print the version number")
    def version(self, plexus):
        """
        Print the version of the merlin package
        """
        # print the version number as simply as possible
        print(merlin._merlin_version)
        # all done
        return


    @merlin.export(tip='dump the application virtual filesystem')
    def vfs(self, plexus):
        """
        Dump the application virtual filesystem
        """
        # get the prefix
        prefix = self.prefix or '/merlin'
        # show me
        plexus.vfs[prefix].dump()
        # all done
        return


# end of file
