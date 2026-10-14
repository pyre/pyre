#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that configuration files set dict traits either in their text form or one key at a time,
and that both lead to the same map
"""


def test() -> None:
    """
    Load a pfg and a yaml file that set the same map in both forms
    """
    # support
    import pyre

    # a component with a dict
    class Reader(pyre.component, family="pyre.tests.dict.files.reader"):
        """
        A component with a dict trait
        """

        # a map of strings
        selection = pyre.properties.kv()

    # load the configuration files
    pyre.loadConfiguration("component_dict_files.pfg")
    pyre.loadConfiguration("component_dict_files.yaml")

    # every one of the readers they configure
    for name in ("pfgtext", "pfgkeys", "yamltext", "yamlkeys"):
        # gets the same map
        assert dict(Reader(name=name).selection) == {"band": "L", "frequency": "A"}, name

    # access the store
    nameserver = pyre.executive.nameserver
    # every entry
    for name, source in (("pfgtext", ".pfg"), ("pfgkeys", ".pfg"), ("yamltext", ".yaml")):
        # remembers the file it came from
        locator = str(nameserver.getInfo(nameserver.hash(f"{name}.selection.band")).locator)
        # by name
        assert f"component_dict_files{source}" in locator, locator

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
