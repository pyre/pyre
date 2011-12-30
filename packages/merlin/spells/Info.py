# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

# externals
import merlin


# spells
class Info(merlin.spell):
    """A simple spell that prints out the contents of the merlin virtual filesystem"""


    # public state
    all = merlin.properties.bool(default=False) 
    all.doc = 'display all available information'

    project = merlin.properties.bool(default=True) 
    project.doc = 'controls whether to display project information'

    user = merlin.properties.bool(default=False) 
    user.doc = 'controls whether to display user information'

    host = merlin.properties.bool(default=False) 
    host.doc = 'controls whether to display host information'


    # interface
    @merlin.export
    def main(self, **kwds):
        """
        Print out information about a merlin project
        """
        # shorthand to the merlin app
        merlin = self.merlin
        # and to the fileserver
        vfs = self.vfs

        # project information
        if self.project or self.all:
            # attempt to
            try:
                # load the project metadata
                project = self.merlin.curator.loadProject()
            # if that fails
            except vfs.NotFoundError:
                # no worries
                self.warning.log('no project information found')
            # otherwise
            else:
                # print
                self.info.line('project:')
                self.info.line('  name: {}'.format(project.name))
                self.info.line('  root: {}'.format(vfs['/project'].uri))
                self.info.log('  merlin configuration: {}'.format(vfs['/merlin/project'].uri))

        # user information
        if self.user or self.all:
            # access the user metadata
            user = self.merlin.user
            # print
            self.info.line('user:')
            self.info.line('  name: {}'.format(user.name))
            self.info.line('  email: {}'.format(user.email))
            self.info.line('  affiliation: {}'.format(user.affiliation))
            self.info.line('  uid: {}'.format(user.uid))
            self.info.line('  username: {}'.format(user.username))
            self.info.line('  home: {}'.format(user.home))
            self.info.log('  merlin configuration: {}'.format(vfs['/merlin/user'].uri))

        # host information
        if self.host or self.all:
            # access the host metadata
            host = self.merlin.host
            # print
            self.info.line('host:')
            self.info.line('  name: {}'.format(host.name))
            self.info.line('  system: {}'.format(host.system))
            self.info.line('  release: {}'.format(host.release))
            self.info.log('  architecture: {}'.format(host.architecture))

        # all done
        return


# end of file 
