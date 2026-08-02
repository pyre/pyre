<!-- -*- Markdown -*-
   -
   - michael a.g. aïvázis <michael.aivazis@para-sim.com>
   - (c) 1998-2026 all rights reserved
   -->

# The `pyre.externals` layer

`pyre.externals` locates the third party packages a build depends on, describes what it
found in terms a build engine can use, and resolves a set of requirements into a
configured set of installations. It answers three questions: which packages are available
on this host, where their parts are, and whether a particular set of demands can be
satisfied at once.

The layer knows nothing about any specific host. Everything it reports is derived either
from a package database it interrogates, from artifacts it finds on the filesystem, or
from configuration the user supplied. When those sources disagree, the arbitration rules
of the configuration store decide, and user configuration always wins.

## Categories, flavors, and the catalog

A **category** is a capability a build depends on: `hdf5`, `mpi`, `python`. A **flavor**
is one of the ways a category can be realized. Most categories have a single flavor, but
`mpi` has two that are not interchangeable, and `hdf5` has three, since a build of it may
be serial or aware of either message passing implementation.

Each category occupies a directory under `packages/pyre/externals/supported`. The
directory name is the category tag, which is what makes the catalog self-describing:
there is no registry to edit, and the set of supported categories is exactly the set of
directories. A category directory holds a protocol, one installation class per flavor,
and an `__init__.py` that publishes the protocol under the name `protocol`. Adding
support for a package means adding a directory.

The protocol derives from `Library`, `Tool`, or both, depending on whether consumers link
against the package, invoke it, or do both. It declares the category tag and generates
the recipes for its flavors. The installation classes are components whose traits hold
the discovered configuration: include directories, library directories, library stems,
compile time markers, and the requirements the installation imposes on other categories.

A component declares a dependency on a category with the corresponding facility:

```python
import pyre


class Simulation(pyre.application):
    """
    An application that reads and writes HDF5 files in parallel
    """

    # the data format
    hdf5 = pyre.externals.hdf5()
    hdf5.doc = "the HDF5 installation"
```

The trait is resolved when it is first accessed, and the value is a configured
installation:

```python
app = Simulation(name="simulation")
# where the compiler should look for headers
print(app.hdf5.incdir)
# and what belongs on the link line
print(app.hdf5.libraries)
```

## Recipes

A **recipe** is a declarative description of what one flavor of a category looks like on
disk. Recipes carry everything an engine needs in order to recognize an installation and
configure it, and the engines interpret them without any package specific code.

A recipe names the category and the flavor, the installation class that realizes it, and
the flavor classes the flavor answers to. It lists the headers that prove the package is
present, optional headers that extend the include path when they happen to be there, the
library stems that belong on the link line, the executables the installation should
expose, and the compile time markers consumers need. It may declare requirements on other
categories, and it may carry checks that read the contents of what was found.

Because package managers name the same package differently, a recipe also carries the
native names to look for in each database. A native entry may be a single name or a group
consisting of a lead and its companions, which is how a logical package that a
distribution splits into pieces is put back together. The lead carries the identity and
the markers; the companions contribute their contents to the interpretation, which is how
the launcher that Debian ships in `openmpi-bin` is found alongside the headers in
`libopenmpi-dev`.

The recipe for the OpenMPI flavor of the message passing interface illustrates most of
this:

```python
yield Recipe(
    # of this category
    category=cls.category,
    # the flavor tag
    flavor="openmpi",
    # realized by the openmpi installation
    factory=OpenMPI,
    # a selection group on package managers with alternatives
    group="mpi",
    # provable by the top level header
    headers=("mpi.h",),
    # contributing this library to the link line
    libraries=("mpi",),
    # the launcher executable, possibly decorated with the flavor
    binaries={"launcher": r"mpirun(\.openmpi)?"},
    # the markers for the compile line
    defines=("WITH_MPI", "WITH_OPENMPI"),
    # with database specific names where the flavor name isn't enough; debian and
    # fedora both split the launcher into runtime packages, so they ride along as
    # companions
    natives={
        "dpkg": (("libopenmpi-dev", "openmpi-bin"),),
        "rpm": (("openmpi-devel", "openmpi"),),
    },
)
```

