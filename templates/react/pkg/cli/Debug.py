# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# externals
import {project.name}


# declaration
class Debug({project.name}.shells.command, family='{project.name}.cli.debug'):
    """
    Display debugging information about this application
    """


    # user configurable state
    prefix = {project.name}.properties.str()
    prefix.tip = "specify the portion of the namespace to display"


    @{project.name}.export(tip="dump the application configuration namespace")
    def nfs(self, plexus, **kwds):
        """
        Dump the application configuration namespace
        """
        # get the prefix
        prefix = self.prefix or "{project.name}"
        # show me
        plexus.pyre_nameserver.dump(prefix)
        # all done
        return 0


    @{project.name}.export(tip="dump the application configuration namespace")
    def vfs(self, plexus, **kwds):
        """
        Dump the application virtual filesystem
        """
        # get the prefix
        prefix = self.prefix or '/{project.name}'
        # build the report
        report = '\n'.join(plexus.vfs[prefix].dump())
        # sign in
        plexus.info.line('vfs: prefix={{!r}}'.format(prefix))
        # dump
        plexus.info.log(report)
        # all done
        return 0


# end of file
