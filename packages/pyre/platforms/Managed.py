# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import re
import shutil

# the framework
import pyre

# my protocol
from .PackageManager import PackageManager


# declaration
class Managed(pyre.component, implements=PackageManager):
    """
    The base engine for hosts with real package managers

    Subclasses supply the primitives: an index of installed packages and the contents of each;
    this class supplies the generic algorithm that interprets a package {recipe} against those
    primitives to produce configured installation trait values
    """

    # public data
    @property
    def name(self):
        """
        Get the name of this package manager
        """
        # the base class doesn't have one; subclasses must provide the tag that identifies
        # their section of a package recipe
        raise NotImplementedError(f"class '{type(self).__name__}' must supply a 'name'")

    @property
    def client(self):
        """
        Get the name of the front end to the package manager database
        """
        # the error message template
        msg = (
            f"class '{type(self).__name__}' must supply 'client', "
            "the path to the package manager front end"
        )
        # the base class doesn't have one; subclasses must point to their front end
        raise NotImplementedError(msg)

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
        Retrieve the package manager install location
        """
        # check my cache
        prefix = self._prefix
        # for whether I have done this before
        if prefix is not None:
            # in which case I'm done
            return prefix
        # otherwise, locate the full path to the package manager client
        client = shutil.which(str(self.client))
        # if we found it
        if client:
            # pathify
            client = pyre.primitives.path(client)
        # otherwise
        else:
            # maybe it's not on the path; try the default
            client = self.defaultLocation / self.client
            # if it's not there
            if not client.exists():
                # build the message
                msg = f"could not locate '{self.client}'"
                # complain
                raise self.ConfigurationError(configurable=self, errors=[msg])

        # found it; let's remember its exact location
        self.client = client
        # extract the parent directory
        bin = client.parent
        # and once again to get the prefix
        prefix = bin.parent
        # remember it for next time
        self._prefix = prefix
        # and return it
        return prefix

    @pyre.export
    def available(self):
        """
        Check whether this engine is functional on this host
        """
        # attempt to
        try:
            # locate my front end
            self.prefix()
        # if this fails
        except self.ConfigurationError:
            # i can't help anybody
            return False
        # otherwise, i'm open for business
        return True

    @pyre.export
    def installed(self):
        """
        Retrieve available information for all installed packages
        """
        # ask the index...
        return self.getInstalledPackages()

    @pyre.export
    def info(self, package):
        """
        Return the available information about {package}
        """
        # send what the index has
        return self.getInstalledPackages()[package]

    @pyre.export
    def contents(self, package):
        """
        Retrieve the contents of the {package}
        """
        # ask the package manager for the package contents
        yield from self.retrievePackageContents(package=package)
        # all done
        return

    @pyre.export
    def resolve(self, recipe):
        """
        Map {recipe} onto the name of an installed package that provides it, if any
        """
        # go through the ranked candidate groups
        for package, _ in self.resolveAll(recipe=recipe):
            # the lead of the first one is our best answer
            return package
        # if there weren't any, the recipe is not satisfiable here
        return None

    @pyre.export
    def configure(self, recipe):
        """
        Interpret {recipe} against my package database and return a map of installation trait
        values, or {None} if the package is not installed here
        """
        # go through the ranked candidate groups; some leads, e.g. debian metapackages,
        # carry none of the actual files, so keep going until one passes the recipe markers
        for package, companions in self.resolveAll(recipe=recipe):
            # interpret the recipe against this group
            values = self.interpret(recipe=recipe, package=package, companions=companions)
            # if the markers panned out
            if values is not None:
                # we have our configuration
                return values
        # if no candidate passed, the recipe is not satisfiable here
        return None

    # implementation details
    def resolveAll(self, recipe):
        """
        Generate the ranked sequence of (lead, companions) groups of installed packages that
        may provide {recipe}
        """
        # grab the index of installed packages
        installed = self.getInstalledPackages()
        # collect the candidate groups
        candidates = tuple(recipe.candidates(manager=self.name))
        # keep track of what has been offered
        offered = set()
        # first, look for exact lead matches
        for lead, companions in candidates:
            # if this lead is installed and hasn't been offered
            if lead in installed and lead not in offered:
                # remember it
                offered.add(lead)
                # and offer the group
                yield lead, companions
        # next, look for packages whose names start with a lead, e.g. versioned names
        # like {postgresql16} or {libpython3.13-dev}; scan in reverse order so higher
        # versions win
        for lead, companions in candidates:
            # go through the installed packages
            for package in sorted(installed, reverse=True):
                # if this one matches and hasn't been offered
                if package not in offered and package.startswith(lead):
                    # remember it
                    offered.add(package)
                    # and offer the group
                    yield package, companions
        # finally, interpret leads as regular expressions, for names whose version tag is in
        # the middle, e.g. macports' {py312-numpy}; again, higher versions win
        for lead, companions in candidates:
            # attempt to
            try:
                # compile the lead
                regex = re.compile(lead)
            # if it isn't a valid pattern
            except re.error:
                # move on
                continue
            # go through the installed packages
            for package in sorted(installed, reverse=True):
                # if this one matches in full and hasn't been offered
                if package not in offered and regex.fullmatch(package):
                    # remember it
                    offered.add(package)
                    # and offer the group
                    yield package, companions
        # all done
        return

    def expand(self, spec):
        """
        Generate the installed packages that match the companion {spec}, exactly or by prefix
        """
        # grab the index of installed packages
        installed = self.getInstalledPackages()
        # an exact match goes first
        if spec in installed:
            # offer it
            yield spec
        # then everything the spec abbreviates, higher versions first
        for package in sorted(installed, reverse=True):
            # skip the exact match and non-matches
            if package != spec and package.startswith(spec):
                # offer the rest
                yield package
        # all done
        return

    def interpret(self, recipe, package, companions=()):
        """
        Interpret {recipe} against the combined contents of {package} and its {companions},
        and return a map of installation trait values, or {None} if the group fails the
        recipe markers
        """
        # grab the lead package contents
        contents = tuple(self.contents(package=package))
        # go through the companion specs
        for spec in companions:
            # and every installed package each one matches
            for member in self.expand(spec=spec):
                # folding in their contents
                contents += tuple(self.contents(package=member))
        # start collecting trait values
        values = {}
        # get the package version
        version = self.version(package=package)
        # if the database knows it
        if version:
            # record it
            values["version"] = version

        # locate the folders that hold the header markers
        incdir = []
        # go through the markers
        for header in recipe.headers:
            # find the folder that contains this header
            folder = self.findfirst(target=header, contents=contents)
            # if it's there and we haven't seen it before
            if folder and folder not in incdir:
                # add it to the pile
                incdir.append(folder)

        # locate the folders that hold the libraries, and resolve the actual library stems
        libdir = []
        # the resolved stems
        stems = []
        # go through the library stem patterns
        for pattern in recipe.libraries:
            # find the folder and the actual stem
            folder, stem = self.findlib(pattern=pattern, contents=contents)
            # if we found the library
            if stem and stem not in stems:
                # remember the resolved stem
                stems.append(stem)
            # if the folder is new
            if folder and folder not in libdir:
                # add it to the pile
                libdir.append(folder)

        # locate the executables the recipe cares about
        bindir = []
        # go through the (trait, pattern) markers
        for trait, pattern in recipe.binaries.items():
            # find the folder and the actual filename
            folder, filename = self.findbin(pattern=pattern, contents=contents)
            # if we found the executable
            if filename:
                # record the resolved name under its trait
                values[trait] = filename
            # if the folder is new
            if folder and folder not in bindir:
                # add it to the pile
                bindir.append(folder)

        # acceptance: a recipe that expects headers must find them; otherwise this candidate,
        # e.g. a debian metapackage, doesn't actually carry the goods
        if recipe.headers and not incdir:
            # reject it
            return None
        # similarly, a recipe that expects libraries must resolve at least one stem
        if recipe.libraries and not stems:
            # reject it
            return None
        # and a recipe that expects nothing but executables must find at least one; recipes
        # that also carry header or library markers treat their executables as optional,
        # since package managers often split them off, e.g. debian's {openmpi-bin}
        if recipe.binaries and not recipe.headers and not recipe.libraries and not bindir:
            # reject it
            return None

        # the optional markers extend the include path when present; they play no part in
        # the acceptance above, so they can neither qualify nor veto a candidate
        for extra in recipe.extras:
            # find the folder that contains this one
            folder = self.findfirst(target=extra, contents=contents)
            # if it's there and we haven't seen it before
            if folder and folder not in incdir:
                # add it to the pile
                incdir.append(folder)

        # if any include directories were discovered
        if incdir:
            # record them
            values["incdir"] = incdir
        # if the recipe expects libraries
        if recipe.libraries:
            # record the folders
            values["libdir"] = libdir
            # and the resolved stems
            values["libraries"] = stems
        # if the recipe expects executables
        if recipe.binaries:
            # record the folders
            values["bindir"] = bindir

        # if the recipe carries compile time markers
        if recipe.defines:
            # record them
            values["defines"] = list(recipe.defines)
        # if the recipe induces other package categories
        if recipe.dependencies:
            # record them
            values["dependencies"] = list(recipe.dependencies)

        # evaluate the content proofs against the discovered headers, and the linkages
        # against the discovered libraries
        harvested = recipe.prove(incdir=incdir, libdir=libdir)
        # a failed proof means this interpretation is not the flavor it claims to be
        if harvested is None:
            # so reject it
            return None
        # fold in whatever the extractors gathered; the database reported values are
        # authoritative, so only fill the gaps
        for trait, value in harvested.items():
            # politely
            values.setdefault(trait, value)

        # collect all the folders we discovered
        folders = incdir + libdir + bindir
        # if there are any
        if folders:
            # the installation prefix is their longest common prefix
            values["prefix"] = pyre.primitives.path(self.commonpath(folders=folders))
        # otherwise
        else:
            # fall back to the package database prefix
            values["prefix"] = self.prefix()

        # hand back the configuration
        return values

    # implementation details
    def version(self, package):
        """
        Extract the version of {package} from the installed package index
        """
        # my index stores (version, extra) pairs; unpack and return the version
        version, _ = self.info(package=package)
        # send it off
        return version

    def find(self, target, pile):
        """
        Interpret {target} as a regular expression and return a sequence of the contents of {pile}
        that match it.

        This is intended as a way to scan through the contents of packages to find a path that
        matches {target}
        """
        # compile the target regex
        regex = re.compile(target)

        # go through the pile
        for item in pile:
            # check
            match = regex.match(item)
            # if it matches
            if match:
                # hand it to the caller
                yield match

        # all done
        return

    def findfirst(self, target, contents):
        """
        Locate the folder that contains {target} in the {contents} of some package
        """
        # form the regex
        regex = rf"(?P<path>.*)/{target}$"
        # search for it in contents
        for match in self.find(target=regex, pile=contents):
            # extract the folder
            return pyre.primitives.path(match.group("path"))
        # otherwise, leave it blank
        return None

    def findlib(self, pattern, contents):
        """
        Locate a library whose stem matches {pattern} in the {contents} of some package, and
        return the folder that contains it along with the actual stem
        """
        # the host knows how libraries are named; anchor its pattern to a directory,
        # since package contents are absolute paths
        regex = rf"(?P<path>.*)/{pyre.executive.host.libraryPattern(stem=pattern)}"
        # search for it in contents
        for match in self.find(target=regex, pile=contents):
            # extract the folder and the stem
            return pyre.primitives.path(match.group("path")), match.group("stem")
        # otherwise, report failure
        return None, None

    def findbin(self, pattern, contents):
        """
        Locate an executable that matches {pattern} in the {contents} of some package, and
        return the folder that contains it along with the actual filename
        """
        # form the regex: executables live in a {bin} directory
        regex = rf"(?P<path>.*/bin)/(?P<file>{pattern})$"
        # search for it in contents
        for match in self.find(target=regex, pile=contents):
            # extract the folder and the filename
            return pyre.primitives.path(match.group("path")), match.group("file")
        # otherwise, report failure
        return None, None

    def locate(self, targets, paths):
        """
        Generate a sequence of the full {paths} to the {targets}
        """
        # go through the targets
        for target in targets:
            # and each of paths
            for path in paths:
                # form the combination
                candidate = path / target
                # check whether it exists
                if candidate.exists():
                    # got one
                    yield candidate
                    # grab the next
                    break
        # all done
        return

    def commonpath(self, folders):
        """
        Find the longest prefix common to the given {folders}
        """
        # convert the paths into a sequence of strings
        folders = tuple(map(str, folders))
        # compute and return the longest common prefix
        return os.path.commonpath(folders)

    # private data
    # the installation location of the package manager
    _prefix = None
    # the fallback location of the front end, for hosts where it is not on the path
    defaultLocation = pyre.primitives.path("/usr/bin")


# end of file