A category with a single flavor names neither a flavor tag nor a factory beyond its
default, and the category name serves as the fallback native name, so a recipe for a
conventional library is considerably shorter.

## Package database engines

Discovery is performed by a stack of engines, ordered by the host description from most
specific to least. Each engine knows one way of finding out what is installed.

The managed engines interrogate a package database. `Conda` reads the installation
records of an environment, `MacPorts` queries the port registry, and `DPkg` and `Rpm`
consult their respective databases. They all work the same way: resolve a recipe to a
native package, gather the contents of that package and its companions, and locate the
recipe's markers among them. Because the interpretation is driven by the file list rather
than by an assumed layout, a distribution that puts headers somewhere unusual is absorbed
without special handling.

The bare engine has no database. It probes a search path for the canonical layout and
proves an installation by finding the recipe's markers under it. It is the fallback on
hosts with no package manager, and the only engine available for packages installed from
source.

An engine returns a map of trait values, or nothing when it cannot satisfy the recipe. A
recipe that expects headers must find them; a recipe that expects libraries must resolve
at least one stem. Executables are treated as optional whenever the recipe also carries
headers or libraries, since package managers routinely ship the client separately from
the development artifacts.

## Markers, proofs, and linkages

Markers establish that an installation exists. Proofs and linkages establish what kind of
installation it is.

A **proof** reads the content of a header that the discovery has already located. It
either requires a pattern to appear or forbids it, and an interpretation that fails a
proof is rejected. This settles questions the package metadata cannot answer. Both Conda
and MacPorts name every flavor of HDF5 `hdf5`, so the package name reveals nothing about
whether a build supports parallel access; the build configuration header states it
plainly, and the recipes for the parallel flavors require the declaration that the serial
recipe forbids.

A proof may instead harvest a value. When the pattern matches, a capture group is
deposited under a named trait, but a failure to match costs nothing. Version extraction
works this way. A value harvested from a header fills a gap; it never displaces a version
the package database reported, because the database is the better authority when it has
an opinion.

A **linkage** reads the shared libraries a discovered library was linked against. Where a
proof reads what a build says about itself, a linkage reads what it actually bound to.
This resolves the question a proof cannot: the build configuration header of a parallel
HDF5 confirms that the build is aware of message passing, but not which implementation it
was built against. The library names it directly, because the two implementations version
their runtimes differently, and the dependency is recorded in the library itself
regardless of what the package that shipped it was called.

A linkage votes only on what it can read. When the library is absent, available only as a
static archive, or in a format none of the readers understand, the check abstains and the
interpretation stands on its other evidence. A check that vetoed on silence would reject
installations whose headers had already proved them sound.

The three HDF5 flavors are told apart by exactly these two mechanisms. The serial recipe
forbids the declaration that the parallel ones require, and each parallel recipe names the
runtime it expects to find among the library's dependencies:

```python
# the serial flavor: the build must not be mpi aware, and it reveals its version
proofs=(
    Proof(header="H5pubconf.h", pattern=r"#\s*define\s+H5_HAVE_PARALLEL\s+1", forbid=True),
    Proof(header="H5pubconf.h", pattern=r'#\s*define\s+H5_VERSION\s+"([^"]+)"', harvest="version"),
),

# the openmpi flavor: mpi aware, and bound to the openmpi runtime
proofs=(
    Proof(header="H5pubconf.h", pattern=r"#\s*define\s+H5_HAVE_PARALLEL\s+1"),
    Proof(header="H5pubconf.h", pattern=r'#\s*define\s+H5_VERSION\s+"([^"]+)"', harvest="version"),
),
linkages=(Linkage(library="hdf5", pattern=r"libmpi\.(so\.4\d|4\d\.dylib)"),),
dependencies=("mpi[openmpi]",),
```

The dependency edge is what keeps the two selections aligned. A build that resolves
`hdf5[parallel]` and gets the OpenMPI flavor will not then be given MPICH when it resolves
`mpi`, because the flavor it received demanded otherwise.

## Requirements

A **requirement** is a demand on a category. It is the vocabulary consumers use to ask for
packages and the vocabulary recipes use to constrain their dependencies.

The text form places the category first, followed by an optional bracketed list of flavor
selectors and an optional sequence of version clauses:

    hdf5
    hdf5>=1.12,<2
    hdf5[openmpi]
    hdf5[parallel]>=1.14
    hdf5[parallel,!mpich]

