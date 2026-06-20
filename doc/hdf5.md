<!-- -*- Markdown -*-
   -
   - michael a.g. aïvázis <michael.aivazis@para-sim.com>
   - (c) 1998-2026 all rights reserved
   -->

# The `pyre.h5` layer

> **Status:** working document. Seeded 2026-06-13 from a first reading of
> `packages/pyre/h5`. The current implementation is a design experiment shaped
> over a long period by real needs, *not* an implementation that followed a
> fixed blueprint. This document is being written and critiqued in parallel with
> revisiting that implementation; expect sections to be revised, contradicted, or
> marked as open questions as our understanding sharpens.
>
> **The read path is substantially implemented; the write path is largely
> design stubs.** Fleshing out the writer — so that a schema-defined data product
> can actually be realized to disk — is an active goal.

## Purpose

`pyre.h5` is a Python layer over HDF5 (sitting on the `libh5` pybind11 bindings
of the C++ `pyre::h5` library) whose goal is to make HDF5 files feel like
typed, navigable, partially-materializable object hierarchies — rather than a
bag of paths and raw buffers.

The value-added ideas, relative to working with raw `h5py`/`libhdf5`:

- **A schema can pre-exist the file.** The single most important idea. Most HDF5
  tooling (`h5py` included) is *consumer-shaped*: it assumes a file already
  exists and treats it as the source of truth. That is fine for reading, but it
  offers nothing for the genuinely hard problem — *creating* a complex file
  correctly and repeatably. `pyre.h5` lets you declare, ahead of time, what a
  file of a given kind should look like. See **Data products** below.
- **Structure is first-class and separable from access.** The shape of a file —
  its groups, datasets, and the metadata describing them (type, shape, layout) —
  can be described, inspected, and manipulated *without* holding live HDF5
  handles.
- **Partial, query-driven materialization.** A reader is not obliged to
  reconstruct the entire file in memory. A *query* — a lightweight subtree of
  structural nodes — selects which paths through the group hierarchy get
  realized under the in-memory `root`, leaving the rest untouched on disk.
- **A typed value model.** Datasets carry a dual type description (in-memory vs
  on-disk) so that reading and writing perform the right conversions, and so
  that Python code sees natural values rather than raw buffers.

## Data products

A **data product** is a *type* of HDF5 file: a named, disciplined description of
the groups, datasets, types, shapes, and layout that every concrete file of that
kind must exhibit. It is expressed as a `schema` — a class declaration whose
members are the product's groups and datasets.

The point of the product abstraction is that the schema is the **truth** for
creation. When no file exists yet, there is nothing to interrogate; the schema
*is* the specification that all realizations must mirror. Proper discipline
therefore requires the schema to pre-exist: it captures structure and dataset
metadata once, and every file written as that product conforms to it by
construction.

Crucially, a data product schema describes **everything except the numbers**.
The actual numeric payload of each dataset is supplied at realization time, from
sources that may be dynamic (computed, streamed, read from elsewhere). Realizing
a data product is thus the act of binding:

> **data product realization = schema (structure + metadata + types) + value sources → concrete HDF5 file**

This is precisely the writer's job, and the reason the write path cannot be a
mirror image of the read path: reading discovers structure, writing imposes it.

## The central asymmetry: reading vs writing

Creating and reading HDF5 files are fundamentally different problems, and the
design leans into that difference rather than papering over it.

- **When reading, the file is the source of truth.** The on-disk file already
  knows its hierarchy, the set of paths that lead to datasets, and all the
  metadata needed to describe each dataset. Reading therefore *visits* the
  hierarchy and *extracts* structure and dataset information from it. For a pure
  consumer this is the whole story, and a `schema` is overkill — which is the
  mode most HDF5 packages, `h5py` included, get stuck in. The caller may not
  care about the whole file, so a `schema` *can* still be supplied as an
  optional **query**: it frames a subtree of interest, and only the nodes along
  that subtree are filled in under the in-memory `root`. On the read side the
  schema is a bonus (constraint, conformance check), never a requirement.

- **When writing, the schema is the source of truth.** There is no file to
  interrogate, so the structure cannot be discovered — it must be declared. The
  schema *is* the specification of the data product, and the writer realizes it
  by creating the declared structure and filling each dataset from its value
  source. On the write side the schema is mandatory; it is the thing that makes
  repeatable, disciplined file creation possible at all.

This asymmetry — schema-optional on read, schema-mandatory on write — is why the
layer is split into two cooperating halves, and why the write path is *not* a
mirror image of the read path.

## The two halves: `schema` and `api`

### `schema/` — structural metadata, no live handles

`schema` is the dual-purpose parking place for **structural metadata**. Its
nodes describe *what* a group or dataset is, without being burdened by the live
HDF5 entities required to actually touch bytes on disk.

- `Descriptor` — the base structural node. Carries `_pyre_name` (the on-disk
  member name, which need not be a valid Python identifier) and participates in
  visitor dispatch via `_pyre_identify`.
- `Group(Descriptor, metaclass=Schema)` — a composite/container node. A group
  *schema* is declared as a **Python class**: subclass `schema.group`, declare
  members as class attributes, and the `Schema` metaclass harvests them.
- `Dataset(Descriptor)` — a typed leaf (`@pyre.schemata.typed`). Carries a
  `memtype` (in-memory representation) and a `disktype` (on-disk
  representation). Type-specific behavior comes from mixins in `typed/`
  (`array`, `bool`, `complex`, `enum`, `float`, `int`, `str`, `timestamp`,
  containers).
- `Schema` (metaclass) — harvests descriptors from a class declaration into
  `_pyre_localDescriptors`, `_pyre_classDescriptors`, and `_pyre_staticAliases`
  (the on-disk-member-name → Python-attribute-name map). Inheritance is honored
  by walking the MRO.
- `Inventory` — a `set` of descriptor names belonging to a group.

A schema tree is exactly what the read path accepts as a **query**: a cheap,
handle-free description of a subtree to realize.

### `api/` — live access, mirrors the C++ hierarchy

`api` is focused on **actual file access**. Its class hierarchy mirrors the C++
`pyre::h5` hierarchy:

- `Identifier` — wraps `_pyre_id`, the live `libh5` handle; knows how to
  `_pyre_close`.
- `Location(Identifier)` — adds `_pyre_location`, a path within the file.
- `Object(Location)` — adds `_pyre_layout` (a `schema.descriptor`) and
  attribute access.
- `Group(Object)` — a live container. Member access auto-dereferences datasets
  to their *value*; navigation via `_pyre_find` / `_pyre_descriptor`; uses the
  layout's alias map to translate path fragments to attribute names.
