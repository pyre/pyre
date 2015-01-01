# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

PROJECT = pyre
PACKAGE = geometry
PROJ_CLEAN += $(EXPORT_MODULEDIR)/$(PACKAGE)

# default target
all: export

# export
EXPORT_PYTHON_MODULES = \
    CPGrid.py \
    Field.py \
    Grid.py \
    Mesh.py \
    Octree.py \
    Point.py \
    PointCloud.py \
    Simplex.py \
    SimplicialMesh.py \
    Surface.py \
    __init__.py

export:: export-package-python-modules


# end of file
