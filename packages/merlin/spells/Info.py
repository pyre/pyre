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
                plexus.warning.log('no project information found')
            # otherwise
            else:
                # print
                plexus.info.line('project:')
                plexus.info.line('  name: {}'.format(project.name))
                plexus.info.line('  root: {}'.format(vfs['/project'].uri))
                plexus.info.log('  merlin configuration: {}'.format(vfs['/merlin/project'].uri))

        # user information
        if self.user or self.all:
            # access the user metadata
            user = merlin.pyre_user
            # print
            plexus.info.line('user:')
            plexus.info.line('  name: {}'.format(user.name))
            plexus.info.line('  email: {}'.format(user.email))
            plexus.info.line('  affiliation: {}'.format(user.affiliation))
            plexus.info.line('  uid: {}'.format(user.uid))
            plexus.info.line('  username: {}'.format(user.username))
            plexus.info.line('  home: {}'.format(user.home))
            plexus.info.log('  merlin configuration: {}'.format(vfs['/merlin/user'].uri))

        # host information
        if self.host or self.all:
            # access the host metadata
            host = merlin.pyre_host
            # print
            plexus.info.line('host:')
            plexus.info.line('  name: {}'.format(host.hostname))
            plexus.info.line('  platform: {}'.format(host.platform))
            plexus.info.line('  release: {}'.format(host.release))
            plexus.info.line('  codename: {}'.format(host.codename))
            plexus.info.log('  merlin configuration: {}'.format(vfs['/merlin/system'].uri))

        # asset information
        if self.assets or self.all:
            # access the asset folder
            assets = vfs["/merlin/project/assets"]
            # print
            plexus.info.line('assets:')
            # grab each asset pickle
            for name, node in assets.contents.items():
                # load it
                asset = merlin.curator.load(node)
                # print a marker
                plexus.info.line('  {}: {}'.format(asset.name, asset.category))
            # no more assets
            plexus.info.log()

        # all done
        return


# end of file