- `Dataset(Object)` — a live dataset with a value cache. The `value` property
  pulls from disk on demand and pushes on assignment, delegating the actual
  conversion to its layout. Exposes on-disk metadata (`cell`, `shape`, `space`,
  `type`, `chunk`, `filters`, `dcpl`, `dapl`, …) straight from `_pyre_id`.
- `File(Group)` — "a group at `/`". Opens local files (`_pyre_local`) or remote
  S3 objects via the ROS3 driver (`_pyre_ros3`); holds the `_pyre_uri`.
- `Datatype` — a named (committed) datatype.

### How they relate

Every live `api.Object` holds a `_pyre_layout` that is a `schema` descriptor.
The schema is the structural shadow of the live object; the live object is the
schema bound to a handle and a location. The read path *produces* both at once
(inferring the schema from disk); the write path *consumes* a live object (or
assembles one from a schema).

## Toward a write-capable schema

The current `schema` is biased toward *reading*: it grew out of describing
already-existing files (notably NISAR products, as consumed by the `qed`
visualizer), so it is good at *capturing what was discovered* and weaker at
*prescribing what must be created*. Making `schema` rich enough to write a real
product — deeper and more correlated than the toys in the test suite — is the
active design goal.

### Approach: schema-as-classes, borrowing pyre component mechanics

A product schema is declared as a set of classes, one per group, using the same
declarative style as pyre components. The cost is at least as many classes as
there are groups in the file; this is accepted as unavoidable, and is in fact
faithful — the class hierarchy mirrors the group hierarchy exactly. The payoff
is a declarative description with room for an arbitrarily deep hierarchy. The
group hierarchy is already captured well; the gaps are in the two dimensions
below.

### Dimension 1 — exhaustive per-dataset creation metadata

HDF5 **freezes** most dataset characteristics at creation time (`H5Dcreate`).
Therefore, when the writer visits a schema dataset node, that node must carry
enough information to create the dataset *even though its contents are not
available yet*. The complete set of properties HDF5 locks at creation:

- **datatype** (on-disk) — permanent
- **dataspace**: rank, current dimensions, and **maximum dimensions** — the
  latter determines extendibility; permanent
- **storage layout**: contiguous / chunked / compact — permanent
- **chunk dimensions** — required if chunked or extendible; permanent
- **filters**: gzip / szip / shuffle / fletcher32 / scale-offset / n-bit, and
  their ordering — permanent
- **fill value** and **fill time**, **storage allocation time** — permanent
- string specifics: fixed- vs variable-length, padding, character encoding

The node today carries `memtype` / `disktype`, a `shape`, and (on arrays) a
`chunk`. Still missing, and to be added exhaustively: **maximum
dimensions / extendibility, fill value, filters / compression, explicit storage
layout, allocation and fill time, and string length / encoding**.

### Dimension 2 — a reactive shape-schema

Dataset shapes within a product are strongly correlated: many datasets share
extents (in NISAR terms, azimuth / range dimensions — the HDF5 "dimension
scales" idea). Shapes therefore should not be independent literals. Instead, a
product declares a small set of **named dimensions** as `pyre.calc`
dynamic/reactive nodes, and each dataset's shape is an expression over those
nodes. Setting the product's fundamental dimensions once propagates to every
dependent dataset shape by dataflow, and gives a single locus for validating
shape consistency across the whole product.

**`shape` is the single source of dimensionality (in the h5 layer).** An h5
array descriptor declares only `shape` — a list whose length *is* the rank and
whose entries are independently:

- an `int` — a fixed extent;
- `Ellipsis` (`...`) — a free extent, unknown until realization;
- a `str` naming a dimension (e.g. `"nlines"`), resolved to a reactive
  `pyre.calc` node scoped to where the name is provided.

This unifies dimensionality, partial knowledge, and reactivity in one attribute,
with no rank/shape consistency check to enforce (and no writer bail). The general
`schemata.Array` still carries a vestigial `rank` field; the h5 layer simply
never uses it — `Inspector` infers from the dataspace `shape`, and descriptors
declare `shape`. Purging `rank` from `schemata.Array` itself is a separate,
framework-wide question (it is a public trait attribute with downstream
consumers) and is intentionally left out of this effort.

#### Declaration and resolution (implemented)

Dimensions are **declared** with the `dimension()` descriptor on the group that
*scopes* them (harvested into a bucket separate from members); a dataset
**references** them by name in its `shape`. The two are bound by a **`Resolver`**
visitor that runs eagerly in `Root.__init__`, walking the tree and populating the
root's `_pyre_shapes` (a `pyre.calc.Hierarchical`, keyed by **schema-relative**
dotted paths — deliberately decoupled from the api file path, mirroring how
NISAR's own shape database scopes independently of file location):

- each group registers its provided dimensions as **unresolved** nodes
  (`shapes.retrieve(<path>.<dim>)`) — the index is left fully unresolved for the
  realization to fill;
- each dataset's named axes are aliased to the nearest enclosing provider, found
  by **walking up** the scope (tail-stripping), recorded via `Hierarchical.alias`.

A realization then assigns values; aliases reaching a valued node compute, while
those reaching a still-unresolved node raise `UnresolvedNodeError` at read time —
the "you must supply every dimension" contract. This is what gives the
shared-vs-independent behaviour: setting `RSLC.swaths.nlines` once sizes the
length of *both* frequencies' rasters, while each `…frequencyX.nsamples` is set
independently.

An unresolved reference fires a `firewall` but then **continues** (skipping that
one alias) rather than bailing, so a user who has made firewalls non-fatal to
debug still gets a fully-built structure — a general rule here: never assume a
firewall aborted.

**Where this is headed (not yet built):**
- A **navigable get/set interface** for dimensions, mirroring the schema tree and
  api traversal (`spec.…nlines = 9000`), instead of today's raw
  `spec._pyre_shapes["RSLC.swaths.nlines"] = 9000`.
- Dataset shapes as **expressions** over dimensions (a downsampled raster sized
  `nlines // 2`, …) — the `pyre.calc` substrate already supports this; only the
  declaration syntax is missing.

## The visitors / drivers

| Class | Role |
|-------|------|
| `Inspector` | Bridge to `libh5`. Patched onto api `Group` as `_pyre_inspector`. Builds api nodes **and** their schema layouts from on-disk info. Two modes: infer (everything) and query (constrained). |
| `Reader` | Opens a file (local or `s3://` via ROS3) and delegates to the `Inspector` with an optional `query` and anchor `path`. |
| `Writer` | Persists an in-memory api `Object` tree to a file, creating groups/datasets as needed. Falls back to `Assembler` when given only structure. |
| `Explorer(Inspector)` | Visits a *live* api `Object` and extracts its `schema` descriptor (pure structure extraction). |
| `Assembler` | Turns a `schema` descriptor into an empty api `Object` tree populated with defaults. Backs `h5.product()`. |
| `Viewer` | Renders structure to a journal channel. *(not yet read in detail)* |
| `Walker`, `Validator` | *(not yet read in detail)* |

### Read path in detail

`Reader.read(path="/", query=None)`:

1. Open the file; obtain the file's `Inspector`.
2. Resolve the anchor handle at `path` (`file._pyre_id.get(...)`).
3. Hand off to `Inspector._pyre_inspect(h5id=anchor, path, query, depth)`.

`Inspector` then branches:

- **No query → infer.** `_pyre_inferObject` dispatches on the on-disk object
  type. For a group it recurses over `h5id.members()`; for a dataset it reads
  the cell type and dataspace to synthesize a typed `schema.dataset` (scalars,
  rank-1 strings, and N-d arrays are distinguished). Compound types currently
  recognize only `std::complex<float>` / `std::complex<int>`.
- **Query → constrained.** `_pyre_queryObject` walks only the members named in
  the query's alias map; missing members are silently skipped. For each
  dataset, `_pyre_consolidateSchema` reconciles the **expected** (query) and
  **actual** (on-disk) descriptors — on a cell-type mismatch it warns and
  prefers the actual; otherwise it prefers the expected.

The result is a live api `Object` tree, each node carrying both a handle and an
inferred/consolidated schema layout, with dataset values pulled lazily.

### Write path in detail

> **Status (updated 2026-06-18):** the writer loop is closed for the goal-post
> case. `Writer` now realizes a schema-defined product to disk: it mounts the
> product at the root's location (creating the prefix groups above it, e.g.
> `/science/LSAR`), and sizes each array dataset from its **resolved shape
> dimensions** rather than from a bound value. Presence is governed by
> resolution — an optional member whose dimensions are unset is treated as
> absent, so the set of dimensions a realization supplies controls both the
> extents and the *presence* of its contents. The nisar `writer/rslc.py` and
> `writer/gslc.py` tests emit real RSLC/GSLC files with programmatically
> controlled raster shapes (set one frequency's dimensions → that sub-band
> materializes at the resolved extents; leave another's unset → the whole
> sub-band is dropped), read them back by inference, and assert the on-disk
> shapes and the dropped band. The earlier scalar/string round-trip
> (`api/writer.py`) still passes unchanged. Per-type `_pyre_pull` / `_pyre_push`
> leaves exist for every type (`Bool`, `Float`, `Enum`, `String`, `Strings`,
> `Integer`, `Complex`, `Array`). What remains deferred: actually *binding*
> numeric payloads from (possibly dynamic) value sources (the writer creates
> fill-valued rasters and flushes a value only when one is bound), `listOf*`-
> driven presence and auto-derivation, attributes (`_pyre_createAttribute` is
> empty), partial/tile writes, file-to-file transfer (see the dated note in
> `typed/Array.py`), and chunk/filter derivation.

