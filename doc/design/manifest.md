<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# the manifest of an HDF5 file

A design for a C++ structure that holds the complete layout of an HDF5 file: every object, where
its bytes are, and how they sit on the pages of the file. It is built once per file, from
metadata only, and answers questions about the file without going back to the library. On top
of it, a separate layer of lenses lets a client that knows a product, e.g. a NISAR product, mark
some datasets as rasters, cubes, masks, or metadata, the way qed decides today what it can show.

The names follow the vocabulary of pyre's fleets and crews: a manifest says what is aboard and
where it is stowed, an assay tests what the chunks actually hold, and a lens is how a client that
knows a product looks at one.

Status: **proposal**. Nothing here is built.


## Where things stand

The question of how a product sits in its file is asked today by qed, in Python, in
`qed/pkg/readers/pages.py`. It walks the groups of the file through the h5 bindings, asks each
dataset for its chunk table, and computes from those tables:

- the occupancy of the pages by each dataset, and the bytes a reader moves for every byte it
  needs (`occupancy`);
- the strip of pages a raster lands on (`strip`), and what every page of the file holds
  (`filemap`);
- the state of each cell of the chunk grid: written, missing, fill (`states`);
- how often consecutive chunks on a page are neighbors on the raster (`locality`);
- what the dataset holds where there is no data, which needs reading and decoding chunks
  (`nodata`, `decode`, `shuffle`, `interpret`).

