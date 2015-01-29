# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# project defaults
include {project.name}.def
# the package name
PACKAGE = apache
# the stuff in this directory goes to {{etc/{project.name}/apache}}
EXPORT_ETCDIR = $(EXPORT_ROOT)/etc/$(PROJECT)
# the apache configuration files
APACHE_CONF = \
    $(PROJECT) \
    $(PROJECT).conf \
# the list of files
EXPORT_ETC = $(APACHE_CONF) \
    $(PROJECT).wsgi

# the standard build targets
all: tidy

# install
install: tidy
	$(RSYNC) $(RSYNCFLAGS) $(APACHE_CONF) $(APACHE_CONFIGURL)
	ssh $(APACHE_USERURL) 'addgroup $(APACHE_USER) {project.name}'
	ssh $(APACHE_USERURL) 'a2ensite {project.name}'

live:
	@echo ssh $(APACHE_USERURL) '$(RM_F) ${{addprefix $(APACHE_CONFIGDIR)/,$(APACHE_CONF)}}'
	@echo ssh $(APACHE_USERURL) '$(LN_S) $(PROJ_APACHE_CONF) $(APACHE_CONF)'
	@echo ssh $(APACHE_USERURL) 'a2ensite $(PROJECT)'
	@echo ssh $(APACHE_USERURL) 'service apache2 restart'

# restart the server after a configuration change
restart:
	ssh $(APACHE_USERURL) 'service apache2 restart'

# end of file