Conceptually, realizing a data product is a binding pipeline:

1. **Schema** — the data product definition pre-exists.
2. **Assemble** — `Assembler` turns the schema into an in-memory api `Object`
   tree, populated with defaults and carrying each node's layout.
3. **Bind values** — the actual numeric payloads, from their (possibly dynamic)
   sources, are injected into the assembled datasets.
4. **Persist** — `Writer` traverses the bound tree, creates the declared
   structure on disk, and flushes each dataset's value through its layout.

As implemented, `Writer.write(data=None, query=None)`:

1. If only `query` (structure) is given, materialize an empty `data` object via
   `Assembler`.
2. Read the product's shape index off `data._pyre_layout._pyre_shapes` (a plain
   group has none → `None`), and compute the mount depth from the root's
   location. Create the prefix groups above the mount (`/science`, `/science/
   LSAR`) on the destination handle.
3. Traverse `data`, visiting groups and datasets, threading the `shapes` index
   and the mount `depth` so each node's location can be rendered schema-relative
   (dotted, mount-stripped) to key into the index.
   - **Groups:** an optional group whose *provided* dimensions are all
     unresolved is skipped (absent this realization); otherwise reuse-or-create
     it and recurse.
   - **Array datasets** (those naming string dimensions, in a tree that has a
     shape index): resolve each axis — `int` → fixed, `Ellipsis` → free (0 for
     now), name → the resolved value via the alias the `Resolver` registered at
     the dataset's path. If a named axis is unset, an optional dataset is
     skipped and a required one fires a fire-and-continue firewall. Create at
     the resolved extents with the layout's on-disk type; flush a value only if
     one is bound, otherwise leave the dataset fill-valued.
   - **Scalars / dynamic containers / value-shaped arrays:** unchanged — write
     via `_pyre_describe()` + `_pyre_write`, only when a value is bound.

Open mechanics still deferred (called out in the status block above): where
value sources attach and how numeric binding actually works; `listOf*`-driven
presence; attribute creation; how chunking and filters are derived from the
schema; and whether an existing file is reconciled against the product schema
rather than blindly extended.

## Write path: creation vs access property lists

HDF5 configures a dataset through property lists. Two matter for the write path,
and they split exactly along the schema-fixed vs runtime-tunable line:

- **DCPL — dataset *creation* property list** (`H5::DSetCreatPropList`). Frozen
  at `H5Dcreate`: storage layout, chunk shape, filters, fill value + fill time,
  allocation time. These define the product's on-disk form, so **they belong in
  the `schema`** as per-dataset creation metadata (Dimension 1). Every
  realization of the product must reproduce them.
- **DAPL — dataset *access* property list** (`H5::DSetAccPropList`). Set per
  open, affects performance not persistence: the chunk cache (slots, bytes, w0).
  **Runtime-tunable, not part of the schema** — the user supplies it when
  opening, per workload. (`DXPL`, the per-call transfer property list — e.g.
  collective MPI-IO — is a third runtime category, also outside the schema.)

So the rule: **DCPL properties become schema descriptor metadata; DAPL/DXPL stay
as runtime arguments to the reader/writer.**

### Binding completeness (audit 2026-06-14)

The bindings live in `extensions/h5`; `DCPL`/`DAPL` are the HDF5 C++ classes, so
anything they expose but the bindings omit is a pure pybind gap.

