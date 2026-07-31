# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import importlib

# framework
import pyre

# the requirement vocabulary
from .Requirement import Requirement

# the resolution outcome
from .Report import Report

# the internal restart signal
from .exceptions import ResolutionRestart


# the manager of external package discovery
class Index:
    """
    The manager of external package discovery on this host

    The index owns the stack of package database engines assembled from the host description,
    realizes package recipes by asking each engine in turn, and deposits successful
    discoveries into the configuration store at {discovery} priority, so that user
    configuration overrides discovered values through the normal arbitration rules. It also
    provides the dependency resolver that build engines use to convert a set of requirements
    into configured installations in link order. Requirements accumulate monotonically:
    each category collects the demands made against it, selections honor the accumulated
    pool, and a demand that arrives after its category was selected either renegotiates the
    selection, when it was made during the current resolution, or reports a conflict
    """

    # singleton access
    @classmethod
    def index(cls):
        """
        Grant access to the singleton index
        """
        # if this is the first time
        if cls._index is None:
            # make one
            cls._index = cls()
        # hand it back
        return cls._index

    # meta-methods
    def __init__(self):
        """
        Prime an empty index
        """
        # the engine stack; built lazily from the host description
        self._engines = None
        # the cache of realized selections, by category
        self._selections = {}
        # the accumulated requirements: category -> {normalized spec -> requirement}
        self._demands = {}
        # the categories whose selection failure implicates their requirements
        self._blocked = set()
        # all done
        return

    # cache management
    def reset(self):
        """
        Discard the cached engine stack and selections

        Long running processes that adjust the configuration store or the host description
        after selections have been made can call this to force fresh discovery
        """
        # discard the engine stack
        self._engines = None
        # the selections
        self._selections = {}
        # the accumulated requirements
        self._demands = {}
        # and the failure diagnoses
        self._blocked = set()
        # all done
        return

    # interface
    def engines(self):
        """
        Assemble the stack of functional package database engines on this host
        """
        # check the cache
        engines = self._engines
        # if this has been done before
        if engines is not None:
            # we are done
            return engines
        # get the host
        host = pyre.executive.host
        # and the engine registry
        from .. import platforms

        # assemble the stack
        stack = []
        # go through the host's ranked engine tags
        for tag in host.packagers:
            # look up the engine foundry
            foundry = platforms.engines.get(tag)
            # if the tag is unknown
            if foundry is None:
                # make a channel
                import journal

                # and complain
                journal.warning("pyre.externals").log(f"unknown package database '{tag}'")
                # move on
                continue
            # otherwise, instantiate the engine
            engine = foundry()(name=f"pyre.packagers.{tag}")
            # if it is functional on this host
            if engine.available():
                # add it to the stack
                stack.append(engine)
        # freeze and cache the stack
        self._engines = tuple(stack)
        # hand it back
        return self._engines

    def select(self, protocol):
        """
        Realize the best recipe of the category described by {protocol} that honors the
        requirements accumulated against it, and return the configured installation, or
        {None} if no engine can locate a satisfactory one
        """
        # get the category tag
        category = protocol.category
        # check the cache
        if category in self._selections:
            # we've answered this before
            return self._selections[category]
        # gather the requirements accumulated against this category
        demands = tuple(self._demands.get(category, {}).values())
        # go through the category flavors, in order of preference
        for recipe in protocol.recipes():
            # if the requirements rule this flavor out
            if not all(
                demand.admits(flavor=recipe.flavor, tags=recipe.tags) for demand in demands
            ):
                # implicate the requirements in a potential failure
                self._blocked.add(category)
                # and move on to the next flavor
                continue
            # and the engine stack, most specific database first
            for engine in self.engines():
                # attempt to
                try:
                    # interpret the recipe against this engine's database
                    values = engine.configure(recipe=recipe)
                # if the engine is broken on this host
                except engine.ConfigurationError:
                    # try the next one
                    continue
                # if the recipe is not satisfiable here
                if not values:
                    # try the next engine
                    continue
                # get the version this interpretation reports
                version = values.get("version", Requirement.unknown)
                # if the requirements rule it out
                if not all(demand.accepts(version=version) for demand in demands):
                    # implicate the requirements in a potential failure
                    self._blocked.add(category)
                    # and try the next engine
                    continue
                # otherwise, deposit the discoveries into the configuration store
                self.deposit(recipe=recipe, values=values, engine=engine)
                # instantiate the installation; its traits bind to the deposited values,
                # unless the user has overridden them at higher priority
                installation = recipe.factory(name=recipe.flavor)
                # cache the answer
                self._selections[category] = installation
                # and hand it back
                return installation
        # if no recipe panned out, remember the failure
        self._selections[category] = None
        # and report it
        return None

    def deposit(self, recipe, values, engine):
        """
        Deposit the discovered trait {values} for {recipe} into the configuration store on
        behalf of {engine}
        """
        # get the executive
        executive = pyre.executive
        # and the configuration store
        nameserver = executive.nameserver
        # record the provenance of these values
        locator = pyre.tracking.simple(f"while interrogating {engine.about()}")
        # collect the traits the installation factory understands
        traits = {trait.name for trait in recipe.factory.pyre_configurables()}
        # discovered values with no resting place on the factory
        orphans = {}
        # go through the discovered values
        for trait, value in values.items():
            # if the factory has no resting place for this value
            if trait not in traits:
                # discarding an empty one loses nothing, but a non-empty one is a
                # recipe/factory mismatch worth reporting; set it aside
                if value:
                    # in the orphan pile
                    orphans[trait] = value
                # either way, there is nowhere to deposit it
                continue
            # deposit the value under the instance name of the installation, at {discovery}
            # priority so that any user configuration wins the arbitration
            nameserver.insert(
                name=f"{recipe.flavor}.{trait}",
                value=value,
                priority=executive.priority.discovery(),
                locator=locator,
            )
        # if there were any orphans, the recipe promises information its installation cannot
        # hold; this is an authorship error, so report the whole pile at once
        if orphans:
            # get the journal
            import journal

            # make a channel
            channel = journal.firewall("pyre.externals.discovery")
            # describe the problem
            channel.line(
                f"{recipe}: discovered information with no resting place "
                f"on '{recipe.factory.pyre_family()}':"
            )
            # itemize the orphans
            for trait, value in orphans.items():
                # one per line
                channel.line(f"    {trait}: {value!r}")
            # and complain
            channel.log()
            # in case firewalls aren't fatal: the orphans are simply not deposited; the
            # installation is missing information and downstream validation may complain

        # all done
        return

    def resolve(self, requested):
        """
        Resolve the {requested} package requirements, including their transitive
        dependencies, and return a report with the configured installations in link order

        Entries in {requested} may be text specifications or structured requirements
        """
        # normalize the request
        requested = tuple(Requirement.parse(spec=spec) for spec in requested)
        # the categories selected during this call, hence still open to renegotiation
        fresh = set()
        # requirements only accumulate, so repeated passes converge; bound them anyway
        for _ in range(self._restarts):
            # attempt to
            try:
                # make a pass over the request and its closure
                return self._pass(requested=requested, fresh=fresh)
            # if a requirement invalidated a selection made earlier in the pass
            except ResolutionRestart:
                # go again, with the richer demand pool
                continue
        # exhausting the attempts indicates a bug in the invalidation logic
        import journal

        # so build a firewall
        channel = journal.firewall("pyre.externals")
        # complain
        channel.line(f"resolution failed to converge after {self._restarts} passes")
        # with the request as the context
        channel.line(f"while resolving {', '.join(str(req) for req in requested)}")
        # flush
        channel.log()
        # in case firewalls aren't fatal, hand back an empty report
        return Report(requested=requested)

    def _pass(self, requested, fresh):
        """
        Make one resolution pass over {requested} and its dependency closure, depth first
        """
        # prime a fresh report
        report = Report(requested=requested)
        # the categories that have been fully processed
        done = set()
        # the categories currently on the visit stack, for cycle detection
        active = set()
        # the finished (category, installation) pairs, in dependency post-order
        order = []

        # the visitor
        def visit(requirement):
            """
            Visit the category constrained by {requirement} and its dependency closure
            """
            # get the category
            category = requirement.category
            # fold the requirement into the demand pool; an incompatible selection that is
            # still negotiable restarts the pass; an incompatible frozen one is a conflict
            if not self._register(requirement=requirement, fresh=fresh):
                # record the conflict, with the full demand pool as the evidence
                report.conflicted[category] = tuple(self._demands[category].values())
                # mark the category as handled
                done.add(category)
                # and move on
                return
            # if this category has been handled
            if category in done:
                # nothing further to do
                return
            # if it is currently being processed, we have a dependency cycle
            if category in active:
                # make a channel
                import journal

                # complain
                journal.warning("pyre.externals").log(f"dependency cycle at '{category}'")
                # and bail
                return
            # look up the category protocol
            protocol = self.protocol(category=category)
            # if the framework doesn't know this category
            if protocol is None:
                # record it
                report.unsupported.append(category)
                # mark it
                done.add(category)
                # and move on
                return
            # note whether the selection predates this call
            known = category in self._selections
            # realize the category
            installation = self.select(protocol=protocol)
            # if no engine could locate a satisfactory installation
            if installation is None:
                # failures the requirements are implicated in
                if category in self._blocked:
                    # are conflicts, reported with the demand pool as the evidence
                    report.conflicted[category] = tuple(self._demands[category].values())
                # everything else
                else:
                    # is simply not installed on this host
                    report.unavailable.append(category)
                # mark it
                done.add(category)
                # and move on
                return
            # selections made by this call remain negotiable until it completes
            if not known:
                # so remember this one
                fresh.add(category)
            # mark the category as in progress
            active.add(category)
            # visit the requirements this selection imposes on other categories
            for dependency in installation.dependencies:
                # recursively
                visit(dependency)
            # done with this category
            active.discard(category)
            # mark it
            done.add(category)
            # and record the selection
            order.append((category, installation))
            # all done
            return

        # visit each requested requirement
        for requirement in report.requested:
            # and its closure
            visit(requirement)

        # dependencies finish before their dependents, so reversing the finish order places
        # every package ahead of the packages it depends on: link order
        for category, installation in reversed(order):
            # record the selection
            report.selections[category] = installation

        # hand back the report
        return report

    def _register(self, requirement, fresh):
        """
        Fold {requirement} into the demand pool of its category and check it against the
        current selection

        Returns {True} when the requirement can be honored: nothing has been selected yet,
        or the existing selection satisfies it. A violated selection that is still in the
        {fresh} set is discarded and the pass restarted; a violated frozen selection cannot
        be renegotiated, reported by returning {False}
        """
        # get the category
        category = requirement.category
        # and its demand pool
        pool = self._demands.setdefault(category, {})
        # the normalized text form is the deduplication key
        spec = str(requirement)
        # if this exact requirement has been seen
        if spec in pool:
            # it has already been checked
            return True
        # fold it into the pool
        pool[spec] = requirement
        # get the current selection
        installation = self._selections.get(category)
        # if there isn't one, or selection failed
        if installation is None:
            # there is nothing to check; the requirement is honored at selection time
            return True
        # check the selection against the newcomer
        satisfied = requirement.admits(
            flavor=installation.flavor, tags=installation.tags
        ) and requirement.accepts(version=installation.version)
        # if the selection honors it
        if satisfied:
            # all good
            return True
        # if the selection is still negotiable
        if category in fresh:
            # discard it
            del self._selections[category]
            # it is no longer fresh
            fresh.discard(category)
            # and restart the pass so the category is reselected under the richer demands
            raise ResolutionRestart(description=f"reselecting '{category}'")
        # otherwise, the selection is frozen and the requirement cannot be met
        return False

    def protocol(self, category):
        """
        Map a {category} tag onto its protocol class, if the framework supports it
        """
        # look up the module and class name
        name = self._categories.get(category)
        # if the category is unknown
        if name is None:
            # report failure
            return None
        # otherwise, import the module
        module = importlib.import_module(f".{name}", package=__package__)
        # extract the protocol and return it
        return getattr(module, name)

    # private data
    # the singleton
    _index = None
    # the bound on resolution passes; requirements only accumulate, so hitting it is a bug
    _restarts = 32
    # the registry of supported categories: category tag -> module and protocol name
    _categories = {
        "blas": "BLAS",
        "cython": "Cython",
        "eigen": "Eigen",
        "fftw": "FFTW",
        "gcc": "GCC",
        "gsl": "GSL",
        "hdf5": "HDF5",
        "metis": "Metis",
        "mpi": "MPI",
        "numpy": "NumPy",
        "parmetis": "ParMetis",
        "petsc": "PETSc",
        "postgresql": "Postgres",
        "pybind11": "Pybind11",
        "python": "Python",
        "vtk": "VTK",
    }


# end of file
