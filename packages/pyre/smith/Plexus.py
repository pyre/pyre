# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# externals
import re

# the framework
import pyre

# my superclass
from .ProjectTemplate import ProjectTemplate


# declaration
class Plexus(ProjectTemplate, family="pyre.smith.projects.plexus"):
    """
    Encapsulation of the project information
    """

    # additional user configurable state
    template = pyre.properties.str(default="plexus")
    template.doc = "the project template"

    # interface
    @pyre.export
    def blacklisted(self, filename):
        """
        Check whether {filename} is on the list of files to not expand
        """
        # check with my pile
        return self.blacklist.match(filename)

    # constants
    blacklist = re.compile(
        "|".join(
            [
                r".+\.png",
            ]
        )
    )


# end of file
