<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# geometry over spaces of known dimension

A design for points, curves, surfaces and the relations among them, over an underlying space of
arbitrary but known dimension. The geometry is C++, in `pyre::geometry`, with `pyre.geometry` as
its Python layer, and `pyre.db` learns to store it in PostGIS.

Branch: `geometry` in `pyre`.

Status: **agreed** on 2026-11-07, nothing built yet.


## The model

A shape is a subset of a **space**. The space, not the shape, decides what a straight edge is, how
distance is measured, and which algorithms apply. Coordinates belong to a **chart** of the space:
the dateline and the poles are properties of the longitude–latitude chart, not of the sphere. A
**reference system** pairs a space with a chart and a datum, and carries the authority code that
PostGIS calls an SRID.

Spaces combine by Cartesian product. A shape in $A \times B$ that is a product of a shape in each
factor intersects another such shape exactly when the factors intersect pairwise, so the support
of a product needs no algorithm of its own.

Time is a one dimensional affine space: instants subtract to give durations, but do not add.

```mermaid
classDiagram
  direction LR
  class Space {
    <<concept>>
    +dimension() size_t
    +geodesic(p, q) Segment
    +distance(p, q) double
  }
  class Euclidean~d~
  class Sphere
  class Ellipsoid
  class Timeline
  class Lattice~d~
  class Product~A_B~
  class Chart~S~ {
    <<concept>>
    +coordinates(point) tuple
    +point(coordinates) Point
  }
  class LonLat~S~
  class ReferenceSystem~S~
  Space <|.. Euclidean
  Space <|.. Sphere
  Space <|.. Ellipsoid
  Space <|.. Timeline
  Space <|.. Lattice
  Space <|.. Product
  Chart <|.. LonLat
  ReferenceSystem o-- Space
  ReferenceSystem o-- Chart
```

### Spaces

- `Euclidean<d>`: $\mathbb{R}^d$, with straight edges.
- `Sphere`: $S^2$ of a given radius, with great circle edges.
- `Ellipsoid`: an oblate spheroid given by its semi-major axis and flattening, with geodesic
  edges computed by Karney's algorithms, written in pyre.
- `Timeline`: `Euclidean<1>` with an epoch, so that instants and durations are different types.
- `Lattice<d>`: a finite subset of $\mathbb{Z}^d$, the simplest space; a catalog of tracks and
  frames is one.
- `Product<A, B>`: the Cartesian product of two spaces.

### Points

`Point<S>` is an element of the space `S`. The coordinate array of today's `Point<dim, T>` becomes
the storage of `Euclidean` points, and `Brick` and `PointCloud` move onto it. Points on the sphere
and on the ellipsoid are stored as unit vectors in $\mathbb{R}^3$, which have no singularities at
the poles or at the dateline; longitude and latitude exist only through the chart.

A value carried by each vertex, what PostGIS calls the M coordinate, is a field over the vertices
of a shape, not a coordinate of the space.

### Edges

On the sphere and the ellipsoid, a flag on each shape decides how its edges are interpreted:
either as geodesics of the space, or as straight lines in the longitude–latitude chart. Data in
the wild uses both, and the common metadata repository calls them "geodetic" and "cartesian".


## Shapes

Every shape is a template over its space. There is no virtual base: shapes satisfy a `Shape`
concept, and `AnyShape` erases the type for heterogeneous collections and for the bindings, the
way `AnyGrid` does for grids. The names are mathematical; the PostGIS names appear only in the
codecs and in `pyre.db`.

```mermaid
classDiagram
  direction TB
  class Shape~S~ {
    <<concept>>
    +dimension() intrinsic
    +envelope() Box
  }
  Shape <|.. Point
  Shape <|.. Segment
  Shape <|.. Path
  Shape <|.. Arc
  Shape <|.. Curve
  Shape <|.. Polygon
  Shape <|.. CurvePolygon
  Shape <|.. Surface
  Shape <|.. Box
  Shape <|.. Collection
  Path <|-- Ring
  Polygon <|-- Triangle
  Surface <|-- Triangulation
  Box <|-- Interval
  Path *-- Point
  Segment *-- Point
  Curve o-- Path
  Curve o-- Arc
  Polygon *-- Ring
  CurvePolygon *-- Curve
  Surface *-- Polygon
  Triangulation *-- Triangle
  Collection o-- Shape
  Collection o-- AnyShape
```

The shapes cover everything PostGIS can store:

