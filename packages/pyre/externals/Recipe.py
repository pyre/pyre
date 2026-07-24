# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the declarative description of a package flavor
class Recipe:
    """
    The declarative description of what a package flavor looks like on disk

    Recipes carry everything a package database engine needs in order to locate and configure
    an installation: the native package names to look for in each database, the header and
    executable markers that prove the installation is usable, the library stems that belong on
    the link line, the compile time markers, and the package categories this one depends on.
    Package category protocols publish their flavors as a sequence of recipes; engines
    interpret them without any package specific code
    """

    # meta-methods
    def __init__(
        self,
        *,
        category,
        factory,
        flavor=None,
        natives=None,
        group=None,
        headers=(),
        libraries=(),
        binaries=None,
        defines=(),
        dependencies=(),
    ):
        """
        Describe a package flavor
        """
        # the category this recipe belongs to
        self.category = category
        # the component that gets instantiated when this recipe is realized
        self.factory = factory
        # the flavor tag; single flavor categories reuse the category name
        self.flavor = flavor if flavor is not None else category
        # the map from engine names to candidate native package names
        self.natives = dict(natives) if natives else {}
        # the selection group, for package managers that support alternatives, e.g. macports
        self.group = group
        # the header paths, relative to the include directory, that prove the package is usable
        self.headers = tuple(headers)
        # the library stem patterns to resolve and place on the link line
        self.libraries = tuple(libraries)
        # the map from installation trait names to executable name patterns
        self.binaries = dict(binaries) if binaries else {}
        # the compile time markers that indicate the package is present
        self.defines = tuple(defines)
        # the package categories this one depends on
        self.dependencies = tuple(dependencies)
        # all done
        return

    # interface
    def candidates(self, manager):
        """
        Generate the ranked sequence of native package groups to look for in the database of
        the given package {manager}

        Each candidate is a (lead, companions) pair: the {lead} names the package that
        carries the identity and the hard markers of the recipe; the {companions} name
        sibling packages whose contents are folded in, for databases that split a logical
        package into pieces, e.g. debian's {openmpi-bin} carrying the launcher that
        {libopenmpi-dev} does not
        """
        # keep track of what has been offered
        seen = set()
        # the engine specific specs go first, then the flavor, then the category
        for spec in self.natives.get(manager, ()) + (self.flavor, self.category):
            # a bare name is a group with no companions
            if isinstance(spec, str):
                # unpack it trivially
                lead, companions = spec, ()
            # anything else is a (lead, *companions) group
            else:
                # unpack it
                lead, *companions = spec
                # and freeze the companions
                companions = tuple(companions)
            # skip duplicate leads
            if lead in seen:
                # and move on
                continue
            # remember this one
            seen.add(lead)
            # and offer the group
            yield lead, companions
        # all done
        return

    # debugging support
    def __str__(self):
        # identify myself by category and flavor
        return f"recipe for '{self.category}' flavor '{self.flavor}'"

    # narrow the footprint
    __slots__ = (
        "category",
        "factory",
        "flavor",
        "natives",
        "group",
        "headers",
        "libraries",
        "binaries",
        "defines",
        "dependencies",
    )


# end of file
