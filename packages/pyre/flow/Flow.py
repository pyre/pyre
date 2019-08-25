# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# external
import itertools
# superclass
from .Producer import Producer


# declaration
class Flow(Producer, family="pyre.flow"):
    """
    A container of flow nodes
    """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default implementation
        """
        # use the default container
        from .Workflow import Workflow
        # and publish it
        return Workflow


    @classmethod
    def pyre_normalize(cls, value, node, **kwds):
        """
        Help convert {value} into a flow instance
        """
        # if {value} is not a string
        if not isinstance(value, str):
            # wouldn't know what to do
            return value

        # otherwise, we will build a flow using {value} as its name
        # get the executive
        executive = cls.pyre_executive
        # the fileserver
        fs = executive.fileserver
        # the nameserver
        ns = executive.nameserver
        # and the configurator
        cfg = executive.configurator

        # grab the node meta-data
        info = ns.getInfo(node.key)
        # extract the locator
        locator = info.locator
        # and the priority
        priority = info.priority

        # form possible filenames looking for a configuration file
        scope = itertools.product(reversed(ns.configpath), [value], cfg.encodings())
        # go through the possibilities
        for root, filename, extension in scope:
            # assemble the uri
            uri = executive.uri().coerce(f"{root.uri}/{filename}.{extension}")
            # attempt to
            try:
                # ask the fileserver to resolve it
                source = fs.open(uri=uri)
            # if something went wrong
            except executive.PyreError as error:
                # no worries
                continue

            # ask the configurator to process the stream
            errors = cfg.loadConfiguration(uri=uri, source=source,
                                           locator=locator, priority=type(priority))
            # if there were any errors, add them to the pile
            executive.errors.extend(errors)

        # this is all wrong: why pyre_default()
        # regardless of whether we were able to find a configuration, get the container
        workflow = cls.pyre_default()
        # instantiate and return it
        return workflow(name=value, locator=locator)


# end of file
