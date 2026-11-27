# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the server programs: managing a cluster needs no libpq, so they are looked for everywhere
# the directory where they live; the package database names it when it knows where they are, and
# otherwise it is wherever the PATH finds them
postgres.bin ?= ${patsubst %/,%,${dir ${shell command -v initdb 2> /dev/null}}}
# are the programs that make and run a cluster there?
postgres.programs := \
    ${if ${and ${wildcard $(postgres.bin)/initdb},${wildcard $(postgres.bin)/pg_ctl}},yes,}

# the drivers of the cluster manager in the {pyre.pkg} suite make clusters of their own, so they are
# told where the programs are
tests.pyre.pkg.db.cluster_lifecycle.argv := --cluster.programs=$(postgres.bin)
tests.pyre.pkg.db.cluster_restart.argv := --cluster.programs=$(postgres.bin)
# they leave the logs of their servers behind, and a failed run leaves its cluster too
tests.pyre.pkg.db.cluster_lifecycle.clean := cluster_lifecycle cluster_lifecycle.log
tests.pyre.pkg.db.cluster_restart.clean := cluster_restart cluster_restart.log
# and they are skipped where the programs are not
pyre.pkg.tests.drivers.exclude += \
    ${if $(postgres.programs),,db/cluster_lifecycle.py db/cluster_restart.py}


# check availability: the library talks to the server through the interfaces libpq 17 introduced,
# and an older libpq leaves it out of the build
libpq.available := ${call extern.is.atLeast,libpq,17}

# if a recent enough {libpq} is available
ifeq ($(libpq.available), libpq)


# postgres ships no python package of its own; its python lives in {packages/pyre/db}, part of
# {pyre.pkg}
pyre-postgres.packages :=
# a library
pyre-postgres.libraries := pyre-postgres.lib
# a python extension, deposited into the {pyre} package that hosts it
pyre-postgres.extensions := pyre-postgres.ext
# the library stands on its own, so it gets a c++ suite of its own; the extension suite exercises
# the bindings, and the package suite exercises {pyre.db} against the server. all three are
# skipped whole when no server answers
pyre-postgres.tests := pyre-postgres.lib.tests pyre-postgres.ext.tests pyre-postgres.pkg.tests


# the postgres library meta-data; it is header only, and it knows nothing about python
pyre-postgres.lib.root := lib/postgres/
pyre-postgres.lib.stem := pyre-postgres
# deposit the headers under the {pyre} namespace so they never collide in a shared prefix
pyre-postgres.lib.incdir := $(builder.dest.inc)pyre/postgres/
# the gateway header is deposited one level above the rest, as {pyre/postgres.h}
pyre-postgres.lib.gateway := postgres.h
pyre-postgres.lib.prerequisites := journal.lib
pyre-postgres.lib.extern := journal.lib libpq
pyre-postgres.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-postgres.lib.c++.defines += $(pyre.lib.c++.defines)

# the postgres extension meta-data; it wraps the library above
pyre-postgres.ext.root := extensions/postgres/
# the module stays {postgres}; {packages/pyre/extensions} re-exports it as {libpq}
pyre-postgres.ext.stem := postgres
# the module rides in the {pyre} package, alongside {libpyre}
pyre-postgres.ext.pkg := pyre.pkg
pyre-postgres.ext.wraps := pyre-postgres.lib
pyre-postgres.ext.capsule :=
pyre-postgres.ext.extern := pyre.lib journal.lib libpq pybind11 python
pyre-postgres.ext.lib.c++.flags += $(pyre-postgres.lib.c++.flags)
pyre-postgres.ext.lib.c++.defines += $(pyre-postgres.lib.c++.defines)
pyre-postgres.ext.lib.prerequisites += pyre-postgres.lib journal.lib # pyre.lib is added automatically


# the server the testsuites talk to
# each suite makes a cluster of its own, unless told to use a server that is already running
postgres.fixture ?= yes

