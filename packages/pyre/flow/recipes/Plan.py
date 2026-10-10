# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import uuid

# support
import journal
import pyre

# the exceptions i raise
from ..exceptions import (
    NoComponentError,
    NoEngineError,
    RealizationError,
    UnresolvedProductError,
)

# my parts
from .Graph import Graph
from .registry import catalogs


# a recipe staged against a catalog
class Plan:
    """
    A recipe staged against a catalog of c++ engines: every node of the recipe has the
    declaration of the type of the c++ node that stands for it, chosen so that each factory
    takes the products its neighbors make; a plan realizes graphs for any tile shape
    """

    # the spellings of the cells that python names
    cells = {
        "float32": "float",
        "float64": "double",
        "complex64": "std::complex<float>",
        "complex128": "std::complex<double>",
    }

    # factories
    @classmethod
    def tile(cls, *, catalog, cell: str) -> str:
        """
        The declaration of the type of the tiles in {catalog} that own cells of type {cell}, as
        python names it: float32, float64, complex64, or complex128
        """
        # find it among the products the catalog can make
        return cls.find(catalog=catalog, cell=cell, makes=True)

    @classmethod
    def raster(cls, *, catalog, cell: str) -> str:
        """
        The declaration of the type of the rasters in {catalog} that wrap cells of type {cell}
        they do not own, as python names it: float32, float64, complex64, or complex128
        """
        # find it among the products the catalog cannot make
        return cls.find(catalog=catalog, cell=cell, makes=False)

    @classmethod
    def find(cls, *, catalog, cell: str, makes: bool) -> str:
        """
        The declaration of the type of the products in {catalog} whose cells are of type {cell},
        and which the catalog can make, or not, as {makes} says
        """
        # the spelling of the cell
        decl = cls.cells.get(cell)
        # go through the products of the catalog
        for entry in catalog.products.values():
            # until the one whose cells are spelled this way, and which is made the right way
            if decl is not None and entry.cell == decl and entry.makes == makes:
                # hand it off
                return entry.decl
        # a cell type the catalog has no such products of
        raise UnresolvedProductError(
            node=cell, reason=f"the catalog has no such products of {cell}"
        )

    @classmethod
    def stage(cls, *, recipe, catalog=None, products: dict | None = None):
        """
        Choose a c++ engine for every factory of {recipe} from {catalog}, so that the types of
        the products agree on both sides of every binding; {products} pins the types of some
        products, typically the sources, by the declarations of their types; {catalog} is the
        catalogs of every extension that registered one, unless told otherwise
        """
        # use the catalogs of every extension that registered one, unless told otherwise
        catalog = catalogs() if catalog is None else catalog
        # the types of the products that are pinned
        kinds = dict(products or {})
        # go through them
        for name, decl in kinds.items():
            # a type the catalog cannot make
            if decl not in catalog.products:
                # cannot be pinned
                raise UnresolvedProductError(node=name, reason=f"the catalog cannot make {decl}")
        # the factories, in the order the data flows through them
        order = recipe.ordered()
        # the products the factories that compute in python make, by name
        made = cls.run(recipe=recipe, order=order)
        # go through them
        for name, value in made.items():
            # the c++ products among them
            if isinstance(value, pyre.libpyre.flow.Product):
                # have types the catalog knows, which pin their neighbors
                kinds[name] = value.decl
        # the rest of the factories need engines
        order = [node for node in order if cls.component(node=node).pyre_engines]
        # the engines that could do the work of each one
        candidates = {node.name: cls.engines(node=node, catalog=catalog) for node in order}
        # the factory that blocked the search the deepest, in case there is no solution
        blocked = [None, -1]

        # place the factories, one at a time, backing up when one cannot be placed
        def solve(index: int, kinds: dict) -> dict | None:
            """
            Choose engines for the factories from {index} on, given the types in {kinds}
            """
            # if every factory has an engine
            if index == len(order):
                # the types are the answer
                return kinds
            # the factory to place
            node = order[index]
            # its bindings
            bindings = [b for b in recipe.bindings if b.factory == node.name]
            # go through the engines that could do its work
            for entry in candidates[node.name]:
                # its slots, by name
                slots = {slot.name: slot for slot in entry.slots}
                # an engine fits if it has every slot the recipe binds, taking the products of
                # the types the neighbors settled on
                if not all(
                    b.slot in slots
                    and kinds.get(b.product, slots[b.slot].product) == slots[b.slot].product
                    for b in bindings
                ):
                    # this one does not
                    continue
                # the types with this engine in place
                extended = dict(kinds)
                # the engine settles the types of the products it is bound to
                extended.update((b.product, slots[b.slot].product) for b in bindings)
                # and its own
                extended[node.name] = entry.decl
                # place the rest
                found = solve(index + 1, extended)
                # if they fit
                if found is not None:
                    # this is the answer
                    return found
            # nothing fits here; if this is the deepest the search has been blocked
            if index > blocked[1]:
                # remember where
                blocked[:] = [node.name, index]
            # and back up
            return None

        # stage
        kinds = solve(0, kinds)
        # if there is no way
        if kinds is None:
            # say which factory could not be placed
            raise NoEngineError(
                node=blocked[0],
                reason="no engine in the catalog takes the products its neighbors make",
            )
        # every product must have a type by now, or have been made in python
        for product in recipe.products():
            # if this one does not
            if product.name not in kinds and product.name not in made:
                # it is bound to nothing and was not pinned
                raise UnresolvedProductError(
                    node=product.name, reason="it is bound to no factory and was not pinned"
                )
        # make a plan and hand it off
        return cls(recipe=recipe, catalog=catalog, kinds=kinds, made=made)

    @classmethod
    def run(cls, *, recipe, order) -> dict:
        """
        Run the factories of {recipe} that have no c++ engines, in flow {order}, and hand back the
        products they make, by name; this is how a reader opens its file and exposes a raster
        before the engines downstream of it are chosen
        """
        # the products made so far, by name
        made = {}
        # go through the factories
        for node in order:
            # the component that does the work
            component = cls.component(node=node)
            # one with c++ engines
            if component.pyre_engines:
                # is not run here
                continue
            # the instance that does the work: the one it is pinned to, or a fresh one; pyre hands
            # back the old instance for a name it has seen before, so a fresh one gets a new name
            instance = (
                node.pin
                if node.level == "instance"
                else component(name=f"{node.name}.{uuid.uuid1()}")
            )
            # the settings the recipe records
            for setting, value in node.settings.items():
                # become its traits
                setattr(instance, setting, value)
            # its bindings
            bindings = [b for b in recipe.bindings if b.factory == node.name]
            # the values of its inputs, by slot
            inputs = {
                b.slot: made[b.product]
                for b in bindings
                if recipe.reads(binding=b) and b.product in made
            }
            # report the run on the debug channel of its family, so whoever watches it can tell
            channel = journal.debug(component.pyre_family())
            # say what is running
            channel.log(f"'{node.name}' stages {list(inputs)} in python")
            # make its outputs
            outputs = instance.pyre_stage(**inputs)
            # go through the slots it writes
            for binding in bindings:
                # skipping the ones it reads
                if not recipe.writes(binding=binding):
                    # on to the next
                    continue
                # a slot it made nothing for
                if binding.slot not in outputs:
                    # leaves its neighbors without a product
                    raise RealizationError(
                        node=node.name, reason=f"it made nothing for '{binding.slot}'"
                    )
                # file the product
                made[binding.product] = outputs[binding.slot]
        # hand them off
        return made

    @classmethod
    def component(cls, *, node):
        """
        The component class that does the work of the factory {node}: the class it is pinned to,
        the class of the instance it is pinned to, or the default of its protocol
        """
        # get the pin
        pin = node.pin
        # a factory pinned to a class
        if isinstance(pin, type):
            # uses it
            return pin
        # one pinned to an instance
        if pin is not None:
            # uses its class
            return type(pin)
        # otherwise, ask the protocol for its preferred implementation
        default = node.protocol.pyre_default()
        # a foundry
        if isinstance(default, pyre.foundry):
            # hands out the class it stands for
            default = default()
        # a protocol with no preferred implementation
        if default is None:
            # leaves the factory without a component
            raise NoComponentError(
                node=node.name, reason=f"{node.protocol} has no default implementation"
            )
        # hand it off
        return default

    @classmethod
    def engines(cls, *, node, catalog) -> list:
        """
        The entries of {catalog} that can do the work of the factory {node}, in a stable order
        """
        # the component that does the work
        component = cls.component(node=node)
        # the templates it names
        templates = set(component.pyre_engines)
        # the entries that instantiate them
        entries = sorted(
            (e for e in catalog.factories.values() if e.decl.split("<", 1)[0] in templates),
            key=lambda entry: entry.decl,
        )
        # a component the catalog has no engines for
        if not entries:
            # cannot be staged
            raise NoEngineError(
                node=node.name, reason=f"the catalog has no engines for {component.__name__}"
            )
        # hand them off
        return entries

    # interface
    def realize(self, *, shape: tuple, nodes: dict | None = None) -> Graph:
        """
        Make the nodes of my recipe for tiles of the given {shape}, apply the settings of the
        factories, and bind them; {nodes} holds products made elsewhere, such as a raster over
        the cells of a dataset, by the names of the products of my recipe they stand for
        """
        # unpack
        recipe, catalog, kinds = self.recipe, self.catalog, self.kinds
        # the nodes, by name, starting with the ones made in python when i was staged, and the
        # ones made elsewhere
        nodes = {**self.made, **(nodes or {})}
        # make the rest of the products
        for product in recipe.products():
            # skipping the ones made elsewhere
            if product.name in nodes:
                # on to the next
                continue
            # at the shape of the realization
            made = catalog.makeProduct(decl=kinds[product.name], name=product.name, shape=shape)
            # a product the catalog cannot make
            if made is None:
                # must be made elsewhere
                raise RealizationError(
                    node=product.name, reason="the catalog cannot make it from a shape"
                )
            # file it
            nodes[product.name] = made
        # make the factories
        for factory in recipe.factories():
            # the ones that compute in python ran when i was staged
            if factory.name not in kinds:
                # so skip them
                continue
            # make the rest, one at a time
            made = catalog.makeFactory(decl=kinds[factory.name], name=factory.name)
            # tell it the family of the component it stands for, which names the debug channel
            # its work is reported on
            made.family = self.component(node=factory).pyre_family()
            # apply its settings
            for name, value in self.settings(factory=factory, made=made).items():
                # one at a time
                if not made.set(setting=name, value=value):
                    # a setting the engine refuses
                    raise RealizationError(
                        node=factory.name, reason=f"its engine refuses {name}={value!r}"
                    )
            # and file it
            nodes[factory.name] = made
        # the graph
        graph = Graph(recipe=recipe, nodes=nodes)
        # go through the bindings
        for binding in recipe.bindings:
            # the ones of the factories that compute in python were honored when i was staged
            if binding.factory not in kinds:
                # so skip them
                continue
            # bind
            if not nodes[binding.factory].bind(slot=binding.slot, product=nodes[binding.product]):
                # a binding the engine refuses leaves nothing behind
                graph.dismantle()
                # and is reported
                raise RealizationError(
                    node=binding.factory, reason=f"its engine refuses to bind '{binding.slot}'"
                )
        # hand off the graph
        return graph

    def settings(self, *, factory, made) -> dict:
        """
        The settings to apply to the engine {made} for the {factory} of my recipe: the values of
        the traits of the instance it is pinned to, if any, overridden by the ones the recipe
        records
        """
        # the settings
        settings = {}
        # a factory pinned to an instance
        if factory.level == "instance":
            # carries the values of the engine's settings in its traits
            for setting in made.settings:
                # one at a time
                settings[setting.name] = getattr(factory.pin, setting.name)
        # the recipe has the last word
        settings.update(factory.settings)
        # hand them off
        return settings

    # metamethods
    def __init__(self, *, recipe, catalog, kinds: dict, made: dict, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the recipe
        self.recipe = recipe
        # the catalog
        self.catalog = catalog
        # the declarations of the types of its nodes, by name
        self.kinds = kinds
        # and the products the factories that compute in python made, by name
        self.made = made
        # all done
        return


# end of file
