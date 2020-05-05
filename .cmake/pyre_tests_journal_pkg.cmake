# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# journal
#
pyre_test_python_testcase(journal.pkg/debug_inventory.py)
pyre_test_python_testcase(journal.pkg/debug-activation.py --journal.debug.activation)
pyre_test_python_testcase(journal.pkg/debug-activation.py --config=activation.pfg)
pyre_test_python_testcase_envvar("DEBUG_OPT=activation" journal.pkg/debug-activation.py)
pyre_test_python_testcase(journal.pkg/debug-injection.py)
pyre_test_python_testcase(journal.pkg/firewall_inventory.py)
pyre_test_python_testcase(journal.pkg/firewall-activation.py --journal.firewall.activation=off)
pyre_test_python_testcase(journal.pkg/firewall-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal.pkg/firewall-injection.py)
pyre_test_python_testcase(journal.pkg/info_inventory.py)
pyre_test_python_testcase(journal.pkg/info-activation.py --journal.info.activation)
pyre_test_python_testcase(journal.pkg/info-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal.pkg/info-injection.py)
pyre_test_python_testcase(journal.pkg/warning_inventory.py)
pyre_test_python_testcase(journal.pkg/warning-activation.py --journal.warning.activation=off)
pyre_test_python_testcase(journal.pkg/warning-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal.pkg/warning-injection.py)
pyre_test_python_testcase(journal.pkg/error_inventory.py)
pyre_test_python_testcase(journal.pkg/error-activation.py --journal.error.activation=off)
pyre_test_python_testcase(journal.pkg/error-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal.pkg/error-injection.py)
pyre_test_python_testcase(journal.pkg/crosstalk.py)
pyre_test_python_testcase(journal.pkg/debug-injection.py --journal.device=import:journal.console)
pyre_test_python_testcase(journal.pkg/debug-injection.py --journal.device=import:journal.file --journal.device.log=journal.log)


# end of file
