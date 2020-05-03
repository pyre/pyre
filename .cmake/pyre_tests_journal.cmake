# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# journal
#
pyre_test_python_testcase(journal/debug.py)
pyre_test_python_testcase(journal/debug-activation.py --journal.debug.activation)
pyre_test_python_testcase(journal/debug-activation.py --config=activation.pfg)
pyre_test_python_testcase_envvar("DEBUG_OPT=activation" journal/debug-activation.py)
pyre_test_python_testcase(journal/debug-injection.py)
pyre_test_python_testcase(journal/firewall.py)
pyre_test_python_testcase(journal/firewall-activation.py --journal.firewall.activation=off)
pyre_test_python_testcase(journal/firewall-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal/firewall-injection.py)
pyre_test_python_testcase(journal/info.py)
pyre_test_python_testcase(journal/info-activation.py --journal.info.activation)
pyre_test_python_testcase(journal/info-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal/info-injection.py)
pyre_test_python_testcase(journal/warning.py)
pyre_test_python_testcase(journal/warning-activation.py --journal.warning.activation=off)
pyre_test_python_testcase(journal/warning-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal/warning-injection.py)
pyre_test_python_testcase(journal/error.py)
pyre_test_python_testcase(journal/error-activation.py --journal.error.activation=off)
pyre_test_python_testcase(journal/error-activation.py --config=activation.pfg)
pyre_test_python_testcase(journal/error-injection.py)
pyre_test_python_testcase(journal/crosstalk.py)
pyre_test_python_testcase(journal/debug-injection.py --journal.device=import:journal.console)
pyre_test_python_testcase(journal/debug-injection.py --journal.device=import:journal.file --journal.device.log=journal.log)


# end of file
