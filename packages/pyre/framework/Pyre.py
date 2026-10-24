# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import weakref
from .. import tracking

# superclass
from .Executive import Executive


# declaration
class Pyre(Executive):
    """
    The default framework executive.

    This class is responsible for the actual instantiation of the providers of the framework
    services.
    """

    # constants
    locator = tracking.simple("during pyre startup")

    # public data
    from . import _verbose as verbose

    # interface
    def activate(self, **kwds):
        """
        Initialize the providers of the runtime services
        """
        # chain up to my base class
        super().activate(**kwds)

        # access the command line
        import sys

        # make a parser
        parser = self.newCommandLineParser()
        # parse the command line
        events = parser.parse(argv=sys.argv[1:])
        # ask my configurator to process the configuration events
        self.configurator.processEvents(events=events, priority=self.priority.command)

        # all done
        return self

    def validateConfiguration(self):
        """
        Check the configuration of every component class and instance i know, record what they
        refuse in my pile, and return it; the framework never calls this, so an application
        decides when, and whether, to check

        N.B.: the check reads every trait, so it materializes the configured state of every
        instance as of that moment: from then on, they no longer follow later changes to their
        classes
        """
        # a check that reaches an instance through another one does not repeat it
        visited = set()
        # get the registrar
        registrar = self.registrar
        # go through the component classes it knows, as they are now, since checking may make
        # more of them
        for component in list(registrar.components):
            # check the class
            component.pyre_classValidateConfiguration()
            # and each of its instances, as they are now, for the same reason
            for instance in list(registrar.components[component]):
                # along with the components they hold
                instance.pyre_validateConfiguration(visited=visited)
        # hand over the pile
        return self.errors

    def showConfigurationErrors(self, channel=None):
        """
        Report the errors in my pile in one entry on {channel}, by default the
        {pyre.configuration} info channel; the framework never calls this, so an application
        decides when, whether, and where to report
        """
        # if there are none
        if not self.errors:
            # there is nothing to report
            return self
        # get the journal
        import journal

        # unless the caller has a channel in mind, make one
        channel = journal.info("pyre.configuration") if channel is None else channel
        # say what this is about
        channel.line("configuration errors:")
        # go through the errors
        channel.indent()
        # each one
        for error in self.errors:
            # in as many lines as it takes
            channel.report(report=str(error).splitlines())
        # done with the errors
        channel.outdent()
        # and flush
        channel.log()
        # all done
        return self

    def showConfigurationCandidates(self, channel=None):
        """
        Report the configuration files i guessed at and did not find, in one entry on {channel},
        by default the {pyre.configuration.candidates} info channel, to help find out why a file
        was not read; the framework never calls this
        """
        # if there are none
        if not self.guesses:
            # there is nothing to report
            return self
        # get the journal
        import journal

        # unless the caller has a channel in mind, make one
        channel = journal.info("pyre.configuration.candidates") if channel is None else channel
        # say what this is about
        channel.line("configuration files guessed at and not found:")
        # go through the guesses
        channel.indent()
        # each one
        for guess in self.guesses:
            # by the file it looked for
            channel.line(str(guess.uri))
        # done with the guesses
        channel.outdent()
        # and flush
        channel.log()
        # all done
        return self

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # get storage for the framework manager proxies
        from .Dashboard import Dashboard as dashboard

        # attach me
        dashboard.pyre_executive = weakref.proxy(self)

        # build my nameserver
        self.nameserver = self.newNameServer()
        # attach
        dashboard.pyre_nameserver = weakref.proxy(self.nameserver)

        # my fileserver
        self.fileserver = self.newFileServer(executive=self)
        # attach
        dashboard.pyre_fileserver = weakref.proxy(self.fileserver)

        # component bookkeeping
        self.registrar = self.newComponentRegistrar()
        # attach
        dashboard.pyre_registrar = weakref.proxy(self.registrar)

        # handler of configuration events
        self.configurator = self.newConfigurator(executive=self)
        # attach
        dashboard.pyre_configurator = weakref.proxy(self.configurator)

        # database schema
        self.schema = self.newSchema(executive=self)
        # attach
        dashboard.pyre_schema = weakref.proxy(self.schema)

        # component linker
        self.linker = self.newLinker()

        # all done
        return


# end of file