# the suites below exclude all their drivers when there is no server for them
ifeq ($(postgres.fixture),yes)
# with clusters of their own, they run wherever the programs that make and run a cluster are
postgres.live := ${if $(postgres.programs),live,}
# and when they cannot run, say why
${if $(postgres.live),,${warning the postgres suites are skipped: ${strip \
    there is no initdb and pg_ctl in ${or $(postgres.bin),the PATH}}}}
else
# otherwise, they run when they can log in to the server libpq's environment names
postgres.live := ${shell psql -XAtqc 'select 1' --dbname=postgres > /dev/null 2>&1 && echo live}
# and when they cannot, the reason is a setup problem, so say so
${if $(postgres.live),,\
    ${warning the postgres suites are skipped: could not log in to the server at \
        ${or ${value PGHOST},the default socket}, port ${or ${value PGPORT},5432}, \
        as ${or ${value PGUSER},${value USER}}}}
endif

# the cluster of a testsuite: its data live in the staging area of the suite, and its socket in a
# directory of its own under /tmp, since a path to a socket is limited to about a hundred
# characters, and the staging area can be deeper than that
#   usage: postgres.cluster {testsuite}
define postgres.cluster =
    # the data directory
    ${eval $(1).cluster.data := $(builder.staging)pyre-postgres/$(1)/cluster}
    # the directory of the socket, named after a checksum of the data directory
    ${eval $(1).cluster.socket := /tmp/pyre-${shell printf '%08x' \
        ${shell printf '%s' '$($(1).cluster.data)' | cksum | cut -d ' ' -f 1}}}
    # the command that manages the cluster
    ${eval $(1).cluster.manage := $(builder.dest.bin)pyre-postgres}
    # and its settings: a superuser {pyre}, and a server that need not survive a crash
    ${eval $(1).cluster.settings := \
        --cluster.programs=$(postgres.bin) \
        --cluster.data=$($(1).cluster.data) --cluster.socket=$($(1).cluster.socket) \
        --cluster.user=pyre --cluster.locale=C --cluster.durable=no}

    # the suite starts with a fresh cluster, and removes it after its last driver
    ${eval $(1).pre := $(1).cluster.start}
    ${eval $(1).post := $(1).cluster.stop}
    # its drivers find the server through libpq's environment, cleared of the settings that
    # could send them to a different one
    ${eval $(1).env := env -u PGDATABASE -u PGPASSWORD -u PGSERVICE -u PGHOSTADDR \
        PGHOST=$($(1).cluster.socket) PGPORT=5432 PGUSER=pyre}

# make and start the cluster, once whatever the suite needs is built, since the command that
# manages it is part of pyre
$(1).cluster.start: | $($(1).prerequisites)
	@${call log.action,start,"the postgres cluster of $(1)"}
	@$($(1).cluster.manage) restart $($(1).cluster.settings)

# stop and remove it
$(1).cluster.stop:
	@${call log.action,stop,"the postgres cluster of $(1)"}
	@$($(1).cluster.manage) remove $($(1).cluster.settings)

# a run of some of the drivers leaves the cluster up, so cleaning the suite removes it, along with
# the log of its server; without the command that manages it, there is no server to stop
$(1).clean::
	@${call log.action,clean,"the postgres cluster of $(1)"}
	@[ ! -x $($(1).cluster.manage) ] || $($(1).cluster.manage) remove $($(1).cluster.settings)
	@$(rm.force) $($(1).cluster.data).log

# the hooks are not files
.PHONY: $(1).cluster.start $(1).cluster.stop

# all done
endef


# get the testsuites
include pyre-postgres.lib.tests pyre-postgres.ext.tests pyre-postgres.pkg.tests

# give each one its cluster
ifeq ($(postgres.fixture)$(postgres.live),yeslive)
${foreach suite,$(pyre-postgres.tests),${eval ${call postgres.cluster,$(suite)}}}
endif


endif


# end of file