- **DAPL** — `getChunkCache`/`setChunkCache` are bound; effectively complete for
  common use.
- **DCPL** — bound: alloc time, chunk, fill *time*, layout, `getFilters`,
  `setDeflate`/`setSzip`/`setNbit`. **Missing, and worth adding before the write
  path leans on creation metadata:**
  - `setFillValue` / `getFillValue` — the important gap; only fill *time* is
    bound, so there is no typed way to set a fill *value* today. (The generic
    `PropList.__setitem__` is string-typed and not a substitute.)
  - `setShuffle`, `setFletcher32`, `setScaleoffset` — filters absent from the
    pipeline bindings.

## Type system: `memtypes`, `disktypes`, `typed`

- `disktypes/` — on-disk datatype descriptors (`Integer`, `Float`, `String`,
  `Array`, `Compound`, `Enum`).
- `memtypes/` — in-memory cell types, including a rich set of complex and
  fixed-width integer/float variants (`Int8`…`Int64`, `UInt*`, `Float`,
  `Double`, `Complex*`).
- `typed/` — the dataset type mixins that give a `schema.dataset` its
  value-processing behavior (`process`, `_pyre_pull`, `_pyre_push`, default
  values, dataspace description).

*(These three packages are noted here for completeness; their internals have not
yet been read in detail.)*

## Open questions / candidates for critique

These are first-pass observations, to be confirmed or discarded as we revisit
the implementation:

- **Read/write reconciliation asymmetry.** The read/query path reconciles
  expected-vs-actual schemas (`_pyre_consolidateSchema`); the write path only
  checks for name existence. Should writing perform analogous reconciliation
  against an existing file's layout?
- **Stubs / NYI.** `Object._pyre_createAttribute` is an empty stub; string-type
  inference in the `Inspector` carries an explicit "how does `h5type` affect the
  inference?" NYI note; `Writer` has a "what to do with the dapl chunk cache
  values?" note.
- **Parallel hierarchies.** `schema.Group` and `api.Group` both carry their own
  `_pyre_identify` / alias / find machinery. How much of this is essential vs
  incidental duplication?
- **Mismatch handling severity.** On a type mismatch the query path *warns* and
  proceeds with the actual type; the comment itself wonders whether this should
  be an error.
- **`Swath`/`Grid` common base (deferred).** The radar `Swath` and geocoded
  `Grid` per-frequency groups share structure — the polarization list, the SLC
  channels, and the per-frequency `nsamples` dimension. A common base would DRY
  this up, but no satisfactory name has surfaced, so for now they stay
  independent (each composing the shared `SLC` datum directly). Their MRO is left
  unsettled deliberately; it does not block the current work.

## The `nisar` sandbox

Exploration of write-capable schemas happens in a self-contained, buildable
project under `examples/h5/nisar`, with the real NISAR data products as the
canonical (eventually large and deep) proving ground — started small and grown
incrementally.

```
examples/h5/nisar/
├── .mm/
│   ├── nisar.mm          # project: declares the package and the test suite
│   ├── nisar.pkg         # package config; root = pkg/nisar/
│   └── nisar.pkg.tests   # test-suite config; depends on nisar.pkg
├── pkg/
│   └── nisar/
│       ├── __init__.py   # registers the package; re-exports pyre + pyre.h5
│       └── meta.py.in    # version/metadata template (expanded by mm)
└── tests/
    └── nisar.pkg/
        └── sanity.py     # imports nisar; silence = pass
```

It is a pure-Python project: no `lib`/`ext`. External dependencies (notably
`pyre` itself) are not declared to `mm` — Python packages may simply fail at
runtime if a dependency is missing. Building from inside the sandbox installs
`nisar` as a sibling package in the shared `pyre/hdf5`-branch prefix
(`…/packages/nisar/`), alongside `pyre`, without disturbing it.

The authoritative direction of truth: NISAR products today have schemas
expressed as XML in a non-public repository. The goal here is to **invert**
that — make the live, executable, verifiable Python the authoritative schema,
and derive any other representation (XML included) from it. That inversion also
gives us a completeness yardstick as the exercise deepens.

### Product schema organization

Two reduced products — RSLC and GSLC — exercise the reuse granularities.
Everything lives under the `schema/` package (a mock-up of what a third party
writes, *from* `h5.schema`; the name `products` is reserved for eventual on-disk
accessor classes), which separates the reusable building blocks from the concrete
products, one class per file. Code refers to the framework as `import nisar` and
fully-qualified `nisar.h5.schema…` / `nisar.constraints…` at use sites.

```
pkg/nisar/schema/
├── descriptors/        # custom dataset descriptors (more to come)
│   └── SLC.py                  # the SLC datum: a 2d complex raster, shape=[nlines, nsamples]
├── mixins/             # reusable group structures
│   ├── common/                 # required of ALL products
│   │   ├── Identification.py      # band-level identification (missionId defaults to "NISAR")
│   │   └── LSAR.py                # the L-band base: mounts /science/LSAR via location=
│   ├── radar/                  # the radar-geometry family
│   │   ├── RadarCoordinates.py    # product group shared by RSLC, RIFG, RUNW, ROFF
│   │   ├── Swaths.py              # provides nlines (shared azimuth); frequencyA/B (Swath); zeroDopplerTime
│   │   └── Swath.py               # a frequency sub-band: provides nsamples; SLC channels; slantRange
│   └── geo/                    # the geocoded family
│       ├── GeoCoordinates.py      # product group shared by GSLC, GUNW, GOFF, GCOV
│       ├── Grids.py               # the grids group: frequencyA/B (Grid)
│       └── Grid.py                # a frequency sub-band: provides nlines+nsamples; SLC channels; x/yCoordinates
├── rslc/               # RSLC(LSAR){ RSLC = RadarCoordinates() } + a fixed-productType Identification
└── gslc/               # GSLC(LSAR){ GSLC = GeoCoordinates() } + a fixed-productType Identification
```

The sharing is **orthogonal**, which is what makes the factoring clean:

- **Band** (`mixins/common`) — every product is rooted at a band. `LSAR` mounts
  at `/science/LSAR` (via the `location` kwarg) and carries the band-level
  `identification`; products subclass it. A future `SSAR` base is the S-band
  peer.
- **Datum** (`descriptors`) — the `SLC` datum, a one-class-per-file descriptor
  (`class SLC(h5.schema.array)`) that fixes the cell type to complex and the
  shape to the two named dimensions `["nlines", "nsamples"]`. Shared by the
  per-frequency groups of *both* RSLC and GSLC.
