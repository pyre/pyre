# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# extract configurations from {yaml} files
class Parser:
    """
    A parser that extract configuration events from {yaml} files
    """

    # types
    from ..events import Assignment, ConditionalAssignment

    # constants
    typeSeparator = "#"
    scopeSeparator = "."

    # interface
    def parse(self, uri, stream, locator):
        """
        Harvest the configuration events in {stream}
        """
        # attempt to
        try:
            # get the {PyYAML} package
            import yaml
        # if this fails
        except ImportError:
            # no worries, we'll try something else
            pass
        # if it succeeds
        else:
            # look for the fast loader, falling back to the pure python implementation
            factory = getattr(yaml, "CLoader", yaml.Loader)
            # build a loader over the stream
            loader = factory(stream)
            # carefully, since the loader holds on to the stream
            try:
                # compose the node tree rather than loading the document, so that every node
                # keeps the mark that says where in the file it came from
                doc = loader.get_single_node()
                # and process the contents
                return self.process(doc=doc, loader=loader, uri=uri, locator=locator)
            # release the loader
            finally:
                # in every case
                loader.dispose()

        # if we get this far, we couldn't find {yaml} support
        import journal

        # make a channel
        channel = journal.warning("pyre.config.yaml")
        # and complain
        channel.line(f"could not locate support for 'yaml'")
        channel.line(f"while attempting to parse '{uri}'")
        channel.log()

        # all done
        return []

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the error pile
        self.errors = []
        # all done
        return

    # implementation details
    def process(self, doc, loader, uri, locator):
        """
        Convert the contents of {doc}, a node tree, into a sequence of configuration events
        """
        # initialize the error pile
        self.errors = []
        # assemble the events
        configuration = tuple(self.harvest(node=doc, loader=loader, uri=uri, locator=locator))
        # and return them
        return configuration

    def harvest(
        self,
        node,
        loader,
        uri,
        scope=None,
        constraints=None,
        locator=None,
        typesep=typeSeparator,
        scopesep=scopeSeparator,
    ):
        """
        Generate the configuration events in {node}, a mapping node of the tree {loader}
        composed out of the document at {uri}; every event records where in the file it
        came from, on top of {locator}, the reason the file was read
        """
        # get the node types
        import yaml

        # anything but a mapping holds no assignments
        if not isinstance(node, yaml.MappingNode) or not node.value:
            # nothing to do
            return

        # if necessary
        if scope is None:
            # initialize the scope
            scope = []
        # and
        if constraints is None:
            # initialize the constraints
            constraints = []

        # otherwise, go through its contents
        for keyNode, valueNode in node.value:
            # make a copy of the constraints
            conditions = constraints[0:]
            # the key is always a string; yaml interprets keys that are valid numbers
            key = str(loader.construct_object(keyNode))
            # record where the entry sits in the file; the marks count from zero, people
            # count from one
            mark = keyNode.start_mark
            where = pyre.tracking.chain(
                this=pyre.tracking.file(source=uri, line=mark.line + 1, column=mark.column + 1),
                next=locator,
            )
            # take apart the token by splitting it on the type separator
            spec = (tag.strip() for tag in key.split(typesep))
            # and extract the scope levels from each one
            spec = tuple(tag.split(scopesep) for tag in spec)
            # if there is only one entry
            if len(spec) == 1:
                # it's my name
                name = spec[0]
                # and i have no family
                family = []
            # otherwise
            else:
                # unpack a pair; anything else is an error
                family, name = spec

            # assemble the constraints
            if family:
                # add a constraint
                conditions.append((scope + name, family))

            # if {value} is a nested scope
            if isinstance(valueNode, yaml.MappingNode):
                # process it
                yield from self.harvest(
                    node=valueNode,
                    loader=loader,
                    uri=uri,
                    scope=scope + name,
                    constraints=conditions,
                    locator=locator,
                )
                # and move on
                continue
            # otherwise, build the value the way the document loader would have
            value = loader.construct_object(valueNode, deep=True)

            # otherwise, we have an assignment; figure out which kind: if it's conditional
            if conditions:
                # the component that owns the assignment is encoded in the last constraint
                component, _ = conditions[-1]
                # the key is the path from the owning component down to the trait; the
                # component name is a prefix of the current scope, so peel it off
                key = (scope + name)[len(component) :]
                # make a conditional assignment
                yield self.ConditionalAssignment(
                    key=key,
                    value=value,
                    component=component,
                    conditions=reversed(conditions),
                    locator=where,
                )
                # and move on
                continue

            # otherwise, it's a raw assignment
            yield self.Assignment(key=scope + name, value=value, locator=where)

        # all done
        return


# end of file
