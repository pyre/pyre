<!-- -*- Markdown -*-
   -
   - michael a.g. aïvázis <michael.aivazis@para-sim.com>
   - (c) 1998-2026 all rights reserved
   -->

# The `pyre.filesystem` package

> **Status:** reference note, written 2026-09-16 from the implementation as it stands. It
> records the object model, the flavors, and the family of query backed filesystems that the
> earthaccess flavor is the first instance of, along with the refactoring that a second
> instance should trigger.

## Purpose

`pyre.filesystem` represents hierarchical collections of resources as trees of nodes, so that
code can walk, search, and open resources without knowing where they live. The tree is built
lazily: a filesystem is mounted over a source, and its contents are discovered on request,
one level or several at a time. A local directory, a zip archive, an S3 bucket, and the page
of results of a catalog query are all sources; the tree looks the same over each.

## The object model

The composite has two node types and one container that owns them.

- **`Node`** is a leaf. It holds a weak reference to its filesystem and nothing else; its
  metadata, its uri within the filesystem, and its explorer marker are looked up through the
  filesystem. `open` and `checksum` delegate to the filesystem as well, since only the
  filesystem knows how to reach the resource.
- **`Folder`** is a node with `contents`, a map from names to nodes. It supports subscripts
  by path, `find(pattern)` over the tree beneath it, `resolve(path)` which descends one level
  at a time discovering along the way, `mount(uri, filesystem)` which grafts a whole
  filesystem in as a node, and node factories that build children owned by the same
  filesystem. Insertion creates the intermediate folders and informs the filesystem.
- **`Filesystem`** is a folder that is also the owner of the tree. It keeps the **vnode
  table**, a weak map from nodes to `Info` records, and answers `info`, `open`, `checksum`,
  and `discover` for every node it owns. A discovery request on a node of another filesystem,
  e.g. one that was mounted in, is forwarded to its owner.

Metadata lives in `Info` records, never on nodes. Every record carries the node's `uri` and a
`sync` stamp, the time of the last discovery that touched it; `InfoFolder` and `InfoFile`
add the folder flag and the explorer marker, and flavors extend them with what their source
knows: `InfoStat` for the `stat` structure of local entries, `InfoZip*` for zip members,
`InfoGranule` for catalog records. A node is therefore cheap, and a flavor decides how much
to remember about each entry.

Explorers are visitors over the tree: `Finder` generates the nodes whose paths match a
pattern, and `TreeExplorer` and `SimpleExplorer` produce reports. `Node.dump` is the
debugging entry point over the tree explorer; nothing in the package serializes a tree, since
a tree is always reconstructible from its source.

## Discovery

`discover(root, levels)` is the one operation that touches the source. Its contract, common
to every flavor that has a physical source:

- it fills `root`, a folder, with nodes for what the source holds beneath it, to the requested
  depth, `levels` deep, with `None` meaning all of it;
- it is a refresh, not a merge: entries the source no longer holds are removed from the folder
  and forgotten by the vnode table, so a second discovery of the same folder leaves the tree
  matching the source;
- it stamps every record it touches with the time of the discovery, so `sync` says how fresh
  a listing is.

The virtual filesystem, which has no source, is always fully explored and `discover` is a
no-op on it. The zip flavor discovers everything on first request and nothing afterwards,
since the archive's table of contents is read whole.

## The flavors

| factory | source | discovery | metadata |
|---|---|---|---|
| `virtual()` | none; built by insertion | none | `InfoFolder`, `InfoFile` |
| `local(root)` | a directory on the host | a `Walker` lists a folder, a `Recognizer` types each entry from `stat` | `InfoStat` mixins per entry type |
| `zip(root)` | a zip archive | the whole table of contents, once | `InfoZipFolder`, `InfoZipFile` |
| `s3(session, root)` | a bucket, through `boto3` | one prefix per folder, delimiter `/`, paginated | `InfoFolder`, `InfoFile` with `sync` |
| `earthaccess(query, ...)` | the page a catalog query answers | the whole page, at the root | `InfoGranule` |
| `naked()` | one local file, no tree | none | `InfoStat` |

`hdf5` is declared and empty; the h5 layer represents its own hierarchy.

The local and s3 flavors share a shape: a `todo` pile of `(folder, level)` pairs, a `dead`
set seeded with the folder's current contents and drained as entries are seen again, and a
stamp per touched record. The pattern is not factored into the base class, and each flavor
carries its own copy.

## Query backed filesystems

The earthaccess flavor is the first instance of a distinct family: a filesystem whose contents
are **the records a query answers**, not the entries of a directory. The source cannot list a
folder; it can only run a query and hand back a page. Everything hierarchical about the tree
is therefore imposed on the page rather than read from the source. Such a filesystem has three
parts, all of them seams:

- **the engine** runs the query: `engine(query, count) -> (hits, page)`, where `hits` is the
  number of matches the source knows of in all and `page` is the records it handed back, at
  most `count` of them;
- **the layout** places a record on the tree: `layout(record) -> (folder, ..., leaf)`, the
  names of the folders that lead to the record and of the leaf that stands for it, so a flat
  page becomes a hierarchy the client finds useful, and the same page can be grouped
  differently by different clients;
- **the description** turns a record into the metadata of its leaf, keeping whatever every
  client of the source wants at hand and the record itself for those who want to dig.

The discovery contract is adapted to the page being the unit of freshness. A discovery at the
root re-runs the query and rebuilds the tree: records still on the page keep their nodes, so
clients holding on to a node see the update, records that vanished are dropped along with the
folders they leave empty, and newcomers are placed. A discovery anywhere below the root is
answered from the page in hand, fetched first if there has never been one, since the query
fetches the page as a whole and no folder can be refreshed on its own. `Folder.resolve`
discovers at the root as it descends, so a client that wants to reach a folder without
re-running the query subscripts the tree instead.

In the earthaccess flavor only the defaults are specific to the NASA common metadata
repository: the default engine drives the `earthaccess` query builder, imported lazily so the
dependency costs nothing until it is used, and the description reads the UMM record shape for
the payload size, the direct access links, and the acquisition window. The tree machinery is
general, and the tests exercise it with a canned engine and plain records, offline.

**Note for the second instance.** When another source of this kind appears, e.g. a STAC
catalog, a database query rendered as a tree, or any service that answers a page of records,
the general machinery should move to a base class of the family, with the flavor supplying
the default engine and the record description, the way the local and s3 flavors sit under
`Filesystem`. One instance does not justify the base class; two do. The seams are already in
place, so the split is mechanical.

## Open items

- The `todo`/`dead`/stamp pattern shared by the local and s3 discoveries could live in the
  base class.
- `Folder.remove` refuses folders; removal of subtrees is not implemented.
- `hdf5` is a placeholder.

<!-- end of file -->