- **Coordinate family** (`mixins/radar`, `mixins/geo`) — `RadarCoordinates` is
  the product group shared by all radar-geometry products (RSLC, RIFG, RUNW,
  ROFF); `GeoCoordinates` by all geocoded products (GSLC, GUNW, GOFF, GCOV).
  Within each, the per-frequency group is `Swath` (radar) or `Grid` (geo) —
  independent for now, their common base deferred (see Open questions).

A product root carries its coordinate-family group as a descriptor **whose
attribute name is the product type** — `RSLC(LSAR)` declares `RSLC =
RadarCoordinates()`, mounting the product group at `/science/LSAR/RSLC`.

**Dimensions are declared, resolution is pending.** Each group declares the
shape dimensions it *provides* as `dimension()` descriptors (harvested apart from
members): `Swaths` provides `nlines` (shared azimuth), `Swath` provides
`nsamples` (per-frequency range), and `Grid` provides both (geocoded grids vary
both extents per frequency). Datasets *reference* dimensions by name in `shape`
(`SLC` → `["nlines", "nsamples"]`, `slantRange` → `["nsamples"]`,
`xCoordinates`/`yCoordinates` → `["nsamples"]`/`["nlines"]`). The down-walk that
resolves those names against the root's `_pyre_shapes` index is the next piece;
see "Dimension 2".

> **First-pass caveat.** `Swath` and `Grid` currently carry the SLC channels
> directly, so they are really the *SLC* per-frequency groups; the non-SLC
> radar/geo products (RIFG, GUNW, …) will need their own per-frequency groups (or
> `Swath`/`Grid` become SLC-specific). `RadarCoordinates`/`GeoCoordinates`
> likewise still assume SLC imagery for now.

### Optional members and `listOfFrequencies`

A NISAR product carries one or both frequency sub-bands, `frequencyA` and
`frequencyB`. Two complementary mechanisms express this:

- **`optional` (a descriptor marker).** Declaring a descriptor normally
  *contracts* its presence; marking it optional relaxes that — "this member may
  be absent." Both `frequencyA` and `frequencyB` are declared on the
  `swaths`/`grids` group as `frequency(optional=True)`. Implemented as an
  `optional` keyword on `schema.Descriptor.__init__`, stored as `_pyre_optional`
  (default `False`), so it works uniformly for groups and datasets.
- **`listOfFrequencies` (per-file truth).** A `strings` dataset on the
  `identification` group naming the sub-bands actually present in a given file —
  a subset of `{"A", "B"}`.

Together: `optional` declares what *may* be present across all files of the
product type; `listOfFrequencies` declares what *is* present in one file. Keeping
the two consistent (only list what exists, only create what is listed) is a
reactive concern, related to the shape-schema (Dimension 2) and not yet wired.

The **same pattern recurses** one level down: each per-frequency group (`Swath`
or `Grid`) carries a `listOfPolarizations` (a non-empty subset of
`{"HH","HV","VH","VV"}`) and declares all four polarization channels as
`optional` `SLC` datums. So `listOfPolarizations` is to the channels what
`listOfFrequencies` is to the frequency sub-bands.

Each product has its own self-contained test driver (`tests/nisar.pkg/rslc.py`,
`gslc.py`) that asserts its structure and constraints and emits a `schema.Viewer`
rendering to a per-product **debug** channel (`nisar.schema.<type>`) — silent
on success, activatable to visualize the tree. Adding a product means adding a
driver, never editing an existing one.

### Constraints (on datasets only)

Datasets can carry **constraints** — `pyre.constraints` predicates that a value
must satisfy. They are enforced by the dataset's `process()`: after the value is
coerced to the dataset's type, each constraint is applied in turn and raises
`ConstraintViolationError` on a violation. `None` (an unset value) is left alone,
with no coercion or constraint check.

```python
listOfFrequencies = h5.schema.strings()
listOfFrequencies.constraints = [
    constraints.isSubset(choices={"A", "B"}),   # must be drawn from {A, B}
    constraints.isNotEmpty(),                    # and at least one must be listed
]
```

**Decision: constraints live on datasets, not groups.** The h5 `Dataset`
(`@pyre.schemata.typed`) already has a typed value pipeline (`process` →
`coerce`), so a `constraints` list slots naturally onto it and is inherited by
every typed dataset. Groups carry no value, so there is nothing for a constraint
to validate; group-level constraints (e.g. cross-member consistency rules) are
not supported. This is accepted for now — no compelling group-level constraint
has surfaced — and can be revisited if one does.

`isNotEmpty` (a `NonEmpty` constraint) was added to `pyre.constraints` for this;
`isSubset` already existed.

**The band prefix and the `location` mount.** Every NISAR product lives under
`/science/<band>SAR` — `/science/LSAR` for the JPL L-band instrument,
`/science/SSAR` for the ISRO S-band instrument. A `Science` group cannot declare
both bands as members, because **declaring a descriptor contracts its
presence** — that would force every file to contain both bands. Instead, a band
base (`LSAR`) carries its own absolute mount point and products subclass it; an
`SSAR` base can be added later the same way, leaving the namespace open rather
than over-contracted.

The mount point is declared with a `location` class keyword consumed by the
`schema` metaclass:

```python
class LSAR(h5.schema.group, location="/science/LSAR"):
    identification = Identification()

class RSLC(LSAR):          # inherits the /science/LSAR mount
    ...
```

`location` is meaningful **only at the root** of a product tree: it is the one
node with no binding attribute to derive its path from. Every interior node's
mount is determined by the attribute name its descriptor is bound to (via
`__set_name__`). Subclasses inherit the mount unless they redeclare it; ordinary
groups default to `None`. (Implemented on `schema.Schema.__new__`, stored as
`_pyre_location` on the descriptor.)

Two conventions established here:

- **Per-product specialization of shared groups.** A product that fixes a field
  (e.g. `productType`) **redeclares** the descriptor in a local `Identification`
  subclass rather than mutating the inherited one — the inherited descriptor is
  a shared class attribute, so mutating it would leak across products.
- **Product subpackages, lowercase re-exports.** Each product's parts live in a
  subpackage (`rslc/`, `gslc/`) and need no name prefixes (`Swaths`, `Grids`,
  `Identification`). Re-exports stay lowercase (`from nisar.schema.rslc import
  rslc`); the product class is **not** lifted into `schema/__init__` under the
  same name as its subpackage, to avoid import-order-dependent attribute clashes.
