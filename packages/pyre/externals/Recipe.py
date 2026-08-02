# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import re

# framework
import pyre


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
        tags=None,
        natives=None,
        group=None,
        headers=(),
        extras=(),
        libraries=(),
        binaries=None,
        defines=(),
        dependencies=(),
        proofs=(),
        linkages=(),
        **kwds,
    ):
        """
        Describe a package flavor
        """
        # chain up
        super().__init__(**kwds)
        # the category this recipe belongs to
        self.category = category
        # the component that gets instantiated when this recipe is realized
        self.factory = factory
        # the flavor tag; single flavor categories reuse the category name
        self.flavor = flavor if flavor is not None else category
        # the flavor classes this flavor answers to, e.g. {parallel}; requirement selectors
        # match against the flavor name and these tags
        self.tags = tuple(tags) if tags else ()
        # the map from engine names to candidate native package names
        self.natives = dict(natives) if natives else {}
        # the selection group, for package managers that support alternatives, e.g. macports
        self.group = group
        # the header paths, relative to the include directory, that prove the package is usable
        self.headers = tuple(headers)
        # header paths that extend the include path when present but never veto the
        # discovery, e.g. the {cccl} subtree of cuda 13
        self.extras = tuple(extras)
        # the library stem patterns to resolve and place on the link line
        self.libraries = tuple(libraries)
        # the map from installation trait names to executable name patterns
        self.binaries = dict(binaries) if binaries else {}
        # the compile time markers that indicate the package is present
        self.defines = tuple(defines)
        # the package categories this one depends on
        self.dependencies = tuple(dependencies)
        # the content checks that settle what the package metadata cannot
        self.proofs = tuple(proofs)
        # the dependency checks that settle what a build actually bound to
        self.linkages = tuple(linkages)
        # all done
        return

    # interface
    def prove(self, incdir, libdir=()):
        """
        Evaluate my content proofs against the headers under {incdir} and my linkages
        against the libraries under {libdir}, and return the harvested values, or {None}
        when any of them fails
        """
        # the values the extractors gather
        harvested = {}
        # the checks, each paired with the folders it reads
        checks = ((self.proofs, incdir), (self.linkages, libdir))
        # go through them
        for tests, folders in checks:
            # and every check of that kind
            for test in tests:
                # evaluate it
                ok, values = test.evaluate(folders=folders)
                # a failed check sinks the whole interpretation
                if not ok:
                    # so report it
                    return None
                # fold in whatever was harvested
                harvested.update(values)
        # the interpretation survives
        return harvested

    def audit(self, installation):
        """
        Re-prove my markers against the effective configuration of {installation} and
        generate a complaint for each one that no longer resolves

        The markers come from me, the paths and resolved names from the installation, so
        this honors whatever the user overrode in configuration; a discovery time check
        can only see what the package database reported
        """
        # the include directories, as the installation has them now; tool installations
        # carry no library traits at all, so every lookup here tolerates their absence
        incdir = tuple(getattr(installation, "incdir", ()))
        # every one of them must exist
        for folder in incdir:
            # or the compile line points at nothing
            if not folder.isDirectory():
                # so complain
                yield f"incdir: '{folder}' is not a directory"
        # every header marker must resolve on one of them
        for header in self.headers:
            # look for it
            if not any((folder / header).exists() for folder in incdir):
                # a marker that doesn't resolve means the package isn't usable
                yield f"unresolved header: '{header}'"

        # the library directories, as the installation has them now
        libdir = tuple(getattr(installation, "libdir", ()))
        # every one of them must exist
        for folder in libdir:
            # or the link line points at nothing
            if not folder.isDirectory():
                # so complain
                yield f"libdir: '{folder}' is not a directory"
        # every library the installation places on the link line must be there; the stems
        # are the resolved ones, so this checks what the linker will actually look for
        for stem in getattr(installation, "libraries", ()):
            # the host knows how libraries are named; the stem is a literal here, so it
            # goes in escaped
            pattern = re.compile(
                pyre.executive.host.libraryPattern(stem=re.escape(stem))
            )
            # look for a match in any of the library directories
            if not any(
                any(pattern.match(str(entry.name)) for entry in folder.contents)
                for folder in libdir
                if folder.isDirectory()
            ):
                # a stem that resolves to no file will fail at link time
                yield f"unresolved library: '{stem}'"

        # the executables the recipe cares about live under the binary directories
        bindir = tuple(getattr(installation, "bindir", ()))
        # every one of them must exist
        for folder in bindir:
            # or the executables are unreachable
            if not folder.isDirectory():
                # so complain
                yield f"bindir: '{folder}' is not a directory"
        # discovery accepts a package whose executables are missing as long as it carries
        # headers or libraries, since package managers routinely split the clients off;
        # verification honors the same rule, or it would condemn installations the engines
        # deliberately admitted. for a pure tool, the executable is the whole package
        if self.binaries and not self.headers and not self.libraries:
            # go through the traits that name executables
            for trait in self.binaries:
                # get the name the installation resolved, which the user may have overridden
                name = getattr(installation, trait, None)
                # nothing to check if the trait is empty
                if not name:
                    # move on
                    continue
                # the named executable must be in one of the binary directories
                if not any((folder / name).exists() for folder in bindir):
                    # or invoking it will fail
                    yield f"unresolved {trait}: '{name}'"

        # finally, the checks must still hold against the effective paths
        if self.prove(incdir=incdir, libdir=libdir) is None:
            # a build that no longer answers to its own recipe is misconfigured
            yield "content proof failed"

        # all done
        return

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
        "tags",
        "natives",
        "group",
        "headers",
        "extras",
        "libraries",
        "binaries",
        "defines",
        "dependencies",
        "proofs",
        "linkages",
    )


# end of file
