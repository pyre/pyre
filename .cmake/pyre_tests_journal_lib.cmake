# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# journal
#
pyre_test_driver(journal.lib/sanity.cc)
pyre_test_driver(journal.lib/chronicler-sanity.cc)
pyre_test_driver(journal.lib/inventory.cc)
pyre_test_driver(journal.lib/diagnostic-sanity.cc)
pyre_test_driver(journal.lib/diagnostic-injection.cc)
pyre_test_driver(journal.lib/channel-inventory.cc)
pyre_test_driver(journal.lib/index-lookup.cc)
pyre_test_driver(journal.lib/index-inventory.cc)
pyre_test_driver(journal.lib/debug-inventory.cc)
pyre_test_driver(journal.lib/debug-injection.cc)
pyre_test_driver(journal.lib/debug-null.cc)
pyre_test_driver_env(journal.lib/debug-envvar.cc DEBUG_OPT=pyre.journal.test)
pyre_test_driver(journal.lib/firewall-inventory.cc)
pyre_test_driver(journal.lib/firewall-injection.cc)
pyre_test_driver(journal.lib/firewall-null.cc)
pyre_test_driver(journal.lib/info-inventory.cc)
pyre_test_driver(journal.lib/info-injection.cc)
pyre_test_driver(journal.lib/warning-inventory.cc)
pyre_test_driver(journal.lib/warning-injection.cc)
pyre_test_driver(journal.lib/error-inventory.cc)
pyre_test_driver(journal.lib/error-injection.cc)
pyre_test_driver(journal.lib/debuginfo.c)
pyre_test_driver(journal.lib/firewalls.c)


# end of file