| PostGIS | `pyre::geometry` | note |
|---|---|---|
| `POINT` | `Point` | |
| `LINESTRING` | `Path` | a chain of segments |
| `LINEARRING` | `Ring` | a closed, simple path |
| `CIRCULARSTRING` | chained `Arc` | |
| `COMPOUNDCURVE` | `Curve` | paths and arcs end to end |
| `POLYGON` | `Polygon` | a boundary ring and rings for its holes |
| `CURVEPOLYGON` | `CurvePolygon` | |
| `TRIANGLE` | `Triangle` | |
| `POLYHEDRALSURFACE` | `Surface` | faces that share edges |
| `TIN` | `Triangulation` | |
| `MULTIPOINT`, `MULTILINESTRING`, `MULTIPOLYGON`, `MULTICURVE`, `MULTISURFACE` | `Collection<T>` | finite unions |
| `GEOMETRYCOLLECTION` | `Collection<AnyShape>` | |
| `BOX2D`, `BOX3D` | `Box` | products of intervals; the envelopes indices work on |
| Z coordinate | a dimension of the space | `Euclidean<3>`, or `Product<Ellipsoid, Euclidean<1>>` for height |
| M coordinate | a field over the vertices | |
| `geometry(T, srid)` | a shape in a planar reference system | |
| `geography(T, srid)` | a shape on `Ellipsoid` or `Sphere` | |
| `tstzrange` and the other ranges | `Interval` | core postgres |

A region in the sense of a search is a `Collection<Polygon>`, so disconnected regions are there
from the start. PostGIS rasters map onto `pyre.grid`, and PostGIS topology, which stores a planar
partition as a cell complex of nodes, edges and faces, comes later.


## Relations

The relations between two shapes are the patterns of their DE-9IM matrix, the dimensions of the
pairwise intersections of their interiors, boundaries and exteriors. `relate(a, b)` computes the
matrix, and the named relations are the patterns PostGIS also offers: `intersects`
($A \cap B \neq \emptyset$), `disjoint`, `contains` and `within`, `covers` and `coveredBy`,
`touches`, `crosses`, `overlaps` and `equals`. `intersects` and `covers` come first.

A relation is a binary operator that delegates to whichever of its operands knows how to compute
it:

```mermaid
sequenceDiagram
  participant caller
  participant op as intersects(a, b)
  participant a
  participant b
  caller->>op: intersects(a, b)
  op->>a: a.intersects(b)
  alt a knows the kind of b
    a-->>op: true or false
  else
    a-->>op: NotImplemented
    op->>b: b.intersects(a)
    b-->>op: true, false, or NotImplemented
  end
  op-->>caller: the answer, or an error that names both kinds
```

The symmetric relations need one method name for both directions, and the knowledge stays with the
shape that has it. In C++ the rule is static: `intersects(a, b)` is an overload set, and a generic
overload, selected by a concept, forwards to `intersects(b, a)` when only that one exists. Products
decompose factor by factor. The Python protocol serves shapes defined in Python.


## Measures and constructions

Measures depend on the metric of the space: `length`, `area`, `distance`, `centroid`.

Constructions build new shapes: `envelope`, `boundary` and `hull` first, then the set operations
`intersection`, `union` and `difference`. pyre writes all of them itself, the simpler ones first.


## Codecs

WKB and EWKB, WKT and EWKT, readers and writers in C++, and the GeoPackage blob, which is a short
header in front of WKB. GeoJSON lives in the Python layer.


## Layers

- `lib/pyre/geometry`: the spaces, charts, shapes, relations, measures, constructions and codecs.
- `extensions/pyre/geometry`: the bindings, with the shapes instantiated for `Euclidean<2>`,
  `Euclidean<3>`, `Sphere`, `Ellipsoid` and `Timeline`, one instantiation per line.
- `packages/pyre/geometry`: the Python layer, GeoJSON and the reflected protocol. The modules there
  today stay until they get in the way, and are replaced when they do.
- `packages/pyre/db`: the columns, indices and expressions that store the shapes in postgres.

The core library links nothing new. Anything that needs an outside library is a package of its
own; projections such as UTM may come from PROJ, once it is clear what relying on it costs.


## pyre.db

- Columns: `pyre.db.geometry(shape, srid, z, m)`, `pyre.db.geography(shape, srid, z, m)`,
  `pyre.db.box()` and `pyre.db.range(of=...)`, which render as `geometry(POLYGON, 4326)`,
  `tstzrange` and the like.
- Index declarations, with their access method: `btree`, `gist`, `spgist`, `brin`.
- Database extensions, such as `postgis`, declared with the schema.
- Spatial expressions in queries: the relations as `ST_Intersects`, `ST_Covers` and the rest, the
  envelope operator `&&`, and the overlap of ranges.
- Values travel as EWKB in the binary result format, through the C++ codec.


## Tests

Assert drivers, as in the rest of pyre. The `pyre.db` drivers check the SQL they generate without
a server. A suite against a live server, with PostGIS, runs in pyre's own docker containers and in
CI as a GitHub service container on a Linux runner; it comes at the end of the work.


<!-- end of file -->
