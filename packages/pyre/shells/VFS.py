# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# framework
import pyre


# the action
class VFS(pyre.command, family='pyre.actions.vfs'):
    """
    Direct access to the application database
    """


    # public state
    prefix = pyre.properties.str(default='/')


    # command obligations
    @pyre.export
    def main(self, plexus, **kwds):
        """
        This is the implementation of the action
        """
        # list the contents
        plexus.vfs[self.prefix].dump()
        # and indicate success
        return 0


    @pyre.export
    def help(self, plexus, **kwds):
        """
        Show a help screen
        """
        # here is the list of my commands
        commands = ' | '.join(['new', 'update', 'terminate'])
        # show me
        self.info.log('list the contents of the virtual file system')
        self.info.line('usage:   {.pyre_namespace} vfs --prefix=<uri>')
        self.info.log()
        # all done
        return 0


# end of file