pyre supplies the raw material: `DataSet::chunkTable()` walks the chunk index once with
`H5Dchunk_iter` (pyre#280), the creation properties report the file space strategy and the page
size, `File::bytes()` the size of the file, and `File::pageBuffer()` what the page buffer has
seen. Everything above that is qed's, written for the rasters of a NISAR reader, and reachable
only from qed.

The same questions matter to anybody who reads HDF5 over a network, and the answers do not depend
on NISAR. The census of the NISAR operations bucket ran this code on tens of thousands of
products; it is slow because it is Python walking objects one call at a time, and it cannot be
reused because it is tied to qed's readers.


## The floor of HDF5

Recommendation: **all of `pyre::h5` moves to HDF5 2 as its floor**, pending an investigation of
the consequences. `lib/h5/external.h` enforces 1.14.4 today. The floor applies to the whole of
`pyre::h5` and not to the manifest alone, because the manifest lives in the same library, and a
second floor behind compile time guards would split it in two.

The reason is the native complex datatype of HDF5 2. Complex cells are stored today as compounds
with two members, `r` and `i`, which is a convention that every reader has to recognize, rather
than a type the library knows. With native complex types:

- `datatype<std::complex<float>>` and its siblings describe a complex type, instead of building a
  compound;
- the description of the cell that the manifest and the schema share has a complex class of its
  own;
- complex cells map to `complex64` and `complex128`, which are data types of the core zarr
  specification, so they cross the bridge without a convention.

The investigation settles the following, and the recommendation stands or falls with its
findings:

- **Existing products.** Products written before HDF5 2, NISAR among them, store complex cells as
  compounds, and must keep reading. The manifest and the lenses recognize both forms. Whether the
  library converts between a native complex type and a compound of two members of the same
  floating type, so that old products read into native cells, is to be confirmed.
- **Integer pairs.** The native complex types of HDF5 2 are expected to take floating components
  only. The raw samples of the L0b products are pairs of integers, which remain compounds, as
  befits pairs of samples rather than complex numbers.
- **Availability.** HDF5 2 on conda-forge, for the builds and for the feedstock of pyre; in the
  packages of the linux distributions that the docker containers and CI use, which lag; and in
  Homebrew and MacPorts.
- **Coexistence.** h5py in the same environment as pyre, since two versions of HDF5 in one
  process cause trouble.
- **The other changes of HDF5 2.** The build of the library and its installed layout, which
  affect the discovery of the package by mm and by the cmake build, and the ros3 driver, on
  which pyre's access to S3 depends.


## The manifest

`pyre::h5::Manifest` is built from an open `File` in one pass, and holds:

**The file.** Its size, the file space strategy, the page size, the free space the library
knows about (`H5Fget_freespace`, `H5Fget_free_sections`), and the versions of its superblock
and its object headers (`H5Fget_info2`).

**The objects.** Every group, dataset, and named datatype, visited once by object token
(`H5Ovisit3`), so an object reached through several hard links is one entry with several names.
Soft and external links are recorded as links and not followed. For each dataset:

- its names, its rank, its shape and its maximum shape;
- its cell: class, size, byte order, sign;
- its storage: compact, contiguous, chunked, or virtual; the shape of its chunks; its filters,
  with their flags and parameters, in the order they are applied;
- its declared fill value, with the fill time and the allocation time;
- the names and types of its attributes.

**The storage.** Every extent in the file that holds raw data, as a structure of arrays:
address, stored size, owner (the index of the dataset), position (the index of the chunk in the
grid of its dataset), and filter mask. A contiguous dataset contributes one extent, a chunked
one an extent per written chunk, and a compact one none, since it lives in its object header.
The arrays are sorted by address once, after the walk, which gives the page index: the range of
extents that start on each page, found by binary search.

Building it reads metadata only: the object headers, the chunk indices, and the superblock.
That is what makes it cheap for a file in S3, where every read is a fetch of a page.


**The grid index.** The extents sorted by address answer questions about pages. Questions about
a region of a dataset want the opposite order, so each chunked dataset also gets a dense array
shaped like its chunk grid, with an entry per cell: the index of its extent, or a sentinel for a
chunk that was never written. This is the index of a zarr shard, with the indirection through
the storage arrays instead of a copy of the address and size. Finding the chunks of a region is
then arithmetic on the grid, and the cells that hold the sentinel are the unwritten chunks,
which read back as the fill value.


## Finding the metadata

The library never keeps a list of its metadata. It finds what it needs by following addresses,
starting from the superblock at the start of the file:

- the superblock holds the address of the object header of the root group and, in versions 2
  and 3, the address of its extension, an object header whose messages hold the file space
  settings, the addresses of the persisted free space managers, and the shared message table;
- an object header holds messages; continuation messages point to further blocks of the same
  header;
- the messages of a group lead to its links, either in the header itself or, past a threshold, in
  a fractal heap indexed by a version 2 B-tree, or, in older files, to a version 1 B-tree with a
  local heap;
- the messages of a dataset hold its dataspace, datatype, fill value, filters, and layout; the
  layout message holds the address of its chunk index, which is one of a single chunk, an
  implicit index, a fixed array, an extensible array, or a version 1 or 2 B-tree;
- attributes live in the header or, past a threshold, in a fractal heap with a B-tree index;
  variable length data lives in global heap collections.

Every structure past version 1 begins with a signature (`OHDR`, `OCHK`, `TREE`, `BTHD`, `BTIN`,
`BTLF`, `HEAP`, `GCOL`, `FRHP`, `FHDB`, `FHIB`, `FSHD`, `FSSE`, `SMTB`, `FAHD`, `FADB`, `EAHD`,
`EAIB`, `EASB`, `EADB`, `SNOD`) and most end with a checksum, so a block can be recognized and
checked once its address is known. The format is published, and the addresses are stable for the
life of the file.

The public API gives part of this away:

- the token of an object, under the native connector, is the address of its object header
  (`H5VLnative_token_to_addr`), so the walk of the manifest already visits every object header
  address;
- `H5Oget_native_info` reports the size of each object header, its free space, and the sizes of
  the indices and heaps of its links and attributes, though not where they are;
- `H5Fget_info2` reports the sizes of the superblock, its extension, and the shared message
  indices; `H5Fget_free_sections` reports the free space; `H5Fget_mdc_image_info` reports the
  metadata cache image, when there is one.

What it does not give is the addresses of continuation blocks, chunk indices, heaps, and B-tree
nodes. Three ways to get them, from cheapest to most complete:

1. **Pages.** In a file with the paged strategy, metadata and raw data never share a page. A
   page with no raw extents on it, and not free, is metadata, so the accounting by page is exact
   without knowing where the blocks are. The NISAR products are paged.
2. **The flavor of each byte.** Every read the library makes through its file driver carries the
   type of what it is reading: superblock, B-tree, object header, local or global heap, or raw
   data. The logging driver records it for every byte (`H5FD_LOG_FLAVOR`), but it wraps only
   local files. A pass through driver of our own would record (address, size, type) for every
   read over any driver, including ros3; building the manifest through it touches every object
   header and chunk index, and leaves out only what the walk does not read, e.g. attribute
   values.
3. **The format.** Starting from the object header addresses the walk already has, read the
   headers, follow their continuation messages, and from the layout, link info, and attribute
   info messages, the addresses of the indices and heaps, recognizing each block by its
   signature. This is what a format checker does, and the only one of the three that is
   complete; it is also the one that has to keep up with new versions of the format.

The first is free and enough for paged files. The second is the next step if the remainder of a
page is not enough.


## The queries

With the storage sorted by address, the questions qed asks become array operations:

- **pages**: for every page, the bytes of each owner on it, the free bytes, and the remainder,
  which is metadata, since the library does not say where its metadata blocks are;
- **strip** and **occupancy** of a dataset: the pages it lands on, how full they are, whose
  bytes share them;
- **locality**: how often the chunks that follow each other on a page are neighbors on the
  raster;
- **cost** of a selection: given a set of datasets and a region of each, the chunks it touches,
  the pages those chunks land on, the bytes a reader that fetches whole pages moves, and the
  ratio to the bytes it needs. Reading one layer of a GUNW alone versus reading them together is
  this query with two selections; the read cost overlay of the quality panel is this query over
  the tiles of a view.

Each answer is a small record or a set of arrays. Nothing is cached in the manifest but the manifest
itself; a client that asks the same question repeatedly keeps the answer.


## The assay

Some questions need the data: which chunks hold nothing but fill, how well each chunk
compresses, what the raster holds where its fill says nothing. These are kept out of the manifest,
so that building one never reads raw data. `pyre::h5::Assay` takes a manifest and a policy (the
datasets to look at, and which of their chunks: all, a sample, or the candidates for fill, which
are the chunks of the smallest stored size) and reads those chunks through the library, which
applies the filters. It records, per chunk read, whether its cells are uniform and their value.
Compression needs no decoding: the stored size is in the manifest and the raw size follows from the
shape of the chunk and the size of the cell.


## The bindings

`libh5.Manifest` exposes the records as properties and the arrays as numpy views through the
buffer protocol, without copies. `pyre.h5.manifest(uri, credentials=...)` opens the file, builds
the manifest, and closes the file, for the common case of a client that wants the structure and not
the data.

A manifest is data, so it can be saved. The natural format is HDF5 itself: the arrays as datasets,
the records as compound datasets, with a version. A census is then a collection of saved
manifests, plus the reductions computed over them, and can be recomputed without returning to the
bucket.


## Ideas from zarr

Zarr keeps an array as a set of objects in a key value store, one per chunk or, with sharding, one
per block of chunks with an index of their offsets and sizes at one end. A reader computes the key
of a chunk from its coordinates and never chases metadata; a chunk that is missing is the fill
value, and writers skip the chunks that hold nothing else by default. The ecosystem around it
treats HDF5 as a source of virtual chunks: Kerchunk and VirtualiZarr find the byte range of every
chunk of an HDF5 file and write them out as a manifest, a table of (location, offset, length) by
chunk coordinates, and Icechunk stores such manifests with the checksum or modification time of
each source, split into pieces by ranges of chunk coordinates so a reader skips the pieces it does
not need.

What carries over:

- **A saved manifest is a zarr manifest.** Exporting the storage of a manifest as a Kerchunk or
  Icechunk manifest makes any HDF5 file pyre can describe readable by the zarr ecosystem without
  conversion. It costs a writer, and it answers the comparison directly: with a manifest, an HDF5
  file is a virtual zarr store.
- **Record the source.** A saved manifest keeps the size, the modification time, and the entity tag
  of the file it describes, so a client can tell when it is stale without reading the file.
- **Read chunks without the library.** With the address, size, and filters of every chunk in
  hand, a client can fetch the bytes of the chunks it needs by range, with as many requests in
  flight as the store allows, and decode them in as many threads as it has cores. The library
  serializes its calls under one lock; this is the path around it, for the filters pyre can apply
  itself: deflate, shuffle, and the fletcher checksum, which cover the NISAR products.
- **Fill is absence.** The census found writers that declare one fill value and use another, and
  so have to write every chunk of fill. Zarr makes not writing them the default. The assay
  pass reports how much a file would shrink, and how much decoding a reader would save, if it
  did the same.
- **Multiscales.** A hybrid Icechunk store (virtual chunks of the original files next to
  materialized coarser levels, rendered in the browser) is the architecture of qed with the
  pyramid kept as zarr; the lesson its authors report is the one the qed measurements found, that
  the chunking of the original products does not suit regional views. Writing the pyramid under
  the zarr multiscales convention would let other viewers use it.

Where HDF5 and pyre stand against it: one self-describing file, a richer type system, many
chunk index structures, and the paged strategy for object stores; against a format whose chunks
are independent objects, which suits parallel writers and needs no walk to find a chunk. The
manifest removes the walk for readers: one pass over the metadata, saved, and every later read is
arithmetic plus a range request. What it does not change is that writing an HDF5 file goes through
one library and one writer.


## A bridge between zarr and HDF5

A tool that moves arrays between the two formats, in both directions, built on the manifest:

- **HDF5 to zarr, virtually.** Write the manifest of a file as a Kerchunk or Icechunk manifest.
  Nothing is copied; zarr readers fetch the chunks from the HDF5 file by range. This works for
  the chunks whose filters a zarr codec reproduces. The deflate filter of HDF5 writes a zlib
  stream (RFC 1950), not the gzip container (RFC 1952) that the `gzip` codec of the core
  specification expects, so deflate maps to `numcodecs.zlib`; shuffle maps to
  `numcodecs.shuffle`, and the fletcher checksum to `numcodecs.fletcher32`. These are extension
  codecs, not core ones: zarr-python supports them, and whether other readers, such as
  tensorstore, zarrs, and zarrita, do is to be checked.
- **HDF5 to zarr, materialized.** Copy the chunks into a zarr store, unchanged when the codecs
  match and recompressed when they do not, optionally rechunked, and with the chunks of fill left
  out.
- **zarr to HDF5.** Write the arrays and groups of a zarr store into an HDF5 file with the paged
  strategy, through pyre's h5 writer and a schema, choosing the chunking and the page size, and
  declaring the fill value so chunks of fill are not written.

Attributes and dimension names map in both directions; the groups of one are the groups of the
other. The interesting part is not the copy but the choices it exposes: the chunking, the page
size, and the treatment of fill, which the manifest and the assay can evaluate before anything is
written.


## One schema for both formats

Neither format says what a product must contain. The zarr specification defines the metadata of
an array and of a group, and nothing about how they are arranged; HDF5 is the same. Both leave
structure to conventions carried in attributes: NetCDF-4 with CF and HDF-EOS on the HDF5 side,
CF as xarray writes it, OME-Zarr, GeoZarr, and the multiscales convention on the zarr side.
OME-Zarr publishes JSON Schemas for its attributes, so its metadata can be validated, but no
convention tells a writer which arrays to store and how. The closest tool in the zarr ecosystem
is pydantic-zarr, which models a hierarchy as `GroupSpec` and `ArraySpec` objects, validates an
existing store against them, and creates an empty hierarchy from them. It describes structure
only, and only in Python.

pyre's h5 schema already does more: a product is a tree of typed descriptors with names,
documentation, optional members, and dimensions, and visitors read, write, validate, and render
it. Most of it does not depend on HDF5:

- `Group`, `Dataset`, and `Dimension`, the `Schema` metaclass that harvests them, and the
  `Resolver` and `Viewer` visitors describe a hierarchy of groups and arrays, which is the data
  model of zarr as much as that of HDF5;
- the cells are the exception. `Dataset` takes a memory type and a disk type, and the disk types
  are `libh5.types` objects, so every leaf of a schema holds an HDF5 datatype;
- the storage hints are another: `typed.Array` carries a chunking strategy and builds a
  `libh5.DataSpace` for the writer;
- the visitors that move data, `Reader`, `Writer`, `Assembler`, and `Explorer`, call `libh5`
  directly.

A schema that serves both formats separates three things:

1. **The cell**, described without HDF5: class, size, byte order, and sign, with complex a
   class of its own. This is the same record the manifest keeps for each dataset, so the two
   share it. Each format maps it to its own types: an HDF5 datatype, or a zarr data type and its
   `bytes` codec. A complex cell maps to the native complex types of HDF5 2, and to `complex64`
   or `complex128` in zarr.
2. **The storage**, as plain data: the shape of the chunks, the filters or codecs, the fill
   value, and the page size where the format has one. A writer for either format reads them; a
   format that cannot honor one reports it.
3. **The visitors**, one set per format: the existing ones over `libh5`, and a reader and writer
   over zarr, which is an optional dependency and lives in its own package.

Some types do not cross. HDF5 enumerations and references have no zarr counterpart; compound
types and variable length strings exist in zarr only through its extensions of the data types,
whose support in zarr-python is to be checked. A schema that uses them is tied to HDF5, and the
zarr writer says so when it is asked to write one. Complex cells stored as compounds of two
members are among them, which is one reason for the floor of HDF5 2.

With one schema, the bridge copies a product in either direction through the same description,
the lens built from a schema checks a zarr store against the product specification as it checks
an HDF5 file, and the specification of a product such as NISAR is written once. `pyre.h5.schema`
is a published interface with clients outside the repository, so the separation keeps its
current spelling working: the HDF5 disk types remain valid descriptions of a cell.


## Cloud storage

Status: **open**. This section collects what is known and is expected to change as the work
proceeds.

**What pyre has.** pyre reads HDF5 from S3 through the ros3 driver of the library, which pyre
requires at 1.14.4 or newer, the release that repaired it. `pyre.h5.read` accepts an `s3://`
uri and a dictionary of credentials with the region, the access key, the secret key, and the
session token; an empty key and secret open the object anonymously. The driver reads only, and
fetches by range. `File._pyre_ros3` builds the address of the object as
`https://{bucket}.s3.{region}.amazonaws.com/{key}`, so pyre reaches AWS and nothing else: the
services that speak the S3 protocol at other endpoints, such as Cloudflare R2, MinIO, Ceph, and
Wasabi, need the endpoint to be configurable, and Google Cloud Storage and Azure Blob Storage are
not reachable at all. The ros3 driver of HDF5 2 is part of the investigation that the floor of
HDF5 2 calls for.

**What zarr has.** Zarr is defined over an abstract key value store, and storage is whatever
implements it. zarr-python 3 has local, memory, and zip stores; `FsspecStore`, which reaches S3
and the services compatible with it through `s3fs`, Google Cloud Storage through `gcsfs`, Azure
Blob Storage and ADLS through `adlfs`, and HTTP for reading; and `ObjectStore`, which reaches S3,
Google Cloud Storage, Azure, and HTTP through `obstore`, the Python binding of the Rust
`object_store` crate. Icechunk has a storage layer of its own over S3, Google Cloud Storage,
Azure, R2, Tigris, and local disks, and adds transactions and versioned snapshots. Credentials go
through the usual mechanisms of each backend. Two features exist for object stores: consolidated
metadata, which puts the metadata of a whole hierarchy in one object so that opening a store does
not cost a request per node, and sharding, which packs many chunks into one object read by
range. All of this is Python: fsspec or obstore does the input and output.

**What the manifest needs.**

- **Reading through the library.** Building a manifest of a file in the cloud, and the assay,
  go through the library and so through its drivers. For S3 that is ros3; reaching the other
  clouds through the library needs a driver for each.
- **Reading chunks without the library.** With the address and size of every chunk in the
  manifest, a reader fetches byte ranges and decodes them itself. This needs a client for the
  store in C++. It is an optional dependency, so it lives in a library and an extension of its
  own, and the core never links it.
- **Writing.** ros3 is read only. An HDF5 file headed for the cloud is written locally and then
  uploaded, as a single object or in parts; the paged strategy and the page size are chosen
  before the upload, since they cannot be changed after. Zarr writes to the store directly, one
  object per chunk or per shard.
- **Saved manifests.** A manifest saved next to the file it describes, or a Kerchunk or Icechunk
  manifest exported from it, lives in the same store, and needs the same client to be written
  and read.

**Questions.**

1. Which clouds must be reached: AWS only, AWS and the services compatible with S3, or Google
   Cloud Storage and Azure too?
2. The client for the store in C++: a small one of pyre's own over HTTP with the AWS signature,
   the AWS SDK, or a binding to the Rust `object_store`, which already covers every cloud zarr
   reaches? The answer decides what the optional dependency is.
3. The credentials: the dictionary `pyre.h5.read` takes today, or a component with a protocol,
   so that profiles, environment variables, instance roles, and anonymous access are
   implementations that a user selects in configuration?
4. Does the endpoint of `File._pyre_ros3` become configurable, so that the services compatible
   with S3 are reachable through the library as well?


## Lenses

The manifest is generic: it knows shapes, cells, and bytes, not what a dataset means. Meaning comes
from a lens, a component that takes a manifest and tags its datasets.

- **The generic lens**, in pyre, classifies by rank, shape, and cell: rank two numeric datasets
  above a size are rasters, rank three are cubes, rank one and small ones are vectors and
  metadata. It needs no knowledge of the product, and gives any client a first answer to "what in
  this file can be looked at".
- **Product lenses** know a product. A NISAR lens matches the manifest against the product
  specification: it tags the rasters of each frequency and polarization with their selectors,
  the masks as masks, the layers of a GUNW as layers, and the metadata cubes of the radar and
  geolocation grids as cubes, with their axes. It lives with the code that knows NISAR, in qef,
  and is found by family, the way any other pyre component is.

A lens returns tags and selectors, never data. qed asks a manifest and its lens for the rasters
and their selectors, and builds its views from the answer. That is what lets qed open any HDF5
file through the generic lens, and a NISAR product through the NISAR lens, with the same reader.

pyre's h5 schemas already describe the expected structure of a product. A lens built from a
schema matches the expected structure against the actual one, and the mismatches, a dataset the
specification promises and the file does not have, a fill value declared one way and used
another, fall out as a side effect. That is the check of metadata against the product
specification the quality work asks for.


## What moves out of qed

- `occupancy`, `strip`, `filemap`, `states`, `apportion`, and `locality` become queries of the
  manifest.
- `tables` and `storage`, the walk, become the construction of the manifest.
- `nodata`, `decode`, `shuffle`, `unshuffle`, `uniform`, and `interpret` become the assay
  pass, in C++, reading through the library instead of decoding in Python.
- `paging` becomes a property of the manifest.
- The histograms and the formatting stay with the clients that draw them.

The quality panel and the `measure` tools then ask pyre for a manifest, and qef's census builds one
per product and saves it.


## Open questions

1. **Metadata.** Pages first; the recording driver when a file is not paged, or when the kind of
   metadata on a page matters. Is the format walk worth its upkeep?
2. **Virtual and external datasets.** Recorded with their mappings and not followed, or followed
   into the files they name?
3. **Attribute values.** Names and types always; values only below a size, or never?
4. **The saved format.** HDF5 with compound records, as above, or something smaller for the
   reductions a census keeps?
5. **The family of lenses.** `pyre.h5.lenses` for the protocol, with the generic lens as its
   default, and `qef.nisar.lenses.*` for the products?
6. **The home of the schema.** Once it no longer depends on HDF5, does the schema stay in
   `pyre.h5.schema`, with the zarr visitors beside it, or move to a package of its own that both
   formats use?


## Order of work

The investigation of the floor of HDF5 2 comes first, and its findings decide the floor against
which the steps below are built.

1. `Manifest` with the file, the objects, and the storage, and its tests on files written by the
   tests with known layouts, including hard links, compact and contiguous datasets, and a paged
   file.
2. The queries, checked against qed's `pages.py` on the same files, then on the GCOV fixture.
3. The bindings, with the numpy views, and `pyre.h5.manifest`.
4. `Assay`.
5. The generic lens and the lens protocol.
6. Saving and loading a manifest.
7. The bridge to zarr: the virtual export first, then the copies in both directions.

qed moves to the manifest once step 3 is done; the NISAR lens and the census follow in qef.


## Estimates

The estimates are in focused working days for one developer who knows pyre's h5 layer, and
include the comments, the tests, and the entries in the cmake build that every contribution
carries. For scale, `qed/pkg/readers/pages.py`, which the first four steps replace, is about 900
lines of Python.

| step | work | days |
|------|------|------|
| 1 | `Manifest`: the walk by object token, the dataset records, the storage sorted by address, the page index, the grid index, and test files with known layouts | 5–7 |
| 2 | the queries, checked against `pages.py` and then on the GCOV fixture; `cost`, the region to chunks to pages to bytes, is the only new one | 3–4 |
| 3 | the bindings with numpy views through the buffer protocol, and `pyre.h5.manifest` over the existing ros3 support | 2–3 |
| 4 | `Assay`: the policy, reading the chunks through the library, and the uniformity records | 3–4 |
| 5 | the lens protocol and the generic lens, once open question 5 is settled | 1–2 |
| 6 | saving and loading: compound records, a version, and the stamp of the source | 3–4 |

Steps 1 through 6 come to between three and a half and five weeks, and qed can move to the
manifest after two to two and a half of them. The entity tag in the stamp of step 6 is not
available through the library; recording it takes a request to the store, outside HDF5.

Step 7 carries most of the uncertainty, and is estimated in weeks:

- the virtual export as a Kerchunk manifest, whose reference format is JSON or parquet: under a
  week;
- the virtual export as an Icechunk manifest: one to two weeks through the Icechunk Python
  library, longer if pyre writes its binary format itself;
- the materialized copy from HDF5 to zarr, with a zarr v3 writer, the choice between copying and
  recompressing, rechunking, and leaving out the chunks of fill: one to two weeks;
- the copy from zarr to HDF5: one to two weeks once pyre's h5 writer is complete. The writer is
  not finished, and is a prerequisite whose own cost may exceed that of the copy;
- one schema for both formats: three to five days for the description of the cell shared with
  the manifest, two to three for the storage hints, and one to two weeks for the zarr reader and
  writer, with the tests that keep the existing spelling of `pyre.h5.schema` working. It precedes
  the copies of the bridge, which then go through it.

Some of the work the design implies is not in the order above:

- reading chunks without the library, with concurrent range requests and pyre's own deflate,
  shuffle, and fletcher decoders: one and a half to two weeks. The client for the store is an
  optional dependency, so it gets a library and an extension of its own;
- the recording driver of option 2 for the metadata: about a week. The format walk of option 3
  is four to eight weeks, plus upkeep with every new version of the format, which is the case for
  answering open question 1 with no;
- in the clients: moving qed to the manifest, three to five days; the NISAR lens in qef, about a
  week; building and saving a manifest per product in the census, two to three days; a lens
  built from an h5 schema that reports the mismatches with the specification, three to five days.

In total: about a month for the core, a month and a half to two months with the Kerchunk export
and the work in qed and qef, and three and a half to four and a half months for everything except
the format walk, with the shared schema and the h5 writer ahead of the copies of the bridge.

The investigation of the floor of HDF5 2 is three to five days. Moving `pyre::h5` to the new
floor, should it stand, is estimated after the investigation, since its cost depends on what it
finds: the changes to the description of complex cells and their tests, the containers and the
CI environments, and the discovery of the package by both builds. The manifest itself needs
nothing past 1.14: `H5Ovisit3` and the object tokens are from HDF5 1.12, and `H5Dchunk_iter`
from 1.14.


<!-- end of file -->
