# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import re

# the framework
import pyre

# my protocol
from .PackageManager import PackageManager


# declaration
class Bare(pyre.component, family="pyre.platforms.packagers.bare", implements=PackageManager):
    """
    Support for hosts without package management facilities

    This engine probes a user configurable list of installation prefixes for the disk
    artifacts a recipe describes; it is the fallback that makes ad hoc installations in
    standard locations visible to the framework
    """

    # constants
    name = "bare"

    # user configurable state
    searchpath = pyre.properties.paths()
    searchpath.default = ["/usr/local", "/usr"]
    searchpath.doc = "the installation prefixes to probe for packages"

    # protocol obligations
    @pyre.export
    def about(self):
        """
        A phrase identifying this database, for provenance records
        """
        # name myself
        return f"the '{self.name}' package database"

    @pyre.export
    def prefix(self):
        """
        The root of the package database installations
        """
        # i don't have a single one; my {searchpath} plays this role
        return ""

    @pyre.export
    def available(self):
        """
        Check whether this engine is functional on this host
        """
        # probing the filesystem always works
        return True

    @pyre.export
    def installed(self):
        """
        Retrieve available information for all installed packages
        """
        # i don't maintain a package index
        return {}

    @pyre.export
    def info(self, package):
        """
        Return the available information about {package}
        """
        # i don't know anything
        raise KeyError(package)

    @pyre.export
    def contents(self, package):
        """
        Generate a sequence of the files installed by {package}
        """
        # i don't know anything
        raise KeyError(package)

    @pyre.export
    def resolve(self, recipe):
        """
        Map {recipe} onto the installation prefix that provides it, if any
        """
        # go through my search path
        for prefix in self.searchpath:
            # if this prefix passes the recipe's markers
            if self.probe(prefix=prefix, recipe=recipe):
                # it's our answer
                return prefix
        # if we got this far, the recipe is not satisfiable here
        return None

    @pyre.export
    def configure(self, recipe):
        """
        Interpret {recipe} against my search path and return a map of installation trait
        values, or {None} if the package cannot be found
        """
        # find the prefix that provides the recipe
        prefix = self.resolve(recipe=recipe)
        # if there isn't one
        if prefix is None:
            # i can't configure this recipe
            return None
        # start collecting trait values
        values = {"prefix": prefix}

        # if the recipe expects headers
        if recipe.headers:
            # collect the folders that hold them
            incdir = []
            # go through the markers
            for header in recipe.headers:
                # locate the include directory that holds this one
                folder = self.scanForHeader(prefix=prefix, header=header)
                # if it's there and we haven't seen it before
                if folder and folder not in incdir:
                    # add it to the pile
                    incdir.append(folder)
            # record what we found
            values["incdir"] = incdir

        # if the recipe expects libraries
        if recipe.libraries:
            # collect the folders
            libdir = []
            # and the resolved stems
            stems = []
            # go through the stem patterns
            for pattern in recipe.libraries:
                # scan the canonical library folders for a match
                folder, stem = self.scanForLibrary(prefix=prefix, pattern=pattern)
                # if we found the library
                if stem and stem not in stems:
                    # remember the resolved stem
                    stems.append(stem)
                # if the folder is new
                if folder and folder not in libdir:
                    # add it to the pile
                    libdir.append(folder)
            # record the folders
            values["libdir"] = libdir
            # and the stems
            values["libraries"] = stems

        # if the recipe expects executables
        if recipe.binaries:
            # they live in the canonical binary directory
            bindir = prefix / "bin"
            # collect the folders that pan out
            folders = []
            # go through the (trait, pattern) markers
            for trait, pattern in recipe.binaries.items():
                # scan for a match
                filename = self.scanForEntry(folder=bindir, pattern=pattern)
                # if we found the executable
                if filename:
                    # record the resolved name under its trait
                    values[trait] = filename
                    # and remember the folder
                    if bindir not in folders:
                        # just once
                        folders.append(bindir)
            # record the folders
            values["bindir"] = folders

        # if the recipe carries compile time markers
        if recipe.defines:
            # record them
            values["defines"] = list(recipe.defines)
        # if the recipe induces other package categories
        if recipe.dependencies:
            # record them
            values["dependencies"] = list(recipe.dependencies)

        # evaluate the content proofs against the discovered headers
        harvested = recipe.prove(folders=values.get("incdir", ()))
        # a failed proof means this installation is not the flavor it claims to be
        if harvested is None:
            # so reject it
            return None
        # fold in whatever the extractors gathered, filling only the gaps
        for trait, value in harvested.items():
            # politely
            values.setdefault(trait, value)

        # hand back the configuration
        return values

    # implementation details
    def probe(self, prefix, recipe):
        """
        Check whether the installation at {prefix} provides the artifacts that {recipe} expects
        """
        # if the prefix is not a directory
        if not prefix.isDirectory():
            # nothing lives here
            return False
        # every header marker must be locatable under the include directory
        for header in recipe.headers:
            # look for it
            if self.scanForHeader(prefix=prefix, header=header) is None:
                # a missing marker disqualifies the prefix
                return False
        # if the recipe expects libraries, at least one stem must be locatable
        for pattern in recipe.libraries:
            # scan for it
            _, stem = self.scanForLibrary(prefix=prefix, pattern=pattern)
            # if we found one
            if stem:
                # that's enough evidence
                break
        # if the scan came up empty
        else:
            # a recipe with library expectations is not satisfied here
            if recipe.libraries:
                # so this prefix is disqualified
                return False
        # every executable marker must be present in the canonical binary directory
        for _, pattern in recipe.binaries.items():
            # scan for it
            if not self.scanForEntry(folder=prefix / "bin", pattern=pattern):
                # a missing executable disqualifies the prefix
                return False
        # all markers passed
        return True

    def scanForHeader(self, prefix, header):
        """
        Locate the include directory under {prefix} that contains {header}, looking one
        level below the canonical {include} as well, for packages that nest their headers,
        e.g. {include/eigen3}
        """
        # the canonical location
        include = prefix / "include"
        # if the header is right there
        if (include / header).exists():
            # done
            return include
        # if the canonical location isn't a directory, there is nothing to scan
        if not include.isDirectory():
            # report failure
            return None
        # otherwise, look one level down
        for entry in include.contents:
            # for a folder that holds the header
            if entry.isDirectory() and (entry / header).exists():
                # got one
                return entry
        # otherwise, report failure
        return None

    def scanForLibrary(self, prefix, pattern):
        """
        Scan the canonical library folders under {prefix} for a library whose stem matches
        {pattern}, and return the folder along with the actual stem
        """
        # form the regex: dynamic libraries on either platform, plus static archives
        regex = re.compile(rf"lib(?P<stem>{pattern})\.(so|dylib|a)(\.\d+)*$")
        # go through the canonical library folders
        for folder in (prefix / "lib", prefix / "lib64"):
            # if this one doesn't exist
            if not folder.isDirectory():
                # move on
                continue
            # go through its contents
            for entry in folder.contents:
                # check the filename
                match = regex.match(str(entry.name))
                # if it matches
                if match:
                    # extract the folder and the stem
                    return folder, match.group("stem")
        # otherwise, report failure
        return None, None

    def scanForEntry(self, folder, pattern):
        """
        Scan {folder} for an entry that matches {pattern} and return its name
        """
        # form the regex
        regex = re.compile(rf"{pattern}$")
        # if the folder doesn't exist
        if not folder.isDirectory():
            # report failure
            return None
        # go through its contents
        for entry in folder.contents:
            # check the filename
            match = regex.match(str(entry.name))
            # if it matches
            if match:
                # hand back the name
                return str(entry.name)
        # otherwise, report failure
        return None


# end of file
