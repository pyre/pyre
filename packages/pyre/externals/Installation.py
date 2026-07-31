# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# framework
import pyre

# the requirement list descriptor
from .Requirements import Requirements


# the base manager of specific package installations
class Installation(pyre.component):
    """
    Base class for all package installations

    Instances hold the fully resolved description of one package installation on this host.
    Their traits are populated by depositing package database discoveries into the
    configuration store at {discovery} priority, so any user configuration overrides the
    discovered values through the normal arbitration rules
    """

    # constants
    category = "unknown"
    flavor = "unknown"
    # the flavor classes this flavor answers to; requirement selectors match against the
    # flavor name and these tags
    tags = ()

    # public state
    version = pyre.properties.str(default="unknown")
    version.doc = "the package version"

    prefix = pyre.properties.path()
    prefix.doc = "the package installation directory"

    dependencies = Requirements()
    dependencies.doc = "the requirements this installation imposes on other package categories"

    # public data
    @property
    def majorver(self):
        """
        Extract the portion of a version number that is used to label my parts
        """
        # get my version
        version = self.version
        # attempt to
        try:
            # split my version into major, minor and the rest
            major, *rest = version.split(".")
        # if i don't have enough fields
        except ValueError:
            # can't do much
            return version
        # otherwise, assemble the significant part and return it
        return major

    @property
    def sigver(self):
        """
        Extract the portion of a version number that is used to label my parts
        """
        # get my version
        version = self.version
        # attempt to
        try:
            # split my version into major, minor and the rest
            major, minor, *rest = version.split(".")
        # if i don't have enough fields
        except ValueError:
            # can't do much
            return version
        # otherwise, assemble the significant part and return it
        return f"{major}.{minor}"

    # framework hooks
    def pyre_configured(self):
        """
        Verify the package configuration
        """
        # chain up
        yield from super().pyre_configured()
        # get my prefix
        prefix = self.prefix
        # if it's empty
        if not prefix:
            # complain
            yield "empty prefix"
        # if not but set to something that's not a directory
        elif not prefix.isDirectory():
            # complain
            yield f"invalid prefix '{prefix}'"
        # all done
        return

    # configuration validation
    def verify(self, trait, folders):
        """
        Verify that the {folders} configured in {trait} exist
        """
        # go through the folders
        for folder in folders:
            # check each one
            if not folder.isDirectory():
                # complain about the bad ones
                yield f"{trait}: '{folder}' is not a valid directory"
        # all done
        return

    # rendering support
    def commonpath(self, folders):
        """
        Find the longest prefix common to the given {folders}
        """
        # convert the paths into a sequence of strings
        folders = tuple(map(str, folders))
        # compute and return the longest common prefix
        return os.path.commonpath(folders)

    def join(self, folders, prefix=""):
        """
        Render the sequence of {folders} as a flat string with each one prefixed by {prefix}
        """
        # splice it all together and return it
        return " ".join(f"{prefix}{folder}" for folder in folders)


# end of file
