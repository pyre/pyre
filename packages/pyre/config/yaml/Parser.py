# -*- python -*-
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
    from ...parsing.exceptions import ParsingError

    # constants
    # the separator of a component's family from its name in a key
    typeSeparator = "#"
    # the separator of the levels of a key
    scopeSeparator = "."
    # the prefix of the tags of the yaml specification, which documents spell "!!"
    standard = "tag:yaml.org,2002:"

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
            # look for the fast safe loader, falling back to the pure python implementation; the
            # safe loaders build only the standard yaml types, so no tag can import or call python
            factory = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
            # build a loader over the stream
            loader = factory(stream)
            # carefully, since the loader holds on to the stream
            try:
                # compose the node tree rather than loading the document, so that every node
                # keeps the mark that says where in the file it came from
                doc = loader.get_single_node()
                # refuse the document if it holds a tag the loader cannot build
                self.screen(node=doc, loader=loader, uri=uri, locator=locator)
                # and harvest its contents
                configuration = self.process(doc=doc, loader=loader, uri=uri, locator=locator)
            # if the document is not well formed, or the loader cannot build one of its values
            except yaml.YAMLError as error:
                # record what is wrong, and where
                self.errors.append(self.malformed(error=error, uri=uri, locator=locator))
                # there is nothing to harvest
                return ()
            # if the document holds a tag the loader cannot build
            except self.ParsingError as error:
                # record it
                self.errors.append(error)
                # there is nothing to harvest
                return ()
            # if all is well
            else:
                # hand over the contents
                return configuration
            # release the loader
            finally:
                # in every case
                loader.dispose()

        # if we get this far, we couldn't find {yaml} support
        import journal

        # make a channel
        channel = journal.warning("pyre.config.yaml")
        # say what is missing
        channel.line(f"could not locate support for 'yaml'")
        # and what needed it
        channel.line(f"while attempting to parse '{uri}'")
        # and complain
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
    def malformed(self, error, uri, locator):
        """
        Build a parsing error out of {error}, raised by the yaml loader because the document at
        {uri} is not well formed, that says what is wrong and where
        """
        # the loader describes the problem
        problem = getattr(error, "problem", None) or str(error)
        # and what it was doing when it ran into it
        context = getattr(error, "context", None)
        # put the two together
        description = f"{context}: {problem}" if context else problem
        # the loader marks where the problem is, when it knows
        mark = getattr(error, "problem_mark", None)
        # the marks count from zero, people count from one
        line, column = (None, None) if mark is None else (mark.line + 1, mark.column + 1)
        # place the problem in the file, after the reason the file was read
        where = pyre.tracking.chain(
            this=pyre.tracking.file(source=uri, line=line, column=column), next=locator
        )
        # build the error and return it
        return self.ParsingError(description=description, locator=where)

    def screen(self, node, loader, uri, locator):
        """
        Refuse the document at {uri}, whose node tree is rooted at {node}, if any of its nodes
        carries a tag that {loader} cannot build
        """
        # get the node types
        import yaml

        # the tags the loader builds by name, and the merge keys it folds into their mappings
        known = set(loader.yaml_constructors) | {self.standard + "merge", self.standard + "value"}
        # the prefixes of the families of tags it builds
        families = tuple(loader.yaml_multi_constructors)
        # the nodes left to look at; an empty document has none
        pending = [] if node is None else [node]
        # and the ones already seen, since an alias shares the node of its anchor
        seen = set()
        # as long as there are nodes left
        while pending:
            # grab the next one in document order
            node = pending.pop()
            # if it was seen before
            if id(node) in seen:
                # move on
                continue
            # otherwise, mark it
            seen.add(id(node))
            # if the loader cannot build its tag
            if node.tag not in known and not node.tag.startswith(families):
                # spell the tag the way the document does
                tag = node.tag.replace(self.standard, "!!", 1)
                # find where the node starts
                mark = node.start_mark
                # and place it in the file, after the reason the file was read; the marks count
                # from zero, people count from one
                where = pyre.tracking.chain(
                    this=pyre.tracking.file(source=uri, line=mark.line + 1, column=mark.column + 1),
                    next=locator,
                )
                # and refuse the document
                raise self.ParsingError(
                    description=f"the tag '{tag}' is not supported", locator=where
                )
            # a mapping holds pairs of nodes
            if isinstance(node, yaml.MappingNode):
                # look at each one, in order
                pending.extend(reversed([part for pair in node.value for part in pair]))
            # a sequence holds nodes
            elif isinstance(node, yaml.SequenceNode):
                # look at each one, in order
                pending.extend(reversed(node.value))
        # all done
        return

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
            # find where the entry starts
            mark = keyNode.start_mark
            # and record where it sits in the file; the marks count from zero, people count
            # from one
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

            # if {value} is a nested scope, i.e. a mapping in block form; a mapping in flow form is
            # a value, and an alias has the form of its anchor, since it is the anchor's node
            if isinstance(valueNode, yaml.MappingNode) and not valueNode.flow_style:
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
                # the full path to the trait
                path = scope + name
                # make a conditional assignment; the key is the naked name of the trait, and the
                # rest of the path names the component that receives it, which may be nested
                # inside the one that owns the constraints
                yield self.ConditionalAssignment(
                    key=path[-1:],
                    value=value,
                    component=path[:-1],
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