- **The `nisar` namespace re-exports `pyre`.** Modules do `import nisar` and use
  fully-qualified `nisar.h5…` / `nisar.constraints…` at the point of use, rather
  than `from nisar import h5` — pulling the pyre symbols into the `nisar`
  namespace is the whole point of re-exporting them, and qualified names show
  provenance where the symbol is used.

Open naming/design items:

- The radar `Swath` / geo `Grid` per-frequency groups want a common base, but no
  satisfactory name has surfaced, so their MRO is deferred (see Open questions).
- **Freezing**, not just defaulting, a specialized field (e.g. nailing
  `productType` so it cannot be reassigned) is desired but not yet wired. The
  likely mechanism is `pyre.calc.Const` at the value layer; it needs design
  before it can be attached to a schema descriptor.

## Roadmap and sequencing

Two efforts are in flight; they are deliberately ordered.

1. **Close the writer loop (done, 2026-06-18).** The write path realizes a
   schema-defined data product to disk. **Goal post — met:** the nisar
   `writer/rslc.py` and `writer/gslc.py` tests emit RSLC/GSLC files carrying
   per-frequency rasters whose **shape is under programmatic control** (set a
   frequency's dimensions on `_pyre_shapes`, the rasters materialize at the
   resolved extents; leave another frequency's unset, the whole sub-band is
   dropped), ready to seed `qed` performance measurements. This exercises the
   schema → assemble → persist pipeline end to end, including the reactive
   shape-schema (Dimension 2). Still open within this effort: numeric value
   binding, `listOf*`-driven presence, and attributes (see the write-path
   status block).

2. **Decouple pyre from the HDF5 C++ layer (next).** Replace the dependency on
   the `H5::*` C++ API with a thin, pyre-owned `pyre::h5` layer over the HDF5 C
   API. Deferred until the writer loop is closed; the binding gaps that motivate
   it (no `setScaleoffset`, no native complex / float16 predefined types in the
   C++ wrapper) are not on the critical path for the writer.

## Replacing the HDF5 C++ layer (assessment, 2026-06-14)

A standing question: HDF5's own C++ layer feels unmaintained and visibly lags
the C API. Should pyre own a thin C++ layer over the C API instead?

**What the HDF5 C++ layer is.** ~20k lines (`c++/src`) covering the full API, but
mechanically thin — every method is one C call plus throw-on-error, atop a
per-class exception hierarchy. It lags the C API: the `setScaleoffset`, native
complex, and float16 gaps hit this session are all present in C, absent in C++.
(Reference checkouts: `~/forks/hdf5`, `~/github/hdf5`; C++ layer in `c++/src`.)

**pyre's actual dependency surface (the number that matters).** pyre's whole h5
footprint is ~4.7k lines of pybind (`extensions/h5`) + ~660 lines of grid-pull
(`lib/pyre/h5`). It touches ~26 `H5::` classes, but 161 of those references are
`H5::PredType` — i.e. predefined-type *constants* (`H5T_NATIVE_*`), plain C
macros needing no wrapping, only exposure. The real surface is ~10 core classes
and **~69 distinct methods**, each a one-line C call.

**Effort to roll our own.** Moderate, not a 20k-line bite — we reimplement
pyre's subset: an RAII `Identifier` base, then File / Group / DataSet /
DataSpace / Attribute / the DataType hierarchy / the property lists. ~69 thin
methods, with errors flowing through `journal` (deleting the `H5::*Exception`
hierarchy) and predefined types exposed as C constants (deleting the 161-ref
`PredType` machinery). Estimate ~2–3k lines of modern pyre C++. One genuinely
careful piece: `hid_t` lifetime/refcounting RAII (~one class). One subtle piece:
datatype memory↔disk mapping — already partly done in `lib/pyre/h5` and the
`typed/` mixins.

**Payoff.** New datatypes/filters become one-line additions; errors are
pyre-native; the object model can fit the schema/api split directly; no more
waiting on the C++ wrapper.

### Phase-1 plan (a de-risking spike) — DONE 2026-06-19

Build `pyre::h5` class-by-class *behind* the existing pybind layer, repointing
bindings one class at a time, with the existing h5 test suite as the safety net —
never a big-bang rewrite. Phase 1 validated the approach on the trickiest
foundation plus one thin leaf:

1. **`Identifier` (RAII core).** `lib/pyre/h5/Identifier.{h,icc,cc}` wraps `hid_t`
   with reference-counted ownership over the C API: adopt-on-construct (a fresh
   handle carries one reference we own), `H5Iinc_ref` on copy, `H5Idec_ref` on
   destruction/`close`, steal on move. `valid()`/`refcount()` via
   `H5Iis_valid`/`H5Iget_ref`; failures go to a `firewall_t`. Sentinels like
   `H5S_ALL` are inert (`H5Iis_valid` is false), so wrapping them never refcounts.
2. **`DataSpace` (a self-contained leaf).** `lib/pyre/h5/DataSpace.{h,cc}` derives
   from `Identifier`; ~24 methods (extent, selection, hyperslabs, point lists),
   each a thin C call with marshalling done in the class and errors via
   `error_t`. A faithful reimplementation of the H5:: surface the binding used.
3. **Repoint the `DataSpace` binding** — `extensions/h5/external.h` now aliases
   `DataSpace = pyre::h5::DataSpace`; the binding calls the pyre methods, with the
   Python-facing names/signatures unchanged.

**The bridge pattern (transitional).** While `Group`/`DataSet`/`Attribute` are
still `H5::`, the few sites where a pyre `DataSpace` meets a not-yet-converted
`H5::` method bridge through the raw handle: `H5::DataSpace(space.id())`. That
constructor *increments* the refcount, and the temporary decrements on
destruction, so the bridge is balanced and ownership is unaffected. Sites:
`Group::create` (the `space` arg), `attributes.icc::createAttribute` (covers all
attribute-bearing objects), and `data.icc`'s `.space` property (copies the
returned `H5::` space into a pyre one via `H5Scopy`). `DataSet`'s internal
string-I/O dataspaces were pinned to `H5::DataSpace` explicitly. Each bridge is
deleted when its `H5::` neighbor is converted.

**Build wiring.** `lib/pyre/h5/*.cc` now compile into `pyre.lib`, so the library
gains an hdf5 dependency *only when hdf5 is available* — `.mm/pyre.mm` adds
`pyre.lib.directories.exclude += h5` when it is not, mirroring the existing
conditional `pyre.lib.extern`. The `h5` subtree is relative to the lib root.

