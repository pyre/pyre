# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import re

# framework
import pyre


# a content check against a discovered header
class Proof:
    """
    A content check against a header discovered by a package database engine

    Hard proofs settle claims the package metadata cannot: a pattern that must appear in
    the header ({forbid=False}) or must not ({forbid=True}); either way the header itself
    must be present, since its absence proves nothing. A proof with a {harvest} target is
    a soft extractor instead: when the pattern matches, its first capture group is
    deposited under the named trait, and when it doesn't, the interpretation survives
    unharmed
    """

    # interface
    def evaluate(self, folders):
        """
        Check my pattern against my header, located under one of the {folders}

        Returns an ({ok}, {values}) pair: whether the interpretation survives, and
        whatever was harvested
        """
        # locate my header
        text = self.locate(folders=folders)
        # if it's nowhere to be found
        if text is None:
            # extractors quietly come up empty
            if self.harvest:
                # no harm done
                return True, {}
            # but proofs fail: absence of evidence settles nothing
            return False, {}
        # look for my pattern
        match = self.pattern.search(text)
        # extractors
        if self.harvest:
            # deposit the capture when the pattern matched
            if match:
                # under my target trait
                return True, {self.harvest: match.group(1)}
            # and shrug when it didn't
            return True, {}
        # exclusions fail on a match
        if self.forbid:
            # so the interpretation survives only a miss
            return match is None, {}
        # requirements fail on a miss
        return match is not None, {}

    def locate(self, folders):
        """
        Find my header under one of the {folders} and return its contents
        """
        # go through the candidate folders
        for folder in folders:
            # form the path to my header
            path = pyre.primitives.path(folder) / self.header
            # attempt to
            try:
                # read it
                return open(str(path)).read()
            # if it isn't there
            except OSError:
                # move on to the next folder
                continue
        # the header is nowhere to be found
        return None

    # meta-methods
    def __init__(self, *, header, pattern, forbid=False, harvest=None, **kwds):
        """
        Describe a content check against {header}
        """
        # chain up
        super().__init__(**kwds)
        # the header path, relative to the discovered include directories
        self.header = header
        # the compiled pattern
        self.pattern = re.compile(pattern)
        # the polarity of a hard proof
        self.forbid = forbid
        # the trait an extractor deposits its capture into
        self.harvest = harvest
        # all done
        return

    # debugging support
    def __str__(self):
        # identify myself by header and role
        role = f"harvest '{self.harvest}'" if self.harvest else ("forbid" if self.forbid else "require")
        # assemble
        return f"proof against '{self.header}': {role}"

    # narrow the footprint
    __slots__ = ("header", "pattern", "forbid", "harvest")


# end of file
