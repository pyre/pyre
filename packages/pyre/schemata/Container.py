# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Schema import Schema


# declaration
class Container(Schema):
    """
    The base class for type declarators that are sequences of other types
    """

    # constants
    typename = "container"  # the name of my type
    isContainer = True

    @property
    def container(self):
        """
        The default container represented by this schema
        """
        # complain that the subclass is not constructed properly
        raise NotImplementedError(
            "class {.__name__} must define a {container} type".format(type(self))
        )

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into an iterable
        """
        # get the worker to build an iterable, cast it into my container type and return it
        return self.container(self._coerce(value=value, **kwds))

    def render(self, renderer, value, workload):
        """
        Render {value} using {renderer}
        """
        # get my schema
        schema = self.schema
        # render just my name
        yield renderer.trait(name=self.name, value="")
        # go through the items
        for item in value:
            # ask my schema to render each one
            entry = ",".join(
                schema.render(
                    renderer=renderer, value=item, workload=workload, incognito=True
                )
            )
            # and put it on a separate line
            yield renderer.value(value=f"{entry},")
        # all done
        return

    # meta-methods
    def __init__(self, default=object, schema=Schema(), **kwds):
        # adjust the default; carefully, so we don't all end up using the same global container
        # checking for {None} is not appropriate here; the user may want {None} as the default
        # value; we need a way to know that {default} was not supplied: use a TYPE (in this
        # case object) as the marker
        default = self.container() if default is object else default
        # chain up with my default
        super().__init__(default=default, **kwds)
        # save my schema
        self.schema = schema
        # all done
        return


# end of file
