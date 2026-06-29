# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# docker: the cli for building and running containers. it is a vendor-distributed tool, so mm does
# not install it — it only locates the executable and verifies its presence before a build that
# needs it. point {toolchain.docker.cli} at an absolute path when docker lives off the {PATH}
toolchain.docker.doc := "the docker cli; build and run containers (vendor-installed)"
toolchain.docker.kind := vendor
toolchain.docker.url := https://docs.docker.com/get-docker/

# docker is not version-pinned, so report whatever is installed by asking the cli. the lazy {=}
# assignment keeps the query out of every parse — {info} references it deferred, so the shell runs
# only when {docker.info} is actually invoked
toolchain.docker.version = $(shell $(toolchain.docker.cli) --version 2>/dev/null)


# install: docker cannot be fetched by mm; send the user to the vendor's download page
docker.install:
	@${call log.sec,"docker","docker is a vendor-distributed tool; mm cannot install it for you"}
	@${call log.info,"download and install it from:"}
	@${call log.info,"    $(toolchain.docker.url)"}

# update: same story as install — there is nothing for mm to fetch
docker.update: docker.install


# end of file
