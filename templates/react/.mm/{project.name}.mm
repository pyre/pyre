# -*- Makefile -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# {project.name} consists of a python package
{project.name}.packages := {project.name}.pkg
# libraries
{project.name}.libraries := 
# python extensions
{project.name}.extensions :=
# a ux bundle
{project.name}.webpack := {project.name}.ux
# and some tests
{project.name}.tests := {project.name}.pkg.tests


# load the packages
include $({project.name}.packages)
# the libraries
include $({project.name}.libraries)
# the extensions
include $({project.name}.extensions)
# the ux
include $({project.name}.webpack)
# and the test suites
include $({project.name}.tests)


# end of file
