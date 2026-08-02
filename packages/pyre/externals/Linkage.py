# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import re

# framework
import pyre

# the binary image readers
from ..platforms import binaries


# a dependency check against a discovered library
class Linkage:
    """
    A check against the shared libraries a discovered library was linked against

    Where a {Proof} reads what a build says about itself in its headers, a linkage reads
    what it actually bound to. This settles the questions the package metadata leaves
    open: a parallel hdf5 names the mpi implementation it was built against right in its
    dependency list, whatever the package that shipped it happened to be called. Hard
    linkages require the pattern to appear among the dependencies, or with {forbid}
    forbid it; a linkage with a {harvest} target deposits the match under that trait
    instead and never fails

    A linkage votes only on what it can read. When the library is absent, static only,
    or in a format none of the readers understand, the check abstains and the
    interpretation stands on its other evidence
    """

    # interface
    def evaluate(self, folders):
        """
        Check my pattern against the dependencies of my library, found under {folders}

        Returns an ({ok}, {values}) pair: whether the interpretation survives, and
        whatever was harvested
        """
        # read the dependencies of my library
        dependencies = self.inspect(folders=folders)
        # if the library is nowhere to be found, or nothing could read it, this check
        # abstains rather than votes: a static only installation, an image in a format
        # we don't parse, or a stripped down deployment says nothing about what the
        # build bound to, and a linkage that vetoed on silence would reject
        # installations whose headers already proved them good
        if dependencies is None:
            # so let the interpretation through, with nothing harvested
            return True, {}
        # look for my pattern among the dependencies
        match = next(
            (m for m in map(self.pattern.search, dependencies) if m is not None), None
        )
        # extractors
        if self.harvest:
            # deposit the capture when the pattern matched
            if match:
                # under my target trait, using the whole match when there is no group
                value = match.group(1) if match.groups() else match.group(0)
                # and hand it over
                return True, {self.harvest: value}
            # and shrug when it didn't
            return True, {}
        # exclusions fail on a match
        if self.forbid:
            # so the interpretation survives only a miss
            return match is None, {}
        # requirements fail on a miss
        return match is not None, {}

    def inspect(self, folders):
        """
        Find my library under one of the {folders} and return its dependencies
        """
        # the host knows how libraries are named; static archives carry no dependency
        # information, so they are not candidates
        stem = re.compile(
            pyre.executive.host.libraryPattern(stem=re.escape(self.library), static=False)
        )
        # go through the candidate folders
        for folder in folders:
            # skipping the ones that aren't there
            if not folder.isDirectory():
                # by moving on
                continue
            # go through the entries
            for entry in folder.contents:
                # looking for one that carries my library
                if not stem.match(str(entry.name)):
                    # and ignoring the rest
                    continue
                # attempt to
                try:
                    # read the image
                    image = binaries.read(path=folder / entry.name)
                    # and hand over what it links against
                    return tuple(image.dependencies)
                # if it isn't an image we understand, or the read went wrong
                except (binaries.exceptions.BinaryError, OSError):
                    # keep looking; a directory may hold a stale or broken file
                    continue
        # the library is nowhere to be found
        return None

    # meta-methods
    def __init__(self, *, library, pattern, forbid=False, harvest=None, **kwds):
        """
        Describe a dependency check against {library}
        """
        # chain up
        super().__init__(**kwds)
        # the library stem whose dependencies I read
        self.library = library
        # the compiled pattern I look for among them
        self.pattern = re.compile(pattern)
        # the polarity of a hard linkage
        self.forbid = forbid
        # the trait an extractor deposits its capture into
        self.harvest = harvest
        # all done
        return

    # debugging support
    def __str__(self):
        # name the role I play
        role = f"harvest '{self.harvest}'" if self.harvest else ("forbid" if self.forbid else "require")
        # and identify myself by library and role
        return f"linkage against 'lib{self.library}': {role}"

    # narrow the footprint
    __slots__ = ("library", "pattern", "forbid", "harvest")


# end of file
