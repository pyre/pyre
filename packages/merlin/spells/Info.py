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
                import journal
                journal.warning('merlin.info').log('no project information found')
            # otherwise
            else:
                # print
                print('project:')
                print('  name: {}'.format(project.name))
                print('  root: {}'.format(vfs['/project'].uri))
                print('  merlin configuration: {}'.format(vfs['/merlin/project'].uri))

        # user information
        if self.user or self.all:
            # access the user metadata
            user = self.merlin.user
            # print
            print('user:')
            print('  name: {}'.format(user.name))
            print('  email: {}'.format(user.email))
            print('  affiliation: {}'.format(user.affiliation))
            print('  uid: {}'.format(user.uid))
            print('  username: {}'.format(user.username))
            print('  home: {}'.format(user.home))
            print('  merlin configuration: {}'.format(vfs['/merlin/user'].uri))

        # host information
        if self.host or self.all:
            # access the host metadata
            host = self.merlin.host
            # print
            print('host:')
            print('  name: {}'.format(host.name))
            print('  system: {}'.format(host.system))
            print('  release: {}'.format(host.release))
            print('  architecture: {}'.format(host.architecture))

        # all done
        return


# end of file 
