# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
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
        # unpack my separators
        typeSeparator = self.typeSeparator
        scopeSeparator = self.scopeSeparator

        # initialize the sequence of events
        configuration = []
        # reset the list of encountered errors
        self.errors = []

        # initialize the to-do list
        todo = [[doc, [], []]]
        # go through it
        for node, scope, conditions in todo:
            # {scope} is the current prefix that has to be distributed to all names
            # {conditions} is a list constraints that must be true before the assignment is applied
            # {node} is a dictionary of (key, value) pairs
            for token, value in node.items():
                # take apart the token by splitting it on the type separator
                spec = (tag.strip() for tag in token.split(typeSeparator))
                # and extract the scope levels from each one
                spec = tuple(tag.split(scopeSeparator) for tag in spec)
                # if there is only one entry
                if len(spec) == 1:
                    # it's my name
                    name  = scope + spec[0]
                    # and i have no family
                    family = []
                # otherwise
                else:
                    # unpack a pair; anything else is an error
                    family, name = spec
                    # and adjust the name by prefixing it with the current scope
                    name = scope + name

                # if {value} is a nested scope
                if type(value) is type(node):
                    # push it on the to-do list
                    todo.append([value, name, conditions])
                    # and move on
                    continue

                # otherwise, we have an assignment; figure out which kind: if it's conditional
                if conditions:
                    # make a conditional assignment
                    assignment = self.ConditionalAssignment()
                    # add it to the pile
                    configuration.append(assignment)
                    # and move on
                    continue

                # finally, this is an unconditional assignment
                assignment = self.Assignment(key=name, value=value, locator=locator)
                # add it to the pile
                configuration.append(assignment)

        # all done
        return configuration


# end of file
