# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import journal


# a visitor that resolves dataset shape references against a schema tree's named dimensions
class Resolver:
    """
    Walk a schema tree and populate the root's shape index

    Each group registers the dimensions it provides as unresolved nodes at their scoped
    path; each dataset's named shape references are aliased to the nearest enclosing
    provider, found by walking up the tree. The root is just the starting point and, like
    every group and dataset, a spectator: the logic lives here.
    """

    # interface
    def resolve(self, root):
        """
        Resolve the shapes of the tree rooted at {root} into {root._pyre_shapes}
        """
        # kick off the down-walk at the root, threading the path and the index
        root._pyre_identify(authority=self, path=(), shapes=root._pyre_shapes)
        # all done
        return

    # visitor hooks
    def _pyre_onGroup(self, group, path, shapes):
        """
        Register {group}'s provided dimensions, then descend into its members
        """
        # register each dimension this group provides
        for dimension in group._pyre_dimensions():
            # at its scoped path; {retrieve} mints an unresolved node if none exists yet
            shapes.retrieve(self._join(path + (dimension._pyre_name,)))
        # descend into the members
        for member in group._pyre_descriptors():
            # extending the path with the member's on-disk name
            member._pyre_identify(
                authority=self, path=path + (member._pyre_name,), shapes=shapes
            )
        # all done
        return

    def _pyre_onDataset(self, dataset, path, shapes):
        """
        Alias {dataset}'s named shape references to the dimensions that scope them
        """
        # get my shape, if any; scalars and dynamic containers have none to resolve
        shape = getattr(dataset, "shape", None)
        # if there is nothing to resolve
        if not shape:
            # we are done
            return
        # the scope for resolution is the group that contains me
        scope = path[:-1]
        # go through my axes
        for axis in shape:
            # only named references resolve; ints and {Ellipsis} pass through untouched
            if not isinstance(axis, str):
                continue
            # find the nearest enclosing provider
            target = self._resolve(name=axis, scope=scope, shapes=shapes)
            # if none was found
            if target is None:
                # we have already complained; move on so the rest of the tree still builds
                continue
            # alias my reference to it
            shapes.alias(target=target, alias=axis, base=self._join(path))
        # all done
        return

    # implementation details
    def _resolve(self, name, scope, shapes):
        """
        Walk up from {scope} to the nearest registered node named {name}
        """
        # start at the dataset's scope
        candidate = list(scope)
        # walk up the tree
        while True:
            # form the candidate full name
            full = self._join(tuple(candidate) + (name,))
            # if a node is registered there
            if full in shapes:
                # that is our target
                return full
            # if we have exhausted the scope without a match
            if not candidate:
                # the reference names no enclosing dimension; this is a schema bug
                channel = journal.firewall("pyre.h5.schema.shapes")
                # describe it
                channel.line(f"unresolved shape dimension '{name}'")
                channel.line(f"referenced from '{self._join(scope)}'")
                # flush
                channel.log()
                # in case firewalls are not fatal, abandon this reference so the rest of
                # the structure still resolves
                return None
            # otherwise, strip the tail and try the enclosing scope
            candidate.pop()

    @staticmethod
    def _join(fragments):
        """
        Join path {fragments} into a dotted name
        """
        # easy enough
        return ".".join(fragments)


# end of file
