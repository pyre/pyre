# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the outcome of a dependency resolution request
class Report:
    """
    The structured outcome of resolving a set of package category requirements

    The report partitions the transitive closure of the request the way a build engine needs
    it: {selections} maps the resolvable categories to their configured installations, in link
    order, i.e. with every package preceding the packages it depends on; {unsupported} lists
    the categories the framework has no recipes for; {unavailable} lists the categories that
    are supported but could not be located on this host; {conflicted} maps the categories
    whose accumulated requirements cannot be satisfied to the requirements involved
    """

    # meta-methods
    def __init__(self, *, requested):
        """
        Prime an empty report for the given {requested} categories
        """
        # the categories the caller asked for
        self.requested = tuple(requested)
        # the map from resolved categories to their installations, in link order
        self.selections = {}
        # the categories the framework knows nothing about
        self.unsupported = []
        # the categories that could not be located on this host
        self.unavailable = []
        # the map from over-constrained categories to the requirements involved
        self.conflicted = {}
        # all done
        return

    # debugging support
    def __str__(self):
        # summarize the outcome
        return (
            f"resolved {len(self.selections)} of {len(self.requested)} requested categories; "
            f"{len(self.unsupported)} unsupported, {len(self.unavailable)} unavailable, "
            f"{len(self.conflicted)} conflicted"
        )

    # narrow the footprint
    __slots__ = ("requested", "selections", "unsupported", "unavailable", "conflicted")


# end of file
