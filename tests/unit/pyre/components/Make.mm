# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#


all: test

test: sanity metaclasses interfaces components

sanity:
	${PYTHON} ./sanity.py

metaclasses:
	${PYTHON} ./requirement.py
	${PYTHON} ./role.py
	${PYTHON} ./actor.py

interfaces:
	${PYTHON} ./interface_sanity.py
	${PYTHON} ./interface_declaration.py
	${PYTHON} ./interface_inheritance.py
	${PYTHON} ./interface_shadow.py
	${PYTHON} ./interface_inheritance_multi.py
	${PYTHON} ./interface_traits.py
	${PYTHON} ./interface_compatibility.py
	${PYTHON} ./interface_compatibility_report.py
	${PYTHON} ./interface_instantiation.py

components:
	${PYTHON} ./component_sanity.py
	${PYTHON} ./component_declaration.py
	${PYTHON} ./component_registration.py
	${PYTHON} ./component_configuration.py
	${PYTHON} ./component_inheritance.py
	${PYTHON} ./component_defaults.py
	${PYTHON} ./component_configuration_inheritance.py
	${PYTHON} ./component_shadow.py
	${PYTHON} ./component_inheritance_multi.py
	${PYTHON} ./component_traits.py
	${PYTHON} ./component_defaults.py
	${PYTHON} ./component_compatibility.py
	${PYTHON} ./component_compatibility_report.py
	${PYTHON} ./component_implements.py
	${PYTHON} ./component_bad_implementations.py
	${PYTHON} ./component_instantiation.py
	${PYTHON} ./component_configuration_instantiation.py
	${PYTHON} ./component_invocation.py
	${PYTHON} ./component_aliases.py --functor.μ=0.10 --gaussian.spread=0.10
	${PYTHON} ./component_binding.py


# end of file 
