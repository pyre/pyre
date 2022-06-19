# -*- Python -*-
# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# get the package
import {project.name}


# declaration
class user({project.name}.shells.command, family='{project.name}.cli.user'):
    """
    An example of a user provided command to exercise extensibility
    """


    # meta-data
    pyre_tip = "an example of a user supplied command"


    # behaviors
    @{project.name}.export(tip='convenience action for testing extensibility')
    def test(self, plexus, **kwds):
        """
        Convenient action for testing extensibility or parking debugging code during development
        """
        # show me
        plexus.info.log(self.pyre_name)
        # all done
        return


# end of file
