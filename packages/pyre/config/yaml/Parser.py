# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


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
            # attempt to
            try:
                # look for and use the fast loader
                doc = yaml.load(stream, Loader=yaml.CLoader)
            # if that fails
            except ImportError:
                # fall back to the pure python implementation
                doc = yaml.load(stream, Loader=yaml.Loader)
            # process the contents
            return self.process(doc=doc, uri=uri, locator=locator)

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
    def process(self, doc, uri, locator):
        """
        Convert the contents of {doc} into a sequence of configuration events
        """
        # initialize the error pile
        self.errors = []
        # assemble the events
        configuration = tuple(self.harvest(node=doc, locator=locator))
        # and return them
        return configuration


    def harvest(self, node, scope=None, constraints=None,
                locator=None, typesep=typeSeparator, scopesep=scopeSeparator):
        # if the current node is trivial
        if not node:
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
        for key, value in node.items():
            # the key is always a string; yaml interprets keys that are valid numbers
            key = str(key)
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
                constraints.append((scope+name, family))

            # if {value} is a nested scope
            if type(value) is type(node):
                # process it
                yield from self.harvest(node=value, scope=scope+name, constraints=constraints,
                                        locator=locator)
                # and move on
                continue

            # otherwise, we have an assignment; figure out which kind: if it's conditional
            if constraints:
                # the component that owns the assignment is encoded in the last constraint
                component, _ = constraints[-1]
                # make a conditional assignment
                yield self.ConditionalAssignment(key = name, value = value,
                                                 component = component,
                                                 conditions = reversed(constraints),
                                                 locator = locator)
                # and move on
                continue

            # otherwise, it's a raw assignment
            yield self.Assignment(key=scope+name, value=value, locator=locator)

        # all done
        return


# end of file
