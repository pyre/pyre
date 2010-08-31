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
	${PYTHON} ./exceptions.py

metaclasses:
	${PYTHON} ./requirement.py
	${PYTHON} ./role.py
	${PYTHON} ./actor.py

interfaces:
	${PYTHON} ./interface.py
	${PYTHON} ./interface_behavior.py
	${PYTHON} ./interface_property.py
	${PYTHON} ./interface_inheritance.py
	${PYTHON} ./interface_shadow.py
	${PYTHON} ./interface_inheritance_multi.py
	${PYTHON} ./interface_compatibility.py
	${PYTHON} ./interface_compatibility_reports.py
	${PYTHON} ./interface_instantiation.py

components:
	${PYTHON} ./component.py
	${PYTHON} ./component_family.py
	${PYTHON} ./component_behavior.py
	${PYTHON} ./component_property.py
	${PYTHON} ./component_facility.py
	${PYTHON} ./component_inheritance.py
	${PYTHON} ./component_shadow.py
	${PYTHON} ./component_inheritance_multi.py
	${PYTHON} ./component_compatibility.py
	${PYTHON} ./component_compatibility_reports.py
	${PYTHON} ./component_implements.py
	${PYTHON} ./component_class_registration.py
	${PYTHON} ./component_class_configuration.py
	${PYTHON} ./component_class_configuration_inheritance.py
	${PYTHON} ./component_class_binding.py
	${PYTHON} ./component_class_binding_implicit.py
	${PYTHON} ./component_class_validation.py
	${PYTHON} ./component_class_trait_matrix.py
	${PYTHON} ./component_defaults.py
	${PYTHON} ./component_instantiation.py
	${PYTHON} ./component_invocation.py
	${PYTHON} ./component_instance_registration.py
	${PYTHON} ./component_instance_configuration.py
	${PYTHON} ./component_instance_configuration_inheritance.py
	${PYTHON} ./component_instance_binding.py
#
	${PYTHON} ./component_bad_implementations.py
	${PYTHON} ./component_aliases.py --functor.μ=0.10 --gaussian.spread=0.10


# end of file 
