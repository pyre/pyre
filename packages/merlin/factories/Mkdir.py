# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
# framework
import merlin
# superclass
from .Factory import Factory


# creates a directory an a filesystem
class Mkdir(Factory, family="merlin.factories.mkdir"):
    """
    Create a subdirectory
    """


    # configurable state
    name = merlin.properties.str()
    name.doc = "the name of the subdirectory to create"

    # input
    parent = merlin.protocols.directory.input()
    parent.default = None
    parent.doc = "the parent directory"

    # output
    child = merlin.protocols.directory.output()
    child.default = None
    child.doc = "the child directory i create"


    # protocol obligations
    @merlin.export
    def pyre_make(self, **kwds):
        """
        Construct my products
        """
        # the trivial implementation here is just a place for a breakpoint while debugging
        # it will be removed at some point...
        # chain up
        return super().pyre_make(**kwds)


    # framework hooks
    def pyre_run(self, **kwds):
        """
        Make the subdirectory
        """
        # marker
        indent = " " * 2
        # sign on
        print(f"{indent*1}[mkdir] {self.child.path}")

        # unpack
        name = self.name
        child = self.child
        parent = self.parent

        # the parent is fully formed so it is guaranteed to have a node
        pnode = parent.node
        # that is non trivial
        if not pnode:
            # failing to satisfy this invariant is certainly a bug
            channel = journal.firewall("merlin.factories.mkdir")
            # so complain
            channel.line(f"invalid parent node in {parent}")
            channel.line(f"while attempting to create the subdirectory '{name}'")
            channel.line(f"within '{parent.pyre_name}'")
            # flush
            channel.log()
            # and bail, just in case this firewall wasn't fatal
            return

        # look through the contents of the parent for {name}
        cnode = pnode.contents.get(name)
        # if it's not there
        if not cnode:
            # ask the parent to create the subdirectory
            cnode = pnode.mkdir(name=name)
        # if it is there and it is a directory
        if cnode.isFolder:
            # attach the new node to the child
            child.node = cnode
            # nothing more to do
            return
        # if there and not a directory, we have a problem
        channel = journal.error("merlin.factories.mkdir")
        # complain
        channel.line(f"a file named '{name}' already exists")
        channel.line(f"while attempting to create a subdirectory in '{parent.pyre_name}'")
        # flush
        channel.log()

        # all done
        return


# end of file