A selector is answered by the flavor name or by any of the flavor classes the recipe
publishes, so `hdf5[parallel]` admits either parallel flavor while `hdf5[openmpi]` admits
only one. A selector preceded by an exclamation point excludes instead. Version clauses
are comparisons joined by commas, and the comma means conjunction: every clause must
hold. Comparison is componentwise and numeric, so `1.9` precedes `1.12`, and a component
carrying a trailing tag sorts above the bare component it extends.

A requirement that carries version clauses rejects an installation whose version could
not be determined, on the grounds that an unknown version cannot be shown to satisfy
anything. A requirement with no clauses accepts any version.

Requirements appear wherever a category is named. The `requirements` trait descriptor
coerces text into structured requirements, and understands that the comma separating list
entries is also the comma joining version clauses, so a fragment opening with a comparison
operator continues the requirement before it rather than starting a new one. An entry that
cannot be parsed is reported rather than dropped, since a dependency that vanishes
silently would subvert the resolution.

## Resolution

Resolving a set of requirements produces a **report**: the categories that were selected
with their configured installations, the categories the framework does not support, the
categories that could not be located on this host, and the categories whose accumulated
demands cannot be satisfied at once.

Requirements accumulate. Each category collects every demand made against it, whether by
a consumer or by another package's dependency edge, and a selection must honor the
conjunction of all of them. Selection walks the flavors in the order the recipes are
generated, which expresses the category's preference, and takes the first flavor that
both satisfies the accumulated demands and can be located by some engine.

Because the walk is depth first, a demand may arrive after its category has already been
selected. When the selection was made during the current resolution it is still
negotiable: it is discarded and the resolution restarts with the richer set of demands.
Since demands only accumulate, the restarts converge. When the selection was handed out by
an earlier resolution it is frozen, and the conflict is reported along with the
requirements that produced it. A conflict is distinguished from an absence: a category
that is installed but cannot satisfy the demands made of it is reported as conflicted, not
as missing.

The selections are ordered so that every package precedes the packages it depends on,
which is the order a linker requires.

```python
import pyre

# resolve a set of demands
report = pyre.externals.resolve(requested=["hdf5[parallel]", "python>=3.12"])

# the selections, in link order
for category, installation in report.selections.items():
    print(f"{category}: {installation.version} in {installation.prefix}")

# what could not be delivered
print(report.unavailable)
print(report.conflicted)
```

Resolving `hdf5[parallel]` on a host that carries the OpenMPI build selects three
categories rather than one: the parallel HDF5, the OpenMPI implementation its recipe
demanded, and nothing further. Adding `mpi[mpich]` to the same request produces a conflict
on `mpi`, reported with both requirements, rather than a silently mixed link line.

## Configuration

Discovered values are deposited into the configuration store under the name of the
installation, at a priority reserved for machine probes. That priority sits below every
form of explicit configuration, so a value a user writes in a configuration file or on the
command line displaces what was discovered, and the provenance of each value remains
available for inspection.

This is what allows an installation to be corrected without being rediscovered. A user who
knows that a package lives somewhere unusual states it, and the discovery fills in
everything else:

```yaml
# restrict this host to filesystem probing
pyre.host:
  packagers: [bare]

# and point the prober at an installation the package managers know nothing about
pyre.platforms.packagers.bare:
  searchpath: [/opt/local, /usr/local]

# the hdf5 headers are not where the layout says they should be
hdf5:
  incdir: [/opt/hdf5/include/serial]
```

## Verification

Discovery proves a recipe's markers against what a package database reported at the time.
**Verification** proves them again against what the installation says now.

The distinction matters because the two can differ. Configuration may point the include
path somewhere that holds no headers, a link line may name a library that is not there, or
an installation may have been removed after it was found. A verification pass re-reads the
markers using the effective trait values rather than the discovered ones, so it sees
exactly what a build would see. It produces an **audit** listing the categories that check
out and the complaints against those that do not.

Verification applies the same standards discovery does. An executable that a recipe names
is required only when the recipe carries no headers or libraries, because a package that
provides both was admitted without its executable in the first place, and a verification
that condemned it would contradict the engine that accepted it.

