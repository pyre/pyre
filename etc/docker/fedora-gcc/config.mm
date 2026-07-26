# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# with {pkgdb: adhoc} the externals are declared here; fedora puts everything in the system
# prefix with libraries under {lib64}, and openmpi in its own home activated by environment
# modules that this cell bypasses

# gsl
gsl.dir := /usr
gsl.libpath := /usr/lib64

# hdf5: the serial flavor
hdf5.dir := /usr
hdf5.libpath := /usr/lib64

# python
python.dir := /usr
python.libpath := /usr/lib64

# pybind11 is header only
pybind11.dir := /usr

# the flavor logic gates the library list on the version
mpi.version := 5.0
# openmpi lives in its own home
mpi.dir := /usr/lib64/openmpi
mpi.flavor := openmpi


# end of file
