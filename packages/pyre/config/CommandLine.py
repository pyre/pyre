# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import itertools
import pyre.tracking


class CommandLine:
    """
    Support for parsing the application command line

    The general form of a command line configuration event is
        --key=value
    which creates a configuration event that will bind {key} to {value}.

    This implementation supports the following constructs:
        --key
            set key to None
        --key=value
        --key.subkey=value
            key may have an arbitrary number of period delimited levels
        --(key1,key2)=value
            equivalent to --key1=value and --key2=value; an arbitrary number of comma separated
            key names are allowed
        --key.(key1,key2)=value
        --key.(key1,key2).key3=value
            as above; this form is supported at any level of the hierarchy

    By default, instances of the command line parser use the following literals
        '-': introduces a configuration command
        '=': indicates an assignment
        '.': the separator for multi-level keys
        '(' and ')': the start and end of a key group
        ',': the separator for keys in a group

    If you want to change any of this, you can instantiate a command line parser, modify any of
    its public data, and invoke "buildScanners" to recompute the associated regular expression
    engines
    """


    # public data
    prefix = '-'
    assignment = '='
    fieldSeparator = '.'
    groupStart = '('
    groupSeparator = ','
    groupEnd = ')'

    assignmentScanner = None
    locator = staticmethod(pyre.tracking.newCommandLocator)


    # types
    from .Configuration import Configuration


    # interface
    def decode(self, source, locator=None):
        """
        Harvest the configuration events in {argv} and store them in a {configuration}

        parameters:
            {source}: a container of strings of the form "--key=value"
            {locator}: an optional locator; not used by this decoder
        """
        # the source is really an iterable of strings
        argv = source
        # buld a configuration object to store the processed commandline
        configuration = self.Configuration()
        # run through the command line
        for index,arg in enumerate(argv):
            # look for an assignment
            match = self.assignmentScanner.match(arg)
            # process it if it matches
            if match:
                # get the tokens from the scanner
                key = match.group("key")
                value = match.group("value")
                if key == 'config':
                    configuration.newSource(source=value, locator=self.locator(arg=index))
                elif key:
                    # if a key were specified
                    self._processAssignments(configuration, key,value, self.locator(arg=index))
                else:
                    # we ran in to a '-' or '--' that signals the end of configuration options
                    self._processArguments(configuration, *argv[index+1:])
                    break
            # else it must be a regylar command line argument
            else:
                self._processArguments(configuration, arg)
        # all done; return the configuration
        return configuration


    def buildScanners(self):
        """
        Build the command line recognizers that are used to detect the supported command line
        argunent syntactical forms
        """
        import re

        # the assignment recognizer regular expression
        regex = []
        # add the prefix
        if self.prefix:
            regex.append(r'(?P<prefix>' + self.prefix + r'{1,2})')
        # and the 'key=value' form
        regex += [
            # the key
            r'(?P<key>[^', self.assignment, r']*)',
            # the optional assignment symbol
            self.assignment, r'?',
            # and the optional value
            r'(?P<value>.+)?'
            ]
        # compile this pattern
        self.assignmentScanner = re.compile("".join(regex))

        # all done
        return
                    

    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # build the scanners
        self.buildScanners()
        # all done
        return


    # implementation details
    def _processAssignments(self, configuration, key, value, locator):
        """
        Handler for command line arguments that were interpreted as assignments

        Look for the supported shorthands and unfold them into canonical forms.
        """
        # split the key on the field separator identify the various fields
        fields = []
        for field in key.split(self.fieldSeparator):
            # check for field distribution
            if field[0] == self.groupStart and field[-1] == self.groupEnd:
                # got one; split on the group separator
                fields.append(field[1:-1].split(self.groupSeparator))
            else:
                # otherwise, just store the field name
                fields.append([field])
        # now, form all the specified addresses by computing the cartesian product
        for spec in itertools.product(*fields):
            # create a new assignment
            configuration.newAssignment(key=spec, value=value, locator=locator)
        # all done
        return


    def _processArguments(self, configuration, *args):
        """
        Interpret {args} as application commands and store them in {configuration}
        """


# end of file 
