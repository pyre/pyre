<!-- -*- Markdown -*-
   -
   - michael a.g. aïvázis <michael.aivazis@para-sim.com>
   - (c) 1998-2026 all rights reserved
   -->

# Grids, mosaics, and out-of-core data products: a HOWTO

> **Status:** working document. Seeded 2026-07-30, tracking the `mosaic` branch as the
> interface takes shape. Organized around use cases rather than classes: start from what
> you are trying to do, and the document leads you to the pieces you need. The C++ read
> and write paths and the python bindings — including the h5-backed mosaic — are
> implemented and exercised.

## Choosing your grid

Every grid is a *packing* (how index space maps to storage offsets) married to a
*storage strategy* (where the cells live). Most of the time you do not choose these
pieces individually; you start from your situation:

| your situation | build | see |
|---|---|---|
| a dense array that fits in memory | a heap grid | [use case 1](#uc1) |
| a flat binary product on disk | a file-backed grid | [use case 2](#uc2) |
| memory owned by someone else (numpy, another library) | a view grid | [use case 3](#uc3) |
| a window of a large chunked HDF5 product | a mosaic | [use case 4](#uc4) |
| shrinking the memory footprint of a long workflow | page release | [use case 5](#uc5) |
| handing cells to numpy without copying | the python bindings | [use case 6](#uc6) |
| writing or updating a chunked HDF5 product | a mosaic and `flush` | [use case 7](#uc7) |

Two decisions cut across all of them:

- **The cell type is yours to name, at compile time.** Whoever receives data must
  allocate for it, so the cell type appears in your source: as the template argument of
  a C++ grid, or the `cell` argument of a python factory. Everything else — dataset
  shapes, chunk shapes, window geometry — is discovered at runtime and travels through
  the runtime-rank flavors of the grid vocabulary.
- **Read-only is a property of the description, not a different API.** A grid over
  read-only cells supports the same interface; writes are refused at the boundary.
  Ask for read-only access where you open things: `writable=False` in the python
  factories, `H5F_ACC_RDONLY` when opening files.

<a name="uc1"></a>
## 1. A dense array that fits in memory

The baseline. In C++, pair a canonical packing with heap storage:

```c++
// the layout: 3x4, c-style order, anchored at zero
auto packing = pyre::grid::canonical_t<2> { { 3, 4 } };
// enough cells on the heap
auto storage = pyre::memory::heap_t<double> { packing.cells() };
// the grid
auto grid = pyre::grid::grid_t<decltype(packing), decltype(storage)> { packing, storage };
// address it with index tuples
grid[{ 1, 2 }] = 42.0;
```

From python, the factory names the cell type and the shape carries the rank:

```python
from pyre.extensions.pyre import grid
# a 3x4 grid of doubles
g = grid.heap(shape=[3, 4], cell="float64")
# index it directly
g[1, 2] = 42.0
# or through any consumer of the buffer protocol, with no copy
mv = memoryview(g)
```

Heap storage is uninitialized at birth; write before you read. Exhibits:
`tests/pyre.lib/grid/grid_heap_access.cc`, `tests/pyre.ext/grid/heap.py`.

<a name="uc2"></a>
## 2. A flat binary product on disk

File-backed grids memory-map their cells, so products larger than memory are readable
without staging, and writes persist without explicit saves:

```python
# create a product sized to the shape
g = grid.map(uri="product.dat", shape=[1024, 1024], cell="float32")
# ... fill it; dropping the grid unmaps and flushes ...

# reopen it later; {create=False} maps the existing file
h = grid.map(uri="product.dat", shape=[1024, 1024], cell="float32", create=False)

# examining a product you do not own: map it read-only
r = grid.map(uri="product.dat", shape=[1024, 1024], cell="float32",
             create=False, writable=False)
```

A read-only map refuses writes through indexing and marks its buffer protocol view
read-only, so numpy sees an immutable array. Asking for a *fresh* product that is
read-only is refused: a product that could never be filled is a mistake. Exhibits:
`tests/pyre.ext/grid/map.py`, `tests/pyre.ext/grid/readonly.py`.

<a name="uc3"></a>
## 3. Memory owned by someone else

A view grid lays a layout over cells some other entity exports, without copying. The
view holds the exporter alive for as long as the grid exists:

```python
import numpy
# someone else's memory
data = numpy.zeros((3, 4), dtype=numpy.float64)
# a grid over it; writes flow through to the array
v = grid.view(source=data, shape=[3, 4], cell="float64")

# read-only exporters work too; {bytes} is the canonical case
frozen = grid.view(source=b"\x01\x02\x03\x04\x05\x06", shape=[2, 3], cell="int8",
                   writable=False)
```

By default the view asks its source for write access, which read-only exporters refuse;
pass `writable=False` to ask only for read access. Exhibits:
`tests/pyre.ext/grid/view.py`, `tests/pyre.ext/grid/lifetime.py`,
`tests/pyre.ext/grid/readonly.py`.

<a name="uc4"></a>
## 4. A window of a large chunked HDF5 product

The out-of-core workflow. A chunked dataset knows its own geometry, so it can describe
itself as a *mosaic*: its extent diced into its chunks, over a store with one
demand-materialized page per chunk. Describing a product costs a page table and nothing
more, no matter how large the product is; memory is spent only on the chunks you touch.

Which recipe you want depends on one question: **can your algorithm work on partial
results?**

### 4a. Yes — interleave work with I/O

Ask for the full description, find the working set, and pull chunks one at a time. The
per-tile call is the seam where your processing goes:

```c++
// open the product
auto file = pyre::h5::File { uri, H5F_ACC_RDONLY, {}, {} };
auto dataset = file.openDataSet("product");

// the mosaic: the product's own chunking over an empty store; free at any scale
const auto mosaic = dataset.mosaic<double>();
// the chunks the algorithm's window touches
for (const auto & tile : mosaic.tilesOverlapping(base, extent)) {
    // pull one chunk into its page: materialize, clamp against the product's edge,
    // land the cells, record the deposit
    dataset.fill(mosaic, tile);
    // process it before pulling the next one, e.g. as a dense zero-copy pane
    auto pane = mosaic.pane(tile);
    // ... work ...
}
```

### 4b. No — declare your minimal acceptable mosaic and fill it

An algorithm that needs its whole window resident before it can start should not pay
loop ceremony. Declare the smallest mosaic that covers the window and ask for all of it:

```c++
// the smallest chunk-aligned mosaic that covers the window
auto window = dataset.mosaic<double>(base, extent);
// make it resident
dataset.fill(window);
// the cells are addressable in the product's own index space
auto value = window[{ row, col }];
```

The window mosaic holds one page per touched chunk — its footprint is your declared
working set, nothing more — and it addresses the product's own index coordinates, so
the algorithm is written as if the whole product were in memory.

Sweeping the window is a single range-based loop: the window is itself a layout — a
canonical box of `extent` anchored at `base` — and iterating a layout generates every
index in its box, in c order:

```c++
// visit every cell of the window
for (const auto & idx : pyre::h5::packing_t { extent, base }) {
    // in the product's own index space
    auto value = window[idx];
}
```

Iterate the *window's* box, not the mosaic: iterating a grid visits every cell of its
whole extent, resident or not, which is exactly what an out-of-core algorithm must
avoid.

### 4c. The whole product

For a product that fits in memory, the same two calls with the no-argument factory
load everything: `dataset.fill(dataset.mosaic<double>())`. The mosaic interface does
not moralize about product sizes; the census (below) tells you what you spent.

### What `fill` promises

- `fill` materializes the page, so you never call `reside` yourself on the read path.
- `fill` records the deposit (`validate`), since the call *is* the deposit.
- `fill` is unconditional: filling a warm tile re-reads it. Skip-if-warm is caller
  policy: guard with `mosaic.storage().valid(ordinal)` if you want a cache.
- Edge chunks are clamped against the product's extent; the overhang in their pages is
  padding, exactly as HDF5 stores it. You never see it: the mosaic addresses only real
  cells.
- Chunk alignment is a performance property, not a correctness requirement: `fill`
  moves cells through hyperslab selections, so a mosaic tiled differently than the
  dataset's storage still fills correctly — it just crosses chunk boundaries on disk.
- Misuse — a mosaic of the wrong rank, a tile outside the product — is an application
  error reported on the `pyre.h5.dataset` channel, not a firewall: what you pass is
  runtime data.

Exhibit: `tests/h5.lib/dataset_mosaic_read.cc` — a narrated end-to-end read, including
the clipped edge chunks and the no-ceremony coda.

<a name="uc5"></a>
## 5. Managing the memory footprint

The store underneath a mosaic keeps a census: `residents()` counts pages that exist,
`bytes()` is the memory bill. All page management is available through the mosaic's own
`storage()` accessor — management mutates through a shared handle, so a const reference
is all you need on a live mosaic.

A long workflow shrinks its working set by handing pages back:

```c++
// done with this chunk: return its page to the never-touched state
mosaic.storage().release(mosaic.packing().tileOrdinal(tile));
```

The rules:

| operation | effect |
|---|---|
| `reside` | materialize a page; allocates on first touch only |
| `validate` | declare that a page holds meaningful content |
| `taint` | declare that a page diverges from its backing store |
| `flush` | declare that a page matches its backing store again |
| `release` | forget a page entirely; it becomes indistinguishable from one never touched |
| `poison` | materialize a page and scribble a recognizable pattern, so unwritten cells stand out |

Releasing a page with unsaved content (`dirty`) draws a firewall: flush first. A
released tile can be filled again — it comes back as a fresh page. Anyone holding a
shared handle to a page's block (python panes do this) keeps the memory alive across a
release, but no longer aliases the mosaic's cells: release orphans outstanding panes
rather than invalidating them. Exhibits: `tests/pyre.lib/grid/mosaic_release.cc`,
`tests/pyre.lib/memory/paged_release.cc`.

<a name="uc6"></a>
## 6. Handing cells to numpy: the python bindings

Every python grid speaks the buffer protocol, so `memoryview(g)` and
`numpy.asarray(g)` see its cells with no copy, and hold them alive for as long as the
consumer exists — dropping the grid object is safe.

A mosaic cannot be a single buffer — its cells live on separate pages — so python
reaches it tile by tile, through panes:

```python
# an in-memory out-of-core grid: describe now, allocate as you touch
m = grid.mosaic(shape=[100, 100], tile=[10, 10], cell="float64")
# single cells work directly; writes materialize the page and taint it
m[35, 42] = 1.0
# bulk access goes through panes: dense zero-copy grids over one page each
for t in m.tilesOverlapping(base=[35, 42], shape=[20, 20]):
    # materialized on first touch
    p = m.pane(tile=t)
    # a pane is an ordinary grid: numpy sees it with no copy
    block = numpy.asarray(p)
```

Two things to keep in mind:

- **Panes are tile-local.** A pane addresses its cells at `[0 .. tileShape)`, not in
  the mosaic's index space — that is what the buffer protocol can express. The
  mosaic-space anchor is `tile * tileShape` if you need to translate.
- **State discipline is explicit.** Writing through a pane's buffer is invisible to
  the store, so declare it: `m.validate(tile=t)` after depositing content,
  `m.taint(tile=t)` after modifying it. (Writes through `m[i, j]` do this for you.)

The mosaic above is backed by anonymous memory. The h5-backed flavor comes from the
dataset itself, wired to pull and push chunks through the file:

```python
from pyre.extensions import libh5
# open the product and get the dataset
dataset = libh5.File(uri=uri, mode="r+").get(path="product")
# the mosaic, over the dataset's own chunking; nothing is resident
m = dataset.mosaic(cell="float64")
# or the smallest mosaic covering a window
w = dataset.mosaic(cell="float64", base=[70, 70], shape=[25, 25])
# pull chunks: one at a time, or wholesale
m.fill(tile=[1, 1])
w.fill()
# deposit through indexing (which declares for you) or through panes (declare yourself)
m[35, 45] = 42.0
# and make the file agree
m.flush()
```

A mosaic knows whether it has a backing store (`m.connected`); the in-memory flavor
raises on `fill`/wholesale `flush`, since there is nowhere to move cells to or from.
One boundary rule, invisible in ordinary use: the `Grid`/`Mosaic` classes are
registered per extension module, and cells cross between modules only through the
buffer protocol — hand numpy the pane, not the mosaic. Exhibits:
`tests/pyre.ext/grid/mosaic.py`, `tests/h5.ext/mosaic.py`, `tests/h5.ext/dcpl_fill.py`.

<a name="uc7"></a>
## 7. Writing a chunked product

The mirror of use case 4. A producer assembles a mosaic over the dataset it is filling,
deposits content through panes — declaring as it goes — and pushes the divergence back
into the file:

```c++
// create the product: schema first
auto dataset = file.createDataSet("product", type, space, dcpl, dapl);
// the producer's mosaic, over the dataset's own chunking
auto product = dataset.mosaic<double>();
const auto & tiles = product.packing();
// deposit, chunk by chunk
for (const auto & t : product.tilesOverlapping(tiles.origin(), tiles.shape())) {
    // materialize the page and deposit through its pane
    auto ordinal = tiles.tileOrdinal(t);
    product.storage().reside(ordinal);
    auto pane = product.pane(t);
    // ... write cells through {pane}, in product coordinates ...
    // declare the deposit and its divergence from the file
    product.storage().validate(ordinal);
    product.storage().taint(ordinal);
}
// make the file agree
dataset.flush(product);
```

### What `flush` promises

- `flush(mosaic)` means "make the file agree with me": it pushes pages that are
  resident *and* have diverged, and skips everything else — so it is cheap to call
  liberally, and calling it twice moves nothing the second time.
- `flush(mosaic, tile)` is the per-tile command: unconditional, like its mirror `fill`,
  except that a tile whose page was never materialized is refused — there is nothing
  to push.
- Both mark the pushed pages clean, and both clamp edge chunks against the product's
  extent: page padding never reaches the file.
- Declaring divergence is the producer's job. The library cannot see writes through a
  pane or a C++ reference, so `taint` is explicit; a producer that forgets gets a
  silent no-op from the wholesale flush. (From python, `m[i, j] = v` declares for you;
  bulk writes through a pane's buffer do not.)
- Nothing flushes implicitly. There is no flush-on-destruction: destructors cannot
  report i/o errors, and implicit persistence is how files get silently corrupted.

### Updating in place: read-modify-write

Partial updates compose from pieces you already have — `fill` the chunk, modify,
`taint`, `flush` — and only the touched chunk moves in either direction:

```c++
auto mosaic = dataset.mosaic<double>();
// the chunk that holds the cell
auto t = mosaic.packing().tileOf(probe);
// pull it, change it, declare, push
dataset.fill(mosaic, t);
mosaic[probe] = value;
mosaic.storage().taint(mosaic.packing().tileOrdinal(t));
dataset.flush(mosaic);
```

### Uninitialized cells: caveat emptor

Pages are born uninitialized, like any fresh allocation. Flushing a partially written
page pushes whatever the unwritten cells happen to hold. The correct idioms: cover the
whole tile, or `fill` first and modify. When hunting a suspected partial write,
`poison` materializes the page with a recognizable pattern — every byte `0xdb`, a nod
to the venerable `0xdeadbeef` — so unwritten cells stand out in the product instead of
masquerading as data:

```c++
// materialize and scribble; anything you forget to write is easy to spot
mosaic.storage().poison(ordinal);
```

## The exhibits

The test drivers double as runnable, narrated documentation:

| exhibit | demonstrates |
|---|---|
| `tests/h5.lib/dataset_mosaic_read.cc` | the out-of-core read, end to end |
| `tests/h5.lib/dataset_mosaic_write.cc` | the write side: produce, verify, update in place, poison |
| `tests/h5.lib/dataset_tiling.cc` | a dataset describing itself in grid vocabulary |
| `tests/pyre.lib/grid/mosaic_window.cc` | window mosaics at the grid level |
| `tests/pyre.lib/grid/mosaic_pane.cc` | zero-copy panes |
| `tests/pyre.lib/grid/mosaic_release.cc` | footprint management on a live mosaic |
| `tests/pyre.lib/memory/paged_state.cc` | the page-state discipline |
| `tests/pyre.ext/grid/mosaic.py` | the python mosaic |
| `tests/pyre.ext/grid/readonly.py` | read-only maps and views |


<!-- end of file -->
