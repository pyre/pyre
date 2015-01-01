# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import itertools
# access to the framework
import pyre
# my protocol
from .Action import Action


# class declaration
class Command(pyre.component, implements=Action):
    """
    A component that implements {Action}
    """


    # public state
    dry = pyre.properties.bool(default=False)
    dry.doc = "show what would get done without actually doing anything"


    # expected interface
    @pyre.export
    def main(self, **kwds):
        """
        This is the implementation of the action
        """
        # just print a message
        self.info.log('main: missing implementation')
        # and indicate success
        return 0


    @pyre.export(tip='show this help screen')
    def help(self, plexus, **kwds):
        """
        Show a help screen
        """
        # hardwired (for now?)
        indent = '    '
        # tell the user what they typed
        self.info.line('{.pyre_namespace} {.pyre_spec}'.format(plexus, self))

        # if i have a docstring
        if self.__doc__:
            # split my docstring into lines
            for line in self.__doc__.splitlines():
                # indent each one and print it out
                self.info.line('{}{}'.format(indent, line.strip()))

        # the pile of my behaviors
        behaviors = []
        # collect them
        for behavior in self.pyre_behaviors():
            # get the name
            name = behavior.name
            # get the tip
            tip = behavior.tip
            # if there is no tip, assume it is internal and skip it
            if not tip: continue
            # everything else gets saved
            behaviors.append((name, tip))

        # if we were able to find any usage information
        if behaviors:
            # the {usage} section
            self.info.line('usage:')
            # a banner with all the commands
            self.info.line('{}{.pyre_namespace} {.pyre_spec} [{}]'.format(
                indent, plexus, self, " | ".join(name for name,_ in behaviors)))
            # leave some space
            self.info.line()
            # the beginning of the section with more details
            self.info.line('where')
            # figure out how much space we need
            width = max(len(name) for name,_ in behaviors)
            # for each behavior
            for behavior, tip in behaviors:
                # show the details
                self.info.line("{}{:>{}}: {}".format(indent, behavior, width, tip))
            # leave some space
            self.info.line()

        # my public state
        public = []
        # collect them
        for trait in self.pyre_configurables():
            # get the name
            name = trait.name
            # get the type
            schema = trait.typename
            # and the tip
            tip = trait.tip or trait.doc
            # skip nameless undocumented ones
            if not name or not tip: continue
            # pile the rest
            public.append((name, schema, tip))

        # if we were able to find any trait info
        if public:
            # the {options} section
            self.info.line('options:')
            # figure out how much space we need
            width = max(len(name) for name,_,_ in public) + 2 # for the dashes
            # for each behavior
            for name, schema, tip in public:
                # show the details
                self.info.line("{}{:>{}}: {} [{}]".format(indent, '--'+name, width, tip, schema))
            # leave some space
            self.info.line()

        # flush
        self.info.log()
        # and indicate success
        return 0


    # meta-methods
    def __init__(self, name, spec, plexus, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # save my short name
        self.pyre_spec = spec
        # give me journal
        import journal
        # build my channels
        self.debug = plexus.debug
        self.firewall = plexus.firewall
        self.info = plexus.info
        self.warning = plexus.warning
        self.error = plexus.error
        # all done
        return


    # implementation details
    def __call__(self, plexus, argv):
        """
        Commands are callable
        """
        # wire it to invoking {main}
        return self.main(plexus=plexus, argv=argv)


    # private data
    pyre_spec = None


# end of file
