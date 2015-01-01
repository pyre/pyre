# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# externals
import merlin


# spells
class Info(merlin.spell):
    """
    A simple spell that prints out information about the machine, user and project
    """


    # public state
    all = merlin.properties.bool(default=False)
    all.doc = 'display all available information'

    assets = merlin.properties.bool(default=False)
    assets.doc = 'controls whether to display asset information'

    project = merlin.properties.bool(default=True)
    project.doc = 'controls whether to display project information'

    user = merlin.properties.bool(default=False)
    user.doc = 'controls whether to display user information'

    host = merlin.properties.bool(default=False)
    host.doc = 'controls whether to display host information'


    # interface
    @merlin.export
    def main(self, plexus, argv):
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
                project = merlin.curator.loadProject()
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
            user = merlin.pyre_user
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
            host = merlin.pyre_host
            # print
            self.info.line('host:')
            self.info.line('  name: {}'.format(host.hostname))
            self.info.line('  platform: {}'.format(host.platform))
            self.info.line('  release: {}'.format(host.release))
            self.info.line('  codename: {}'.format(host.codename))
            self.info.log('  merlin configuration: {}'.format(vfs['/merlin/system'].uri))

        # asset information
        if self.assets or self.all:
            # access the asset folder
            assets = vfs["/merlin/project/assets"]
            # print
            self.info.line('assets:')
            # grab each asset pickle
            for name, node in assets.contents.items():
                # load it
                asset = merlin.curator.load(node)
                # print a marker
                self.info.line('  {}: {}'.format(asset.name, asset.category))
            # no more assets
            self.info.log()

        # all done
        return


# end of file
