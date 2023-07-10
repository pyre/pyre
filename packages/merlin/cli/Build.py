# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import journal
import merlin


# declaration
class Build(merlin.shells.command, family="merlin.cli.projects"):
    """
    Access to the projects of the current workspace
    """

    # user configurable state
    only = merlin.properties.strings()
    only.doc = "narrow the projects to those whose name is in this set"

    # commands
    @merlin.export(tip="build the selected projects")
    def projects(self, plexus, **kwds):
        """
        Build the selected projects
        """
        # grab the builder
        builder = plexus.builder
        # and the user defined selection
        only = self.only
        # build the selector
        sieve = (lambda x: x.pyre_name in only) if only else None
        # filter
        projects = filter(sieve, plexus.projects)
        # ask the builder to add each one to its pile
        builder.add(plexus=plexus, assets=projects, target="projects")
        # and then build everything
        builder.build(plexus=plexus)
        # all done
        return

    @merlin.export(tip="build the selected libraries")
    def libraries(self, plexus, **kwds):
        """
        Build the selected libraries
        """
        # grab the builder
        builder = plexus.builder
        # and the user defined selection
        only = self.only
        # build the selector
        sieve = (lambda x: x.name in only) if only else None
        # assemble all accessible libraries
        libs = (lib for project in plexus.projects for lib in project.libraries)
        # filter
        libraries = filter(sieve, libs)
        # ask the builder to add each one to its pile
        builder.add(plexus=plexus, assets=libraries, target="libraries")
        # and then build everything
        builder.build(plexus=plexus)
        # all done
        return

    def default(self, **kwds):
        """
        The default action
        """
        # build all projects
        return self.projects(**kwds)


# end of file
