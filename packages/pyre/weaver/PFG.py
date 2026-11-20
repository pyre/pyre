# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the pyre package
import pyre

# my ancestor
from .LineMill import LineMill


# my declaration
class PFG(LineMill):
    """
    Support for pyre configuration files
    """

    # trait traversal hooks
    def componentStart(self, component):
        """
        Render a component
        """
        # easy enough
        yield self.place(f"{component.pyre_spec}:")
        # push in
        self.indent()
        # all done
        return

    def componentEnd(self, component):
        """
        Done processing the traits of {component}
        """
        # pop
        self.outdent()
        # leave a blank line
        yield ""
        # all done
        return

    def trait(self, name, value):
        """
        Render a trait
        """
        # easy enough
        return self.place(f"{name} = {value}")

    def value(self, value):
        """
        Render a value for a multiline trait
        """
        # easy
        return self.place(value)

    # the values of traits, which identify themselves to me through their schemata
    def _pyre_onSchema(self, schema, value, incognito=False, **kwds):
        """
        Render {value} on one line, as the text of {schema}
        """
        # get the text
        entry = schema.string(value)
        # an entry of a container
        if incognito:
            # is just its text
            yield self.value(value=entry)
            # and that's all
            return
        # anything else is assigned to its trait
        yield self.trait(name=schema.name, value=entry)
        # all done
        return

    def _pyre_onContainer(self, schema, value, workload, incognito=False, **kwds):
        """
        Render {value} with its name on a line of its own, and each of its entries on the lines
        that follow
        """
        # an entry of another container
        if incognito:
            # fits on the line of that container, as its text
            yield self.value(value=schema.string(value))
            # and that's all
            return
        # start with the name
        yield self.trait(name=schema.name, value="")
        # go through the entries
        for item in value:
            # let each one say how it is rendered as an entry
            entry = ",".join(
                schema.schema._pyre_identify(
                    authority=self, value=item, incognito=True, workload=workload
                )
            )
            # and put it on a line of its own
            yield self.value(value=f"{entry},")
        # all done
        return

    def _pyre_onMapping(self, schema, value, incognito=False, **kwds):
        """
        Render {value} on one line, in the form its text is read back from
        """
        # a mapping is rendered like any value that fits on one line
        yield from self._pyre_onSchema(schema=schema, value=value, incognito=incognito)
        # all done
        return

    def _pyre_onComponent(self, schema, value, workload, incognito=False, **kwds):
        """
        Render {value} by its specification, and add it to {workload} so its traits are
        rendered as well
        """
        # a component is known by its specification
        spec = None if value is None else value.pyre_spec
        # an entry of a container
        if incognito:
            # is just its specification
            yield self.value(value=spec)
        # anything else
        else:
            # is assigned to its trait
            yield self.trait(name=schema.name, value=spec)
        # a component that hasn't been queued yet
        if value is not None and value not in workload:
            # gets its own turn
            workload.append(value)
        # all done
        return

    # private data
    comment = ";"


# end of file
