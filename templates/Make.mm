# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre

TEMPLATES = \
    class.c++ \
    class.python \
    plexus \

#
all: export

#
TEMPLATE_DIR = $(EXPORT_ROOT)/templates
export::
	@find . -name \*~ -delete
	@$(RM_RF) $(TEMPLATE_DIR)
	@$(MKDIR) $(MKPARENTS) $(TEMPLATE_DIR)
	@$(CP_R) $(TEMPLATES) $(TEMPLATE_DIR)


# end of file