If Phase 1 holds up, proceed with the remaining classes, each its own staged
swap. The order is **leaf-first** rather than the structural classes first: the
property lists and the DataType hierarchy are arguments to `create`/`open`, so
converting them before File/Group/DataSet means the structural cluster's calls
take pyre arguments natively instead of needing bridges.

### Phase 2 — property lists — DONE 2026-06-19

The property lists form an **atomic** cluster: each is bound as
`py::class_<DAPL, PropList>`, so pybind needs the C++ base relationship — the base
and all seven derived lists must convert together. `lib/pyre/h5/` now has
`PropList` (the generic base over the C API: `numProps`/`exists`/`property`/
`setProperty`/`removeProperty`/`propertySize` via `H5Pget_nprops`/`H5Pexist`/
`H5Pget`/`H5Pset`/…) plus `DAPL`, `DCPL`, `DXPL`, `FAPL`, `FCPL`, `LAPL`, `LCPL`,
each a thin set of `H5Pget_*`/`H5Pset_*` calls. The base default-constructs to
`H5P_DEFAULT`; each derived default-constructs a fresh list via
`H5Pcreate(H5P_<CLASS>)` and exposes `theDefault()` wrapping `H5P_DEFAULT` (the
Python `default` static). `setScaleoffset` is now a first-class method (no longer
a C-API workaround), and the ros3 driver config lives on `FAPL`.

New bridges (transitional, deleted when neighbors convert): the create/open
paths that still call `H5::` methods take pyre lists by `id()` —
`Group::create` (dcpl/dapl), `File` construction (fcpl/fapl), and
`createAttribute` (acpl). The reverse — `DataSet.dcpl`/`.dapl` and
`File.fcpl`/`.fapl`, which return a list to Python — copy the `H5::` list into a
pyre wrapper via `H5Pcopy`. Default arguments use `theDefault()` (derived) or a
default-constructed base `PropList` (the acpl), both wrapping `H5P_DEFAULT`.

The cluster was later moved into its own namespace, `pyre::h5::properties`
(mirrored by `lib/pyre/h5/properties/`), parallel to `types`. The acronyms
(`DAPL`…`LCPL`) are kept — they are HDF5-canonical and a namespace can't make them
clearer — but the base `PropList` becomes `properties::List` (no
`properties::PropList` stutter). `api.h` publishes descriptive aliases —
`pyre::h5::properties::{list_t, dataset_access_t, dataset_creation_t,
dataset_transfer_t, file_access_t, file_creation_t, link_access_t,
link_creation_t}` — and the binding layer keeps its acronym spellings
(`using DAPL = pyre::h5::properties::DAPL;`) so the registered Python class names
are unchanged.

### Phase 3 — datatypes — DONE 2026-06-19

The datatypes are another **atomic** cluster: the bindings encode the C++ base
relationships (`AtomType : DataType`; `IntType`/`FloatType`/`StrType` : `AtomType`;
`CompType`/`EnumType`/`ArrayType`/`VarLenType` : `DataType`), so the base and all
nine derived classes convert together. `lib/pyre/h5/` now owns `DataType` (the
generic base over the C API: `cell`/`bytes`/`setBytes`/`super`/`isA`/`encode`/
`decode`/`close` via `H5Tget_class`/`H5Tget_size`/`H5Tget_super`/`H5Tdetect_class`/
`H5Tencode`/`H5Tdecode`), `AtomType` (`order`/`offset`/`pad`/`precision`),
`IntType` (`sign`), `FloatType` (`bias`/`normalization`/`inpad`/`fields`),
`StrType` (`charset`/`strpad` plus the native-c-string size ctor), `CompType`
(`members`/`memberName`/`memberIndex`/`memberOffset`/`memberClass`/`memberType`/
`insert`/`pack`), `EnumType` (`members`/`memberValue`/`nameOf`), `ArrayType`, and
`VarLenType`.

The predefined types (`PredType`) remain raw C constants — `H5T_NATIVE_*`,
`H5T_STD_*`, `H5T_IEEE_*`, … — wrapped in a thin `PredType : AtomType`. These are
immutable library globals the program never owns, so `PredType` **retains**
(`H5Iinc_ref`) on construction rather than adopting, keeping its `Identifier`
bookkeeping balanced without ever driving the count below the library's. The
predefined-type modules (`native`/`std`/`big`/`little`/`alpha`/`ieee`/`intel`/
`mips`/`unix`) now publish `pyre::h5::PredType` instances built from the raw
constants; `datatype<cellT>()` and the complex compound types are likewise
rebuilt over the C API (`H5Tcopy` of the native base, `CompType` + `H5Tinsert`).

Two reference subtleties surfaced and are worth recording. (1) HDF5's
`H5::DataType(hid_t)` constructor **increments** the reference count (it shares an
existing handle), whereas pyre's `Identifier(id)` adopts. The Python-facing
`from-id` constructors therefore `H5Iinc_ref` before adopting, so the
`super → .hid → intType(hid)` pattern in `typed/Enum.py` stays safe. (2) `H5Tclose`
**refuses immutable predefined types**, so a transitional bridge cannot simply
wrap an immutable `id()` in a closing `H5::DataType` (it logs
`H5Tclose: immutable datatype`). The `borrowH5Datatype` helper copies into a fresh
**mutable** transient via `H5Tcopy`, hands that to the `H5::` wrapper, and balances
the wrapper's extra reference — used by the create/IO bridges (`Group::create`,
`createAttribute`, and the dataset `read`/`write` paths). Attribute access on
*named* datatypes is intentionally not carried over yet: it belongs to the
`H5Location` layer and returns with the `Attribute` decoupling.

The cluster lives in its own namespace, `pyre::h5::types` (mirrored by
`lib/pyre/h5/types/`), and the `Type` suffix is dropped now that the namespace
carries that meaning: `Datatype` (base), `Atom`, `Predefined`, `Int`, `Float`,
`String`, `Compound`, `Enum`, `Array`, `VarLen`. `api.h` publishes the canonical
aliases — `pyre::h5::types::{datatype_t, atom_t, predefined_t, int_t, float_t,
str_t, composite_t, enum_t, array_t, varlen_t}` (`str_t`, not `string_t`, to avoid
clashing with the `std::string` alias). The binding layer keeps its `*Type`
spellings (`using IntType = pyre::h5::types::Int;` in `extensions/h5/external.h`)
so the registered Python class names — `libh5.datatypes.IntType`, … — are
unchanged. The property lists (`DAPL`…`LCPL`) stay flat in `pyre::h5` for now; a
parallel `pyre::h5::lists` move is a candidate later.

### Phase 5 — the structural cluster — DONE 2026-06-20