The `pyre-externals` driver exposes both operations. Invoked without arguments it surveys
every supported category and reports what is installed. Invoked with category names it
resolves those, and treats their absence as a failure, since naming a category asserts
that it ought to be present. The `--verify` option re-proves whatever was resolved. A
broken installation is always a failure, on the grounds that something claiming to be
present and being unusable is worse than something that was never installed.

```console
$ pyre-externals
python (python3): 3.14.4 in /opt/envs/skg
mpi (openmpi): 5.0.10 in /opt/envs/skg
hdf5: 2.1.0 in /opt/envs/skg
gsl: 2.8 in /opt/envs/skg
vtk: not found

$ pyre-externals --verify hdf5 mpi
mpi: ok
hdf5: ok

$ pyre-externals --supported
blas
cuda
cython
...
```

A broken installation is reported with the complaints against it:

```console
$ pyre-externals --verify hdf5
hdf5: broken
    incdir: '/opt/hdf5/include/serial' is not a directory
    unresolved header: 'hdf5.h'
```

## Binary images

The linkage checks rest on readers for the loadable binary formats, which live in
`pyre.platforms.binaries`. `MachO` reads the format used by macOS, including universal
files that carry several images, and `ELF` reads the format used by Linux and the other
Unix platforms. Both are written in Python and read the files directly, so they work
inside a container, across a mount, and on a host with no toolchain installed.

The readers expose the structure they parsed rather than only the answers derived from it.
The load command table of a Mach-O image and the program headers and dynamic table of an
ELF image are all available, so extracting a field the readers do not currently name is a
matter of reading the parsed table rather than teaching them a new format.

```python
from pyre.platforms import binaries

# read whichever format the file declares itself to be
image = binaries.read(path="/usr/lib/x86_64-linux-gnu/libhdf5_openmpi.so")

# the name it announces itself by
print(image.soname)
# and what it was linked against
for dependency in image.dependencies:
    print(dependency)
```

which reports `libhdf5_openmpi.so.310` and a dependency list that includes
`libmpi.so.40`, the name that identifies the implementation the build was made against.

Each platform names the reader for the images it loads, which is why they live alongside
the platform descriptions: `Darwin` reads Mach-O and `Linux` reads ELF, and every
distribution inherits the association. Knowing the host therefore settles the format
without inspection. The readers themselves do not depend on the host they run on. A reader
interprets what a file declares itself to be, so a Mac reads ELF images and a Linux host
reads Mach-O ones, which is what allows both formats to be exercised everywhere and what
makes a cross-compilation sysroot legible.

The platform also states how libraries are named. The two platforms version their shared
libraries at opposite ends of the filename, appending on Linux and interposing on macOS,
and both conventions are recognized. Every part of the layer that must recognize a library
filename asks the host for the pattern, so the knowledge is stated once.

## Adding a category

Create a directory under `supported` named for the category tag. It holds the protocol,
one installation class per flavor, and an `__init__.py` that publishes them.

The protocol declares the category tag and generates the recipes:

```python
# supported/zlib/Zlib.py
class Zlib(Library, family="pyre.externals.zlib"):
    """
    The compression library
    """

    # constants
    category = "zlib"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors
        """
        # get the implementations
        from .Default import Default

        # there is only one flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # realized by the generic installation
            factory=Default,
            # provable by the top level header
            headers=("zlib.h",),
            # contributing this library to the link line
            libraries=("z",),
            # and this marker to the compile line
            defines=("WITH_ZLIB",),
            # with database specific names where the category name isn't enough
            natives={"dpkg": ("zlib1g-dev",), "rpm": ("zlib-devel",)},
        )
        # all done
        return
```

The installation holds the discovered configuration:

```python
# supported/zlib/Default.py
class Default(LibraryInstallation, family="pyre.externals.zlib.default", implements=Zlib):
    """
    A generic zlib installation
    """

    # constants
    category = Zlib.category
    flavor = category
```

The directory's `__init__.py` publishes the protocol under the name `protocol`, which is
how the catalog finds it, along with the installations. A facility function in the
package's `__init__.py` lets components declare a dependency on the new category by name.

Nothing else requires modification. The category is found because its directory exists,
and every engine interprets its recipes without alteration. Note that this presumes write
access to the framework's own source: contributing a category from outside pyre is not
currently supported, and is recorded as a gap.
