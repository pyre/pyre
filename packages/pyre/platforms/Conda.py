# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import json
import os

# the framework
import pyre

# superclass
from .Managed import Managed


# declaration
class Conda(Managed, family="pyre.platforms.packagers.conda"):
    """
    Support for conda environments

    The engine reads the on-disk install records in {conda-meta} directly, so it works with
    conda, mamba, and micromamba environments without ever invoking a conda front end
    """

    # constants
    name = "conda"

    # user configurable state
    environment = pyre.properties.path()
    environment.default = os.environ.get("CONDA_PREFIX")
    environment.doc = "the prefix of the conda environment to interrogate"

    # protocol obligations
    @pyre.export
    def about(self):
        """
        A phrase identifying this database, for provenance records
        """
        # name myself and the environment i interrogate, so provenance answers the question
        # of which environment a discovery came from
        return f"the '{self.name}' package database in '{self.environment}'"

    @pyre.export
    def prefix(self):
        """
        Retrieve the location of the active conda environment
        """
        # get the environment prefix
        prefix = self.environment
        # if there isn't one
        if not prefix:
            # build the message
            msg = "no conda environment: 'CONDA_PREFIX' is not set"
            # complain
            raise self.ConfigurationError(configurable=self, errors=[msg])
        # otherwise, hand it back
        return prefix

    @pyre.export
    def available(self):
        """
        Check whether this engine is functional on this host
        """
        # get the environment prefix
        prefix = self.environment
        # i'm functional if there is one and it has install records
        return bool(prefix) and (prefix / self._metadir).isDirectory()

    # implementation details
    def getInstalledPackages(self):
        """
        Grant access to the installed package index
        """
        # grab the index
        installed = self._installed
        # if this the first time the index is accessed
        if installed is None:
            # prime it
            installed = {
                package: (version, build)
                for package, version, build in self.retrieveInstalledPackages()
            }
            # and attach it
            self._installed = installed
        # in any case, return it
        return installed

    def retrieveInstalledPackages(self):
        """
        Scan the environment install records for package information
        """
        # form the path to the install records
        metadir = self.prefix() / self._metadir
        # go through the records
        for record in metadir.contents:
            # skip anything that isn't an install record
            if record.suffix != ".json":
                # and move on
                continue
            # the filename encodes the package name, version, and build string
            stem = record.stem
            # take it apart, from the right, since package names may contain dashes
            package, version, build = str(stem).rsplit("-", 2)
            # hand the triplet to the caller
            yield package, version, build
        # all done
        return

    def retrievePackageContents(self, package):
        """
        Generate a sequence with the contents of {package}
        """
        # get the environment prefix
        prefix = self.prefix()
        # look up the package
        version, build = self.info(package=package)
        # form the path to its install record
        record = prefix / self._metadir / f"{package}-{version}-{build}.json"
        # open it
        with record.open() as stream:
            # parse it
            meta = json.load(stream)
        # the record lists files relative to the environment prefix; absolutize each one
        for filename in meta.get("files", ()):
            # and hand it to the caller
            yield str(prefix / filename)
        # all done
        return

    # private data
    # the cache of the installed package index
    _installed = None
    # the environment directory with the install records
    _metadir = "conda-meta"


# end of file