`File`, `Group`, `DataSet`, and `Attribute` — the headline objects — are now
pyre-owned, flat in `pyre::h5` alongside `Identifier` and `DataSpace`. They are
**one atomic cluster**: the shared binding templates couple them. `data<objectT>`
(type/space/storage/scalar IO) serves both `DataSet` and `Attribute`, so the
memory's "DataSet then Attribute later" ordering wasn't possible — the moment
`DataSet` converts, `data<>` can't straddle a pyre `DataSet` and an `H5::`
`Attribute`. `attributes<objectT>` (attribute CRUD) serves `Group`/`DataSet`/`File`.

The C++ hierarchy mirrors the Python `api/` layer (`Location → Object → …`):
`Location : Identifier` carries the attribute interface (`H5A*`: `attributeCount`,
`openAttribute`, `createAttribute`, `hasAttribute`, `renameAttribute`,
`removeAttribute`); `Group : Location` adds the container ops (`H5G*`/`H5O*`/`H5L*`:
`memberCount`, `memberName`, `exists`, `childType`, `objectId`, `openGroup`/
`openDataSet`, `createGroup`/`createDataSet`); `File : Group` opens/creates the
file (`H5Fopen`/`H5Fcreate`) and operates its group interface on the file id;
`DataSet : Location` adds `H5D*` (type/space/storage, `read`/`write`, `dapl`/`dcpl`,
fixed- and variable-length string IO with padding-aware trimming); `Attribute :
Identifier` adds `H5A*` value access plus `name`. The Python-facing class names
(`libh5.File`, `Group`, `DataSet`, `Attribute`) are unchanged — the binding
templates were rewritten to call the pyre method names, and
`extensions/h5/external.h` repoints the aliases.

This is where the **bridges collapsed.** `Group::createDataSet`/`createAttribute`
take pyre `type`/`space`/property-list arguments natively; the dataset `read`/
`write` path calls `H5Dread`/`H5Dwrite` with the raw type id — so `borrowH5Datatype`
and the create/IO `H5::` bridges are gone, and the immutable-`H5Tclose` hazard with
them.

### Phase 6 — completion — DONE 2026-06-20

The last two threads were tied off:

- **The final bridge.** The hyperslab-selection machinery in `datasets.h` now uses
  pyre `DataSpace` throughout: the dataset's own space comes straight from
  `dataset.dataspace()`, the in-memory space is a pyre `DataSpace`, and the
  selection goes through `DataSpace::slab()` (the strided five-argument form for the
  zoom read, the two-argument form for the block read/write). `dataspace_t` is now
  `pyre::h5::DataSpace`; the last `H5::DataSpace` bridge is deleted.
- **Named-datatype attributes restored.** `types::Datatype` now derives from
  `pyre::h5::Location` (mirroring `H5::DataType : H5Object : H5Location`), so the
  whole datatype hierarchy carries the attribute interface again, and the `DataType`
  binding re-enables `attributes(cls)`. The capability dropped in Phase 3 is back.

With no `H5::` symbol left anywhere under `lib/pyre/h5` or `extensions/h5`, both
`external.h` files now include the pure C `<hdf5.h>` instead of `<H5Cpp.h>`. **The
decoupling from the HDF5 C++ layer is complete** — pyre owns its entire HDF5 surface
over the C API, and the Python-facing API never changed across all six phases.

## Binding-module restructure — DONE 2026-06-20

A follow-on cleanup, separate from the decoupling: make the Python binding module
mirror the new lib namespaces (`pyre::h5::types`, `pyre::h5::properties`) and fix
two asymmetries — the datatype bindings lived in a `datatypes` submodule with
`*Type.cc` files while the property lists were loose files registered flat at the
top of `libh5`. Unlike the decoupling, this *deliberately* changes the Python API,
so it was split by blast radius (measured: qed and qef are pure consumers, their
C++ uses only the stable aliases `datatype_t`/`dataset_t`/`read<>()`, and neither
touches `libh5.datatypes`; only the flat proplist names reach them).

The names follow pyre's typed-trait convention — lowercase, since the namespace
disambiguates the clash with Python builtins (`libh5.types.int`, like
`pyre.properties.int`).

- **Tier 1 — datatypes → `libh5.types` (pyre-only, zero external spill).** Source
  `extensions/h5/datatypes/` → `extensions/h5/types/`, binding files renamed to
  mirror the lib (`DataType.cc`→`Datatype.cc`, `IntType.cc`→`Int.cc`, …), C++
  binding namespace `pyre::h5::py::datatypes` → `pyre::h5::py::types`, and the
  registered class names lowercased: `libh5.types.{datatype, atom, predefined, int,
  float, str, compound, enum, array, varlen}` (plus the predefined-type collections
  `native`/`std`/`big`/`little`/`alpha`/`ieee`/`intel`/`mips`/`unix`). pyre's own
  `disktypes`/`Inspector` consumers updated; nothing else uses `libh5.datatypes`.

- **Tier 2 — property lists → `libh5.properties` (the cross-repo piece).** Source
  `extensions/h5/{PropList,DAPL,…,LCPL}.cc` → `extensions/h5/properties/`
  (`PropList.cc`→`List.cc`), namespace `pyre::h5::py::properties`, registered under a
  `properties` submodule: `libh5.DAPL` → `libh5.properties.dapl`, etc., base
  `libh5.properties.list`. pyre consumers (`h5/__init__.py`, `api/{File,Writer,
  Reader}.py`) updated. The qed/qef consumer updates (`libh5.FAPL` →
  `libh5.properties.fapl`) are **deferred until this PR merges** — they are pure
  mechanical find/replace and tracked in those projects' notes.

The structural objects and enums stay flat in `libh5` (`File`, `Group`, `DataSet`,
`Attribute`, `DataSpace`, the `H5*` enums) — they are the headline API and are flat
in the lib too. The C++ `extensions/h5/external.h` aliases (`DataType`, `IntType`,
`DAPL`, …) are kept as internal conveniences, so the binding bodies were untouched
beyond the namespace/registration moves.

## Glossary

- **schema / descriptor** — handle-free structural metadata describing a group
  or dataset.
- **query** — a schema subtree handed to the reader to constrain which file
  paths get materialized.
- **layout** — the `schema` descriptor attached to a live api object.
- **memtype / disktype** — the in-memory and on-disk type representations of a
  dataset, with conversion between them.
- **infer** — synthesize structure purely from on-disk information.
- **consolidate** — reconcile an expected (query) schema with the actual
  on-disk schema.

<!-- end of file -->
